# Codex cross-model integration

**Summary**: How Codex works alongside Claude here — as a **file-based peer** on the repo, and **on-demand via its CLI (read-only)** for a fresh-model second opinion: sparring, peer review, or enacting any tool-neutral role. Codex advises; Claude/owner decides.

**Sources**: built + verified 2026-06-19 (Codex CLI 0.141, ChatGPT account, model `gpt-5.5`); its first sparring run caught two real wiki inconsistencies.

**Last updated**: 2026-06-19

---

## Two modes

1. **Peer on the repo (file-based).** Codex edits the same repos in parallel, reading the same `AGENTS.md` + this wiki as Claude. No bridge/MCP — the shared markdown **is** the contract. Coordinate via [[parallel-agent-collaboration]].
2. **On-demand via CLI (read-only, fresh model).** `codex exec -C <repo> -s read-only "..."` runs a one-shot Codex session that reads the repo and returns text:
   - **Sparring** on ideas/plans/decisions → the `codex-sparring` skill.
   - **Peer review** of a concrete diff → the `peer-review` skill.
   - **Enact any read-only role** as Codex → the `codex-as-role` skill (analyst, security-auditor, researcher, reviewer, …).

   A different model catches blind spots a same-model review misses. **Codex advises; we decide.**

## Why read-only is the sweet spot

`-s read-only` lets Codex read code / run read commands but **never modify**. Advisory roles (review / analyse / research / audit / verify-checks) fit perfectly. Acting roles (implementer) stay on Claude unless deliberately run with a write sandbox.

## Setup / bootstrap

Codex must be installed **and current**. Fresh-machine steps live in the engine template's **`CODEX.md`** (agent-followable). Short form: `npm i -g @openai/codex@latest` → `codex login` → verify with a read-only call.

## Gotchas (learned 2026-06-19)

- **The CLI version must match your account's model.** A stale CLI fails with `model requires a newer Codex`, `model … not supported with a ChatGPT account`, or `unknown variant 'xhigh'`. Fix: upgrade the CLI.
- One-off bypass without editing `~/.codex/config.toml`: `-c model_reasoning_effort=high` and/or `-m <supported-model>`.
- Each call is a **fresh session** (no memory of the Claude chat) → put context + file paths in the prompt; `-C <repo>` gives it the code. **Never feed it secrets.**
- Costs the owner's Codex credits → deliberate use; confirm first.

## Related pages

- [[parallel-agent-collaboration]]
- [[agent-orchestration-options]]
- [[role-code-reviewer]]
