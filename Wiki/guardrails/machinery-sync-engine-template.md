# Machinery sync: keep the engine template in step with the live system

**Summary**: The `knowledge-wiki-engine` repo (`<ENGINE_DIR>`) is a content-free mirror of the system *machinery*. Whenever you change that machinery, mirror it into the engine in the same unit of work so the two never drift.

**Type**: guardrail
**Applies to**: any change to system machinery (not project content)
**Last updated**: 2026-07-17

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: needs-review — no trigger recorded at all

---

## Rule

When you change any of:
- `WIKI_PROTOCOL.md`, the `Claude.md` / `AGENTS.md` adapters, `Templates/`, `Wiki/roster/`, the generic guardrails, or the methodology pages; **or**
- the `~/.claude` machinery (agents / skills / commands / global `CLAUDE.md` / hook scripts); **or**
- the recall MCP, the **gpt-chat sparring MCP** (cross-model second opinion incl. its GPT-side
  read-only wiki tools — owner decision 17.07.2026: part of the engine), or Codex setup,

…then refresh the engine template **in the same change** — `sync.ps1` / `sync.sh` in the engine repo (or a targeted copy + genericize), then review `git diff`, commit, push.

Genericization on the way in: machine paths → placeholders (`<WIKI_DIR>`, `<ENGINE_DIR>`, `~/.claude`), project names → generic, drop dangling links; verify no secrets / user paths / broken links leaked. Run `scripts/wiki-audit.py` to confirm.

## Why

The engine is the reusable, shareable form of the system. If it drifts, a fresh clone bootstraps an **outdated** team. Treat "machinery change" and "engine refresh" as one change — like code and its test.

## What NOT to sync

Project content — `Wiki/projects`, project-specific `Wiki/knowledge`, journals, ADRs, `Raw/` — stays in the live wiki only. The engine stays content-free (a few generic example pages aside).

## Related pages
- [[no-secrets-or-private-account-data]]
- [[repo-boundary-llm-knowledge-library]]
- [[third-party-skill-agent-security-audit]]
