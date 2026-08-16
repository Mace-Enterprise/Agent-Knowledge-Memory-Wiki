---
name: codex-as-role
description: >-
  Enact ANY tool-neutral read-only role brief AS Codex (a different model) for a
  fresh-model perspective — analyst, security-auditor, researcher, reviewer, etc.
  Read-only. Use for a deliberate cross-model take on a specific task.
---

# Codex-as-role

Our roster briefs are tool-neutral, so Codex can enact any of them. Use this when a
**read-only** role's job would benefit from a different model's view. Codex advises;
we decide.

## How

```bash
codex exec -C <repo> -s read-only "Enact the role brief in Wiki/roster/role-<ROLE>.md.
Task: <the specific task + the context Codex needs>.
Follow that brief's procedure and output format. Read-only — change nothing."
```

## Which roles

- **Read-only / advisory (the sweet spot):** analyst, code-reviewer, researcher,
  security, wiki-critic, verifier (as a checker). Safe with `-s read-only`.
- **Acting (implementer):** keep on Claude, or run Codex only deliberately with a
  write sandbox — **not** this skill's default.

## After

Relay the output + your take (Codex advises, we decide). For a concrete code diff,
prefer the dedicated `peer-review` skill.

## Notes

- Read-only; fresh session (pass context + paths); **never secrets**; costs credits → confirm first.
- Setup/gotchas: [[codex-cross-model-integration]].

**Status:** active (promoted from probation 2026-06-27 after a verified win — caught two real backtest bugs on ExampleApp Reentry that Claude had missed: optimistic same-bar-close fill + ex-post "nearest-to-day-low" selection leak). See [[codex-cross-model-integration]].
