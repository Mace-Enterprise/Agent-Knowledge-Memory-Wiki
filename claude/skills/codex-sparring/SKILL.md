---
name: codex-sparring
description: >-
  Get a second opinion from Codex (a different model) on an idea, plan, or code
  question — adversarial sparring to catch blind spots a same-model review misses.
  Use deliberately for weighty decisions. Read-only; costs the user's Codex credits.
---

# Codex sparring

Invoke the local **Codex CLI** as an independent sparring partner: a *different model*
challenges the idea/plan/code and we weigh its feedback. Model diversity catches blind
spots Claude reviewing Claude won't.

## When to use

Deliberately, for **specific** weighty calls — a design/architecture decision, a risky
plan, or a "is this code right?" question. **Not** on every step: each call costs the
user's Codex/OpenAI credits and runs a fresh session. Confirm before spending credits
unless the user already said "ask Codex".

## How — Codex MUST get context + code access

Codex starts a **fresh session with no memory of our chat**, so the call must carry the
context. For **code questions, run it inside the repo** so it can read `AGENTS.md` + the
actual code:

```bash
codex exec -C <repo-dir> -s read-only "SPARRING: <idea/plan/decision, stated concisely>.
Context Codex needs: <facts, constraints, what we already decided>.
Code is in this repo — read <relevant paths> as needed.
Play devil's advocate: challenge assumptions, find flaws/risks/blind spots, propose
alternatives. Be concrete and critical — don't just agree. Read-only: change nothing."
```

- `-C <repo-dir>` → Codex's working root = the repo, so it **sees `AGENTS.md` + the code**.
- `-s read-only` → sandbox: Codex can **read** files / run read commands but **cannot modify** anything.
- Put the real question + enough context in the prompt; name specific files/paths for code questions. Capture stdout and relay it.

## After

Relay Codex's feedback, then add your own take: where it's right, where it's
wrong or missing our context, and what (if anything) we change. **Codex advises; we decide.**

## Guardrails

- Read-only only — never `--full-auto` or `--dangerously-bypass-approvals-and-sandbox` for sparring.
- Costs the user's credits → deliberate, confirm first.
- Fresh external session → never assume it knows prior chat; **never feed it secrets**.

## Troubleshooting

- **`unknown variant 'xhigh'`, `model requires a newer Codex`, or `model … not supported with a ChatGPT account`** → the Codex CLI is behind your account/config. Fix: upgrade it (`npm i -g @openai/codex@latest`), then the config defaults work. One-off bypass without editing config: add `-c model_reasoning_effort=high` and/or `-m <supported-model>`.
- Verified on Codex CLI **0.141** + a ChatGPT account (model `gpt-5.5`). Output ≈70k tokens for a high-effort read+critique of ~6 pages.

**Status:** active (promoted 2026-06-19 — first real sparring run read the wiki read-only and returned a sharp, actionable critique that caught two real inconsistencies). See [[skill-and-agent-probation-lifecycle]].
