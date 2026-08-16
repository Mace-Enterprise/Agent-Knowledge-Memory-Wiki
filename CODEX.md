# Deploying Codex for cross-model review / sparring (agent guide)

**Audience: Claude (or another agent).** Enable Codex as a read-only second opinion
(sparring / peer review / role enactment) on a fresh machine. Idempotent.

> Codex also collaborates as a **file-based peer** (it reads `AGENTS.md` + the wiki and
> edits repos in parallel) — that needs no setup beyond the CLI + auth below.

## 0. Already working?
`codex --version` prints a version AND a read-only test call (step 3) returns text → done. Else continue.

## 1. Install / upgrade the CLI
```
npm i -g @openai/codex@latest
codex --version
```
Keep it **current** — an old CLI cannot use your account's current model (symptoms:
`model requires a newer Codex`, `model … not supported with a ChatGPT account`,
`unknown variant 'xhigh'`).

## 2. Authenticate
- ChatGPT account: `codex login` (opens a browser), **or**
- API key: set `OPENAI_API_KEY`.

## 3. Verify (read-only, cheap)
```
codex exec -s read-only "Reply in one sentence: confirm you can read this and are running read-only."
```
If it errors on model/reasoning, bypass config for the call with
`-c model_reasoning_effort=high` and/or `-m <a-model-your-account-supports>`, then fix
`~/.codex/config.toml` to a supported model.

## 4. Use it
- **Sparring** (ideas/plans): the `codex-sparring` skill.
- **Peer review** (a diff): the `peer-review` skill →
  `codex exec -C <repo> -s read-only "Peer-review <diff>; enact role-code-reviewer; return Strengths/Issues/verdict."`
- **Any read-only role as Codex**: the `codex-as-role` skill.

## Safety
- Always `-s read-only` for review/sparring — never `--full-auto` / `--dangerously-bypass-approvals-and-sandbox`.
- Fresh session → pass context + file paths in the prompt; **never secrets**.
- Costs credits → deliberate, confirm first.
