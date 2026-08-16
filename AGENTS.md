# AGENTS.md — Codex adapter

This file is the Codex entrypoint for `<WIKI_DIR>`.

Mission in one sentence: this repository is the shared long-term memory for
projects, discussions, decisions, verified development experience, guardrails,
and reusable agent/team knowledge, so future Claude/Codex/GPT sessions start
with context instead of rediscovering it.

Read [WIKI_PROTOCOL.md](WIKI_PROTOCOL.md) first. That file is the canonical,
tool-neutral protocol for this knowledge library. Do not duplicate or reinterpret
the protocol here.

## Scope guardrail

- This repository is `<WIKI_DIR>`.
- Do not use any other repository as authority for this knowledge library unless
  the user explicitly asks for cross-repo comparison.
- If the current working directory is not this repository, stop and confirm the
  target before changing files.

## Codex operating rules

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

## Cross-model use

Besides editing as a peer, you (Codex) may be invoked **read-only** by Claude for a
fresh-model second opinion — sparring, peer review, or enacting any tool-neutral
role brief from `Wiki/roster/`. In that mode you advise; the human/Claude decides.
See [Wiki/knowledge/codex-cross-model-integration.md](Wiki/knowledge/codex-cross-model-integration.md).
