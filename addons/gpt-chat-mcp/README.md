# gpt-chat MCP

Minimal **zero-dependency** MCP stdio server that lets an MCP client (Claude Code, Codex, etc.)
chat directly with **OpenAI GPT‑5.5** — a different model family, for cross-model second opinions / sparring.

## Tools

| Tool | Purpose |
|------|---------|
| `ask_gpt` | Chat with GPT. Provide `prompt` or `messages` (multi-turn). Optionally attach local `files` — text/code/csv/json are inlined, png/jpg/gif/webp go in as **vision**, pdf as a document. |
| `pipe_chat_to_gpt` | Feed the **current Claude Code session transcript** (newest `.jsonl`, auto-detected) to GPT‑5.5 together with a `question`, for an outside review of the conversation so far. |

### `ask_gpt` params
`prompt` · `messages[]` · `system` · `files[]` (local paths) · `model` (default `gpt-5.5`) · `reasoning_effort` (`none|low|medium|high|xhigh`) · `max_completion_tokens` · `wiki_access` (default `true`)

### `pipe_chat_to_gpt` params
`question` (required) · `files[]` · `transcript_path` · `project_dir` · `max_chars` (default 60000, keeps most recent) · `model` · `reasoning_effort` · `wiki_access` (default `true`)

## GPT-side wiki access (v2.1)

Both tools expose two **read-only function-calling tools to GPT itself**: `search_wiki` (ranked
keyword search over the knowledge wiki's `.md` pages) and `read_wiki_page` (read one page, 40k-char
cap). GPT can pull the pages it needs for its judgment instead of relying on whatever the caller
thought to attach — the owner's rule: the sparring partner must consult the same knowledge base.
Sandbox: path-containment to `GPT_MCP_WIKI_DIR`, `.md` only, dot-dirs skipped, per-project `.memory/`
dirs deliberately NOT exposed (may hold private data). Tool outputs pass the same secret redaction.
The reply footer shows a `[wiki]` trace of the calls GPT made. Disable per call with `wiki_access:false`.

Implementation note: calls go through **`/v1/responses`** (not `/v1/chat/completions`) because
function tools + `reasoning_effort` are only supported there for gpt-5.5.

## API key — read at runtime, never stored

The server reads the OpenAI key at call time. Resolution order:

1. `OPENAI_API_KEY` env var, else
2. first `sk-…` match in the file at `GPT_MCP_KEY_FILE` (default `<KEY_FILE>`).

The key is **never** written to config, source, or the repo.

## Safety: secret redaction

All outgoing message text is passed through a redaction step **before** it reaches the OpenAI API:
`sk-…` keys and `api-key/bearer/token: …` lines become `[REDACTED]`. This means piping a transcript
or attaching a file can't accidentally exfiltrate the key (e.g. if it appears in the chat history).

## Config (env)

| Var | Default | Meaning |
|-----|---------|---------|
| `GPT_MCP_MODEL` | `gpt-5.5` | default model id |
| `GPT_MCP_KEY_FILE` | `<KEY_FILE>` | key source file |
| `GPT_MCP_PROJECT_DIR` | `process.cwd()` | project root used to locate its transcript folder |
| `GPT_MCP_WIKI_DIR` | `<WIKI_DIR>` | root of the knowledge wiki exposed (read-only) to GPT |
| `OPENAI_API_KEY` | — | overrides the key file if set |

## Register (Claude Code, user scope)

```sh
claude mcp add gpt-chat -s user -- node "<GPTCHAT_MCP_DIR>\server.mjs"
```

## Requirements

Node ≥ 18 (uses native `fetch`). No npm install, no dependencies.
