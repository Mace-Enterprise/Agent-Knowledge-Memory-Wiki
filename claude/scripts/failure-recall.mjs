#!/usr/bin/env node
/**
 * failure-recall.mjs — Failure-triggered knowledge recall (PostToolUse hook).
 *
 * On a failed Bash/PowerShell tool call, searches the local knowledge-recall
 * index with a normalized error signature and injects the top hits as
 * additional context. Guardrails (per GPT-5.5 sparring, 2026-07-04):
 * secret redaction, path/line/hash normalization, max ~900-token injection,
 * per-fingerprint cooldown, mandatory JSONL logging (the KPI data source).
 *
 * Also: `node failure-recall.mjs --report` prints KPI aggregates from the log.
 *
 * Never breaks the tool loop: any internal error -> exit 0, no output.
 *
 * Register in ~/.claude/settings.json:
 *   "hooks": { "PostToolUse": [ { "matcher": "Bash|PowerShell", "hooks": [
 *     { "type": "command", "command": "node \"<path-to>/failure-recall.mjs\"", "timeout": 25 } ] } ] }
 * Adjust RECALL_DIR / RECALL_ENV below to your installation.
 */
import { readFileSync, existsSync, mkdirSync, appendFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import path from "node:path";
import os from "node:os";

const RECALL_DIR = "<RECALL_MCP_DIR>";
const PYTHON = path.join(RECALL_DIR, ".venv/Scripts/python.exe");
const RECALL_ENV = {
  WIKI_DIR: "<WIKI_DIR>/Wiki",
  RECALL_EXTRA_DIRS: "<EXTRA_MEMORY_DIR>",
  // Must match the MCP registration (~/.claude.json) — mixing embedding models
  // in one DB silently corrupts semantic search.
  RECALL_MODEL: "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  RECALL_DB: "<RECALL_MCP_DIR>/recall-index-ml.sqlite",
  // Windows console default is cp1252 -> UnicodeEncodeError / mojibake on piped
  // stdout when notes contain umlauts/arrows. Force clean UTF-8 end to end.
  PYTHONUTF8: "1",
  PYTHONIOENCODING: "utf-8",
};
const STATE_DIR = path.join(os.homedir(), ".claude", "state", "failure-recall");
const STATE_FILE = path.join(STATE_DIR, "state.json");
const LOG_FILE = path.join(STATE_DIR, "log.jsonl");
const COOLDOWN_MS = 30 * 60 * 1000; // same fingerprint at most every 30 min
const MAX_HITS = 3;
const MAX_INJECT_CHARS = 2800; // ~700-900 tokens

const FAIL_RX = /error|exception|traceback|fatal|failed|cannot|denied|refused|not recognized|no such|not found|missing|invalid/i;

function redact(s) {
  return s
    .replace(/(api[_-]?key|token|secret|passwd|password|bearer|authorization|pwd)[=:\s"']+\S+/gi, "$1=[REDACTED]")
    .replace(/\b[A-Za-z0-9+/_-]{32,}\b/g, "[BLOB]");
}

function normalize(s) {
  return s
    .replace(/\x1b\[[0-9;]*m/g, "")                      // ANSI
    .replace(/[A-Za-z]:\\[^\s:'"()]+\\/g, "")             // win dir prefixes -> keep basename
    .replace(/\/(?:[\w.-]+\/)+/g, "")                     // posix dir prefixes -> keep basename
    .replace(/:\d+(?::\d+)?\b/g, ":N")                    // line:col numbers
    .replace(/\b0x[0-9a-fA-F]+\b/g, "0xN")
    .replace(/\b[0-9a-f]{7,40}\b/g, "[HASH]")
    .replace(/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/gi, "[UUID]")
    .replace(/\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}[\d:.]*\b/g, "[TS]");
}

function asText(v) {
  if (v == null) return "";
  if (typeof v === "string") return v;
  try { return JSON.stringify(v); } catch { return String(v); }
}

function detectFailure(resp) {
  // Harness response shapes vary; be defensive and only fire on strong signals.
  const o = (resp && typeof resp === "object") ? resp : {};
  for (const k of ["exitCode", "exit_code", "code", "returnCode"]) {
    if (typeof o[k] === "number") return o[k] !== 0 ? { failed: true, why: `exit=${o[k]}` } : { failed: false };
  }
  const stderr = asText(o.stderr);
  if (stderr.trim() && FAIL_RX.test(stderr)) return { failed: true, why: "stderr" };
  const all = asText(resp);
  if (/command failed|non-zero exit|Traceback \(most recent call last\)|CommandNotFoundException|NativeCommandError/i.test(all))
    return { failed: true, why: "pattern" };
  return { failed: false };
}

function buildSignature(input, resp) {
  const cmd = asText(input?.command).split(/\s+/).slice(0, 3).join(" ");
  const raw = [asText(resp?.stderr), asText(resp?.stdout), asText(resp)].find((t) => t.trim()) || "";
  const tail = raw.split(/\r?\n/).slice(-60);
  const errLines = tail.filter((l) => FAIL_RX.test(l)).slice(-5);
  const sigLines = errLines.length ? errLines : tail.slice(-5);
  const norm = normalize(redact(sigLines.join("\n"))).trim();
  const query = (cmd + " " + norm.replace(/\s+/g, " ")).slice(0, 220).trim();
  const fingerprint = createHash("sha1").update(norm || query).digest("hex").slice(0, 16);
  return { query, fingerprint };
}

function underCooldown(fp) {
  let state = {};
  try { state = JSON.parse(readFileSync(STATE_FILE, "utf8")); } catch {}
  const now = Date.now();
  const hit = state[fp];
  const blocked = hit && now - hit.last < COOLDOWN_MS;
  state[fp] = { last: now, count: (hit?.count || 0) + 1 };
  // prune entries older than 7 days so the file stays tiny
  for (const k of Object.keys(state)) if (now - state[k].last > 7 * 864e5) delete state[k];
  try { mkdirSync(STATE_DIR, { recursive: true }); writeFileSync(STATE_FILE, JSON.stringify(state)); } catch {}
  return blocked;
}

function search(query) {
  const out = execFileSync(PYTHON, ["server.py", "search", query], {
    cwd: RECALL_DIR,
    env: { ...process.env, ...RECALL_ENV },
    timeout: 15000,
    windowsHide: true,
    encoding: "utf8",
  });
  const arr = JSON.parse(out);
  if (!Array.isArray(arr)) return [];
  // navigation pages (index/log) are noise, not knowledge
  return arr.filter((h) => !/\/(log|index)\.md$/i.test(h.path || "")).slice(0, MAX_HITS);
}

function log(entry) {
  try {
    mkdirSync(STATE_DIR, { recursive: true });
    appendFileSync(LOG_FILE, JSON.stringify(entry) + "\n");
  } catch {}
}

function report() {
  let lines = [];
  try { lines = readFileSync(LOG_FILE, "utf8").trim().split("\n").filter(Boolean).map((l) => JSON.parse(l)); } catch {}
  if (!lines.length) { console.log("failure-recall: no log entries yet."); return; }
  const byWeek = {};
  const fpCounts = {};
  let injected = 0, gaps = 0;
  for (const e of lines) {
    const wk = e.ts.slice(0, 10);
    byWeek[wk] = (byWeek[wk] || 0) + 1;
    fpCounts[e.fingerprint] = (fpCounts[e.fingerprint] || 0) + 1;
    if (e.injected) injected++;
    if (e.n_hits === 0) gaps++;
  }
  const repeats = Object.values(fpCounts).filter((c) => c > 1).length;
  console.log(`failure-recall KPI report (${lines.length} failure events)`);
  console.log(`  injections:        ${injected} (${Math.round((100 * injected) / lines.length)}%)`);
  console.log(`  gaps (0 hits):     ${gaps}  <- missing-gotcha candidates for /learn`);
  console.log(`  repeat fingerprints: ${repeats}  <- same error recurring (target: falling)`);
  console.log(`  events per day:`);
  for (const [d, n] of Object.entries(byWeek).sort()) console.log(`    ${d}: ${n}`);
  const top = Object.entries(fpCounts).sort((a, b) => b[1] - a[1]).slice(0, 5);
  console.log(`  top fingerprints: ${top.map(([f, n]) => `${f}x${n}`).join(", ")}`);
}

// ---- main ----
try {
  if (process.argv.includes("--report")) { report(); process.exit(0); }

  const input = JSON.parse(readFileSync(0, "utf8"));
  const tool = input.tool_name || "";
  if (!/^(Bash|PowerShell)$/.test(tool)) process.exit(0);

  const verdict = detectFailure(input.tool_response);
  if (!verdict.failed) process.exit(0);

  const { query, fingerprint } = buildSignature(input.tool_input, input.tool_response);
  if (!query || query.length < 8) process.exit(0);
  if (underCooldown(fingerprint)) {
    log({ ts: new Date().toISOString(), cwd: input.cwd, tool, fingerprint, query, n_hits: -1, injected: false, skipped: "cooldown" });
    process.exit(0);
  }
  if (!existsSync(PYTHON)) process.exit(0);

  const hits = search(query);
  const entry = {
    ts: new Date().toISOString(), cwd: input.cwd, tool, fingerprint, why: verdict.why,
    query, n_hits: hits.length, hits: hits.map((h) => ({ path: h.path, score: h.score })), injected: hits.length > 0,
  };
  log(entry);
  if (!hits.length) process.exit(0);

  let ctx = "Failure-triggered recall (auto): der fehlgeschlagene Befehl matcht Wissens-Notes — VOR dem naechsten Versuch pruefen:\n";
  for (const [i, h] of hits.entries()) {
    const snip = (h.snippet || "").replace(/\s+/g, " ").slice(0, 180);
    ctx += `${i + 1}. ${h.title} — ${h.path}\n   ${snip}\n`;
  }
  ctx = ctx.slice(0, MAX_INJECT_CHARS) + "(Volltext: read_note(path). Quelle: knowledge-recall, Treffer koennen irrelevant sein — bewerten, nicht blind folgen.)";

  process.stdout.write(JSON.stringify({
    suppressOutput: true,
    hookSpecificOutput: { hookEventName: "PostToolUse", additionalContext: ctx },
  }));
  process.exit(0);
} catch {
  process.exit(0);
}
