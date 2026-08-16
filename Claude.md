# Claude.md — Claude Code adapter

This file is the Claude Code entrypoint for `<WIKI_DIR>`.

Mission in one sentence: this repository is the shared long-term memory for
projects, discussions, decisions, verified development experience, guardrails,
and reusable agent/team knowledge, so future Claude/Codex/GPT sessions start
with context instead of rediscovering it.

Read [WIKI_PROTOCOL.md](WIKI_PROTOCOL.md) first. That file is the canonical,
tool-neutral protocol for this knowledge library and is shared with Codex/GPT.

## Scope guardrail

- This repository is `<WIKI_DIR>`.
- Do not use any other repository as authority for this knowledge library unless
  the user explicitly asks for cross-repo comparison.
- If the current working directory is not this repository, stop and confirm the
  target before changing files.

## Claude operating rules

1. Use `Wiki/index.md` to orient before answering or writing.
2. Use `WIKI_PROTOCOL.md` for capture, ingest, experience, ADR, guardrail, and
   team-challenge workflows.
3. Keep `Raw/` immutable.
4. After every wiki change, update `Wiki/index.md` when navigation changes and
   append an entry to `Wiki/log.md`.
5. Preserve unverified but valuable discussion in `Wiki/journal/sessions/`
   before distilling it into knowledge, experience, ADRs, or guardrails.
6. File reusable development learnings under `Wiki/experience/` only after a
   green verifier.
7. Do not assume missing facts, user intent, project boundaries, architecture
   rules, or import decisions. Verify from evidence or ask the human before
   acting on the unknown.
8. For GPT memories, chat exports, or other bulk imports: structure an import
   review report first; the human approves categories/batches before any import.
   Personal or sensitive topics require explicit review.
9. When Claude/Codex or subagents may work in parallel, treat the worktree as
   shared mutable state: check status before editing, preserve unrelated changes,
   and stop before overwriting unclear work.
10. Never store secrets, API keys, private credentials, private account data, or
   unredacted sensitive logs; never commit or push them to GitHub.
11. Before committing, show the diff and get user approval unless the user has
   explicitly requested an automatic commit.

## Post-reinstall smoke test — is the wiki + recall MCP live?

Run this after any reinstall or fresh setup to confirm the wiki memory actually
works. **Architecture note:** the recall MCP (`knowledge-recall`) is a
**CLI-level** registration in `~/.claude.json` (top-level `mcpServers`),
independent of the Claude **Desktop** app. A Desktop reinstall / renaming
`%APPDATA%\Claude` does **not** affect it; wiping or replacing `~/.claude.json`
or the recall venv **does**. Desktop-app plugins/MCP (e.g. `localsynapse`,
extensions) live separately under `%APPDATA%\Claude` and are restored on their
own.

**Green = all four pass:**

1. **Registered** — `~/.claude.json` → top-level `mcpServers.knowledge-recall`
   exists with `command` (recall venv `python.exe`), `args`
   (`recall-mcp/server.py serve`), and `env.WIKI_DIR` =
   `<WIKI_DIR>/Wiki`. Expected extras:
   `RECALL_EXTRA_DIRS` (e.g. `<EXTRA_MEMORY_DIR>`), `RECALL_MODEL`,
   `RECALL_DB`.
2. **Binaries on disk** — the venv `python.exe` and `recall-mcp/server.py` both
   resolve (paths from the `command`/`args` above).
3. **Functional in-session** — `search_notes` on a known topic returns hits;
   `reindex` reports N indexed files + the embedding model; `read_note` loads a
   note. NOTE: `read_note` paths are rooted at the `Wiki/` subdir → use
   `"index.md"`, **not** `"Wiki/index.md"`.
4. **Direct filesystem** — this repo is readable at
   `<WIKI_DIR>` (e.g. `WIKI_PROTOCOL.md`).

**If red:** re-add the `knowledge-recall` block to `~/.claude.json` (values
above), recreate the recall venv if missing, then run `reindex`. The engine and
its recall MCP live in `<ENGINE_DIR>`.
