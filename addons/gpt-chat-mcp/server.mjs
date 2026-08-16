#!/usr/bin/env node
// Minimal zero-dependency MCP stdio server: chat directly with OpenAI GPT-5.5.
// Reads the API key at runtime from a file (never stored in config/repo).
//
// Tools:
//   ask_gpt            - chat with GPT, optionally attaching local files (text/code/csv/img/pdf)
//   pipe_chat_to_gpt   - feed the current Claude Code session transcript to GPT + ask about it
//
// GPT-side wiki access (Owner rule 17.07.2026: the sparring partner must be able to consult
// the knowledge wiki itself): both tools expose read-only function-calling tools to GPT
// (search_wiki / read_wiki_page), sandboxed to the wiki directory. Default ON (wiki_access:false
// to disable). Deliberately NOT covering per-project .memory dirs (may hold private data).
//
// Protocol: MCP over stdio = newline-delimited JSON-RPC 2.0. Logs -> stderr ONLY.

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { createInterface } from "node:readline";
import { homedir } from "node:os";
import { join, basename, resolve, sep } from "node:path";

const DEFAULT_MODEL = process.env.GPT_MCP_MODEL || "gpt-5.5";
const KEY_FILE = process.env.GPT_MCP_KEY_FILE || "<KEY_FILE>";
// /v1/responses statt /v1/chat/completions: nur dort sind Function-Tools MIT reasoning_effort
// erlaubt (400 bei chat/completions, getestet 17.07.2026) — noetig fuer den Wiki-Zugriff.
const API_URL = "https://api.openai.com/v1/responses";

const TEXT_EXT = new Set([
  "txt","md","markdown","py","pine","js","mjs","cjs","ts","tsx","jsx","json","jsonl",
  "csv","tsv","yaml","yml","toml","ini","cfg","conf","xml","html","htm","css","sql",
  "sh","ps1","bat","c","cpp","cc","h","hpp","cs","java","go","rs","rb","php","r","lua","log","env",
]);
const IMG_MIME = { png:"image/png", jpg:"image/jpeg", jpeg:"image/jpeg", gif:"image/gif", webp:"image/webp" };
const PER_FILE_TEXT_CAP = 200_000; // chars
const MAX_BINARY_BYTES = 25 * 1024 * 1024; // 25MB guard for base64 inline

function log(...a) { process.stderr.write("[gpt-chat] " + a.join(" ") + "\n"); }
function extOf(p) { const i = p.lastIndexOf("."); return i < 0 ? "" : p.slice(i + 1).toLowerCase(); }

function getApiKey() {
  if (process.env.OPENAI_API_KEY) return process.env.OPENAI_API_KEY.trim();
  const txt = readFileSync(KEY_FILE, "utf8");
  for (const line of txt.split(/\r?\n/)) {
    const m = line.match(/sk-[A-Za-z0-9_-]{20,}/);
    if (m) return m[0];
  }
  throw new Error("No OpenAI API key found in " + KEY_FILE);
}

// ---- file attachment handling -------------------------------------------------
// Returns { textInline, mediaBlocks[], notes[] }
function buildAttachments(paths) {
  const out = { textInline: "", mediaBlocks: [], notes: [] };
  for (const p of paths) {
    let buf;
    try { buf = readFileSync(p); } catch (e) { out.notes.push(`could not read ${p}: ${e.message}`); continue; }
    const name = basename(p);
    const ext = extOf(p);
    if (IMG_MIME[ext]) {
      if (buf.length > MAX_BINARY_BYTES) { out.notes.push(`${name}: image too large (${buf.length} bytes), skipped`); continue; }
      const url = `data:${IMG_MIME[ext]};base64,${buf.toString("base64")}`;
      out.mediaBlocks.push({ type: "image_url", image_url: { url } });
      out.notes.push(`${name}: attached as image`);
    } else if (ext === "pdf") {
      if (buf.length > MAX_BINARY_BYTES) { out.notes.push(`${name}: pdf too large (${buf.length} bytes), skipped`); continue; }
      const data = `data:application/pdf;base64,${buf.toString("base64")}`;
      out.mediaBlocks.push({ type: "file", file: { filename: name, file_data: data } });
      out.notes.push(`${name}: attached as pdf`);
    } else if (TEXT_EXT.has(ext) || ext === "") {
      let s = buf.toString("utf8");
      if (s.length > PER_FILE_TEXT_CAP) s = s.slice(0, PER_FILE_TEXT_CAP) + `\n...[truncated, file was ${s.length} chars]`;
      out.textInline += `\n\n===== FILE: ${name} =====\n${s}\n===== END FILE: ${name} =====\n`;
      out.notes.push(`${name}: inlined as text (${s.length} chars)`);
    } else {
      // unknown binary -> try utf8, else skip
      const s = buf.toString("utf8");
      if (/�/.test(s.slice(0, 1000))) { out.notes.push(`${name}: unsupported binary type .${ext}, skipped`); continue; }
      out.textInline += `\n\n===== FILE: ${name} =====\n${s.slice(0, PER_FILE_TEXT_CAP)}\n===== END FILE: ${name} =====\n`;
      out.notes.push(`${name}: inlined as text (best-effort)`);
    }
  }
  return out;
}

// ---- transcript discovery + parsing ------------------------------------------
function projectSlug(dir) { return dir.replace(/[:\\/]/g, "-"); }

function findLatestTranscript(explicitPath, projectDir) {
  if (explicitPath && existsSync(explicitPath)) return explicitPath;
  const root = join(homedir(), ".claude", "projects");
  const candidates = [];
  const dirsToScan = [];
  if (projectDir) {
    const d = join(root, projectSlug(projectDir));
    if (existsSync(d)) dirsToScan.push(d);
  }
  if (!dirsToScan.length && existsSync(root)) {
    for (const e of readdirSync(root)) {
      const d = join(root, e);
      try { if (statSync(d).isDirectory()) dirsToScan.push(d); } catch {}
    }
  }
  for (const d of dirsToScan) {
    let files;
    try { files = readdirSync(d); } catch { continue; }
    for (const f of files) {
      if (!f.endsWith(".jsonl")) continue;
      const fp = join(d, f);
      try { candidates.push({ fp, mtime: statSync(fp).mtimeMs }); } catch {}
    }
  }
  candidates.sort((a, b) => b.mtime - a.mtime);
  return candidates.length ? candidates[0].fp : null;
}

function textFromContent(content) {
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  const parts = [];
  for (const b of content) {
    if (!b || typeof b !== "object") continue;
    if (b.type === "text" && b.text) parts.push(b.text);
    else if (b.type === "tool_use") parts.push(`[tool_use: ${b.name || "?"}]`);
    else if (b.type === "tool_result") parts.push(`[tool_result]`);
  }
  return parts.join("\n");
}

function parseTranscript(path, maxChars) {
  const raw = readFileSync(path, "utf8");
  const lines = raw.split(/\r?\n/);
  const turns = [];
  for (const line of lines) {
    const t = line.trim();
    if (!t) continue;
    let obj; try { obj = JSON.parse(t); } catch { continue; }
    const role = obj.message?.role || (obj.type === "user" ? "user" : obj.type === "assistant" ? "assistant" : null);
    if (role !== "user" && role !== "assistant") continue;
    const txt = textFromContent(obj.message?.content);
    if (!txt || !txt.trim()) continue;
    turns.push(`### ${role.toUpperCase()}\n${txt.trim()}`);
  }
  let joined = turns.join("\n\n");
  let truncated = false;
  if (maxChars && joined.length > maxChars) {
    joined = "...[earlier turns truncated]...\n\n" + joined.slice(joined.length - maxChars);
    truncated = true;
  }
  return { text: joined, turnCount: turns.length, truncated, file: path };
}

// ---- secret redaction (never ship keys to OpenAI) -----------------------------
function redactSecrets(s) {
  if (typeof s !== "string") return s;
  return s
    .replace(/sk-[A-Za-z0-9_\-]{20,}/g, "[REDACTED_OPENAI_KEY]")
    .replace(/\b(?:api[-_ ]?key|bearer|token)\b\s*[:=]\s*\S+/gi, (m) => m.replace(/\S+$/, "[REDACTED]"));
}
function redactMessages(messages) {
  for (const m of messages) {
    if (typeof m.content === "string") m.content = redactSecrets(m.content);
    else if (Array.isArray(m.content)) for (const b of m.content) if (b && b.type === "text") b.text = redactSecrets(b.text);
  }
  return messages;
}

// ---- wiki access for GPT (read-only function calling) --------------------------
const WIKI_DIR = process.env.GPT_MCP_WIKI_DIR || "<WIKI_DIR>";
const WIKI_PAGE_CAP = 40_000;     // chars per read_wiki_page
const WIKI_MAX_TOOL_ROUNDS = 8;   // agentic-loop guard

function walkWikiFiles() {
  const out = [];
  const stack = [WIKI_DIR];
  while (stack.length) {
    const dir = stack.pop();
    let entries;
    try { entries = readdirSync(dir, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      if (e.name.startsWith(".")) continue; // .git, .obsidian, ...
      const fp = join(dir, e.name);
      if (e.isDirectory()) stack.push(fp);
      else if (e.name.toLowerCase().endsWith(".md")) out.push(fp);
      if (out.length >= 3000) return out;
    }
  }
  return out;
}
function wikiRel(p) { return p.slice(WIKI_DIR.length).replace(/^[\\/]+/, "").replace(/\\/g, "/"); }

function searchWiki(query, limit = 8) {
  const terms = String(query || "").toLowerCase().split(/[^a-z0-9äöüß_-]+/).filter((t) => t.length >= 3);
  if (!terms.length) return [];
  const scored = [];
  for (const fp of walkWikiFiles()) {
    let body;
    try { body = readFileSync(fp, "utf8").slice(0, 60_000); } catch { continue; }
    const lower = body.toLowerCase();
    const pathLower = wikiRel(fp).toLowerCase();
    let score = 0, firstHit = -1;
    for (const t of terms) {
      if (pathLower.includes(t)) score += 4;
      let n = 0, i = lower.indexOf(t);
      if (i >= 0 && (firstHit < 0 || i < firstHit)) firstHit = i;
      while (i >= 0 && n < 5) { n++; i = lower.indexOf(t, i + t.length); }
      score += n;
    }
    if (score > 0) {
      const title = (body.match(/^#\s+(.+)$/m) || [, ""])[1] || basename(fp);
      const at = Math.max(0, (firstHit < 0 ? 0 : firstHit) - 120);
      scored.push({ path: wikiRel(fp), title, score, snippet: body.slice(at, at + 320).replace(/\s+/g, " ") });
    }
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, Math.max(1, Math.min(20, limit)));
}

function readWikiPage(rel) {
  const fp = resolve(join(WIKI_DIR, String(rel || "").replace(/^[\\/]+/, "")));
  if (!(fp + sep).startsWith(resolve(WIKI_DIR) + sep) && fp !== resolve(WIKI_DIR))
    throw new Error("path escapes wiki root");
  if (!fp.toLowerCase().endsWith(".md")) throw new Error("only .md pages are readable");
  let s = readFileSync(fp, "utf8");
  if (s.length > WIKI_PAGE_CAP) s = s.slice(0, WIKI_PAGE_CAP) + `\n...[truncated, page was ${s.length} chars]`;
  return s;
}

// Responses-API tool shape (flat, not nested under `function`)
const WIKI_GPT_TOOLS = [
  { type: "function",
    name: "search_wiki",
    description: "Search the owner's knowledge wiki (verified experience patterns, guardrails, ADRs, methodology, project profiles). Returns ranked pages with path/title/snippet. Consult it BEFORE judging, so your opinion uses the same knowledge base as the team (rejected approaches live here as tombstones).",
    parameters: { type: "object", properties: {
      query: { type: "string", description: "Keywords, German or English." },
      limit: { type: "integer", description: "Max results (default 8, cap 20)." },
    }, required: ["query"] },
  },
  { type: "function",
    name: "read_wiki_page",
    description: "Read one wiki page by the relative path returned from search_wiki.",
    parameters: { type: "object", properties: {
      path: { type: "string", description: "Relative path, e.g. Wiki/experience/patterns/x.md" },
    }, required: ["path"] },
  },
];

function execWikiTool(name, args) {
  if (name === "search_wiki") return JSON.stringify(searchWiki(args.query, args.limit || 8));
  if (name === "read_wiki_page") return readWikiPage(args.path);
  throw new Error("unknown tool " + name);
}

// ---- OpenAI call via /v1/responses (with optional GPT-side wiki tool loop) -----
// Chat-Completions message blocks -> Responses input blocks
function toResponsesInput(messages) {
  return messages.map((m) => {
    if (typeof m.content === "string") return { role: m.role, content: m.content };
    const blocks = [];
    for (const b of m.content || []) {
      if (b.type === "text") blocks.push({ type: "input_text", text: b.text });
      else if (b.type === "image_url") blocks.push({ type: "input_image", image_url: b.image_url?.url });
      else if (b.type === "file") blocks.push({ type: "input_file", filename: b.file?.filename, file_data: b.file?.file_data });
    }
    return { role: m.role, content: blocks };
  });
}

async function callOpenAI({ model, messages, reasoning_effort, max_completion_tokens, wikiAccess }) {
  redactMessages(messages);
  const toolTrace = [];
  const usage = { prompt_tokens: 0, completion_tokens: 0 };
  let usedModel = model;
  const baseParams = (b) => {
    if (reasoning_effort && reasoning_effort !== "none") b.reasoning = { effort: reasoning_effort };
    if (max_completion_tokens) b.max_output_tokens = max_completion_tokens;
    if (wikiAccess) b.tools = WIKI_GPT_TOOLS;
    return b;
  };
  let body = baseParams({ model, input: toResponsesInput(messages) });
  for (let round = 0; round <= WIKI_MAX_TOOL_ROUNDS; round++) {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + getApiKey() },
      body: JSON.stringify(body),
    });
    const text = await res.text();
    if (!res.ok) throw new Error(`OpenAI ${res.status}: ${text.slice(0, 800)}`);
    const data = JSON.parse(text);
    usage.prompt_tokens += data.usage?.input_tokens || 0;
    usage.completion_tokens += data.usage?.output_tokens || 0;
    usedModel = data.model || model;
    const calls = (data.output || []).filter((o) => o.type === "function_call");
    if (wikiAccess && calls.length && round < WIKI_MAX_TOOL_ROUNDS) {
      const outputs = [];
      for (const c of calls) {
        let out;
        try {
          const a = JSON.parse(c.arguments || "{}");
          out = execWikiTool(c.name, a);
          toolTrace.push(`${c.name}(${(a.query || a.path || "").slice(0, 60)})`);
        } catch (e) { out = "ERROR: " + (e && e.message); toolTrace.push(`${c.name}: ERROR`); }
        outputs.push({ type: "function_call_output", call_id: c.call_id, output: redactSecrets(String(out)).slice(0, 60_000) });
      }
      body = baseParams({ model, previous_response_id: data.id, input: outputs });
      continue;
    }
    const texts = (data.output || []).filter((o) => o.type === "message")
      .flatMap((o) => (o.content || []).filter((c) => c.type === "output_text").map((c) => c.text));
    return { content: texts.join("\n").trim() || "(empty response)", model: usedModel, usage, toolTrace };
  }
  return { content: "(wiki tool loop limit reached without final answer)", model: usedModel, usage, toolTrace };
}

// ---- tool definitions ---------------------------------------------------------
const TOOLS = [
  {
    name: "ask_gpt",
    description:
      "Chat directly with OpenAI GPT-5.5 (a different model family than Claude/Codex) for a cross-model second opinion / sparring. " +
      "Provide `prompt` (single question) or `messages` (multi-turn). Optionally attach local `files` " +
      "(text/code/csv/json inlined; png/jpg/gif/webp as vision; pdf as document). GPT can itself search/read " +
      "the knowledge wiki via built-in read-only tools (default on; disable with wiki_access:false). Returns GPT's reply.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "The question/message (use this OR messages)." },
        messages: {
          type: "array",
          description: "Multi-turn conversation; items {role:'system'|'user'|'assistant', content:string}.",
          items: { type: "object", properties: { role: { type: "string" }, content: { type: "string" } }, required: ["role", "content"] },
        },
        system: { type: "string", description: "Optional system instruction (prepended in prompt mode)." },
        files: { type: "array", items: { type: "string" }, description: "Local file paths to attach to the (last) user message." },
        model: { type: "string", description: "Model id. Default " + DEFAULT_MODEL + " (e.g. gpt-5.5, gpt-5.5-pro, gpt-5.4)." },
        reasoning_effort: { type: "string", enum: ["none", "low", "medium", "high", "xhigh"], description: "Default medium." },
        max_completion_tokens: { type: "integer", description: "Optional reply length cap." },
        wiki_access: { type: "boolean", description: "Let GPT search/read the knowledge wiki itself (read-only). Default true." },
      },
    },
  },
  {
    name: "pipe_chat_to_gpt",
    description:
      "Pipe the current Claude Code chat to GPT-5.5: reads the most recent session transcript (.jsonl) " +
      "and sends it to GPT along with your question, for an outside second opinion on the conversation so far. " +
      "By default auto-detects the latest transcript across all projects.",
    inputSchema: {
      type: "object",
      properties: {
        question: { type: "string", description: "What to ask GPT about the conversation (e.g. 'where is this reasoning weak?')." },
        files: { type: "array", items: { type: "string" }, description: "Optional extra local files to attach." },
        transcript_path: { type: "string", description: "Explicit .jsonl path (else auto-detected)." },
        project_dir: { type: "string", description: "Project root to locate its transcript folder (else newest across all)." },
        max_chars: { type: "integer", description: "Max transcript chars to send (default 60000, keeps most recent)." },
        model: { type: "string", description: "Default " + DEFAULT_MODEL + "." },
        reasoning_effort: { type: "string", enum: ["none", "low", "medium", "high", "xhigh"], description: "Default medium." },
        wiki_access: { type: "boolean", description: "Let GPT search/read the knowledge wiki itself (read-only). Default true." },
      },
      required: ["question"],
    },
  },
];

// ---- JSON-RPC plumbing --------------------------------------------------------
function send(obj) { process.stdout.write(JSON.stringify(obj) + "\n"); }
function ok(id, result) { send({ jsonrpc: "2.0", id, result }); }
function err(id, code, message) { send({ jsonrpc: "2.0", id, error: { code, message } }); }
function textResult(id, text, isError) { ok(id, { content: [{ type: "text", text }], ...(isError ? { isError: true } : {}) }); }

// build messages, attaching files to the last user message when present
function attachFilesToMessages(messages, files) {
  if (!files || !files.length) return { messages, notes: [] };
  const att = buildAttachments(files);
  // find last user message
  let idx = -1;
  for (let i = messages.length - 1; i >= 0; i--) if (messages[i].role === "user") { idx = i; break; }
  if (idx === -1) { messages.push({ role: "user", content: "" }); idx = messages.length - 1; }
  const m = messages[idx];
  const baseText = (typeof m.content === "string" ? m.content : "") + att.textInline;
  const content = [{ type: "text", text: baseText }, ...att.mediaBlocks];
  messages[idx] = { role: "user", content };
  return { messages, notes: att.notes };
}

async function handleAskGpt(id, args) {
  let messages = [];
  if (Array.isArray(args.messages) && args.messages.length) {
    messages = args.messages.map((x) => ({ role: x.role, content: x.content }));
  } else if (typeof args.prompt === "string" && args.prompt.length) {
    if (args.system) messages.push({ role: "system", content: args.system });
    messages.push({ role: "user", content: args.prompt });
  } else {
    return err(id, -32602, "Provide `prompt` or `messages`.");
  }
  const { messages: withFiles, notes } = attachFilesToMessages(messages, args.files);
  try {
    const r = await callOpenAI({
      model: args.model || DEFAULT_MODEL,
      messages: withFiles,
      reasoning_effort: args.reasoning_effort || "medium",
      max_completion_tokens: args.max_completion_tokens,
      wikiAccess: args.wiki_access !== false,
    });
    const noteLine = notes.length ? `\n[attachments] ${notes.join("; ")}` : "";
    const wikiLine = r.toolTrace && r.toolTrace.length ? `\n[wiki] ${r.toolTrace.join(" → ")}` : "";
    const footer = `\n\n— ${r.model} · in:${r.usage.prompt_tokens ?? "?"} out:${r.usage.completion_tokens ?? "?"} tok${noteLine}${wikiLine}`;
    textResult(id, r.content + footer);
  } catch (e) { textResult(id, "ERROR: " + (e && e.message), true); }
}

async function handlePipeChat(id, args) {
  const path = findLatestTranscript(args.transcript_path, args.project_dir || process.env.GPT_MCP_PROJECT_DIR || process.cwd());
  if (!path) return textResult(id, "ERROR: no transcript (.jsonl) found.", true);
  let tr;
  try { tr = parseTranscript(path, args.max_chars || 60000); } catch (e) { return textResult(id, "ERROR reading transcript: " + e.message, true); }

  const system = "You are GPT-5.5 acting as an outside reviewer of a Claude Code session transcript. " +
    "Another AI (Claude) and a user have been working together below. Give a candid, blind-spot-catching " +
    "second opinion. Be specific and concise.";
  const userText = `## QUESTION\n${args.question}\n\n## TRANSCRIPT (${tr.turnCount} turns${tr.truncated ? ", truncated to most recent" : ""}, from ${basename(path)})\n\n${tr.text}`;

  let messages = [{ role: "system", content: system }, { role: "user", content: userText }];
  const { messages: withFiles, notes } = attachFilesToMessages(messages, args.files);
  try {
    const r = await callOpenAI({
      model: args.model || DEFAULT_MODEL,
      messages: withFiles,
      reasoning_effort: args.reasoning_effort || "medium",
      wikiAccess: args.wiki_access !== false,
    });
    const noteLine = notes.length ? `; ${notes.join("; ")}` : "";
    const wikiLine = r.toolTrace && r.toolTrace.length ? ` · wiki: ${r.toolTrace.join(" → ")}` : "";
    const footer = `\n\n— ${r.model} · transcript:${basename(path)} (${tr.turnCount} turns) · in:${r.usage.prompt_tokens ?? "?"} out:${r.usage.completion_tokens ?? "?"} tok${noteLine}${wikiLine}`;
    textResult(id, r.content + footer);
  } catch (e) { textResult(id, "ERROR: " + (e && e.message), true); }
}

const rl = createInterface({ input: process.stdin });
rl.on("line", async (line) => {
  line = line.trim();
  if (!line) return;
  let msg; try { msg = JSON.parse(line); } catch { return; }
  const { id, method, params } = msg;

  if (method === "initialize") {
    return ok(id, { protocolVersion: "2024-11-05", capabilities: { tools: {} }, serverInfo: { name: "gpt-chat", version: "2.1.0" } });
  }
  if (method === "notifications/initialized" || method === "initialized") return;
  if (method === "ping") return ok(id, {});
  if (method === "tools/list") return ok(id, { tools: TOOLS });
  if (method === "tools/call") {
    const name = params && params.name;
    const args = (params && params.arguments) || {};
    if (name === "ask_gpt") return handleAskGpt(id, args);
    if (name === "pipe_chat_to_gpt") return handlePipeChat(id, args);
    return err(id, -32602, "Unknown tool: " + name);
  }
  if (id !== undefined) err(id, -32601, "Method not found: " + method);
});

log("started, default model=" + DEFAULT_MODEL);
