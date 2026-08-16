---
name: peer-review
description: >-
  Get a cross-model PEER REVIEW of a concrete change/diff from Codex (a different
  model), read-only. Use before merging a non-trivial change when an outside,
  blind-spot-catching review adds value. Costs the user's Codex credits.
---

# Peer review (cross-model, via Codex)

A different model reviews a concrete diff as a peer reviewer — catches what a
same-model review misses. Codex **enacts our `role-code-reviewer` brief**, so the
output matches our own review format. Read-only; Codex advises, we decide.

## When

Before merging a non-trivial change/PR, or for an independent check on risky code.
Not on every commit (costs credits, fresh session). Confirm first unless the user
said "peer-review it".

## How

```bash
codex exec -C <repo> -s read-only "PEER REVIEW. Enact the reviewer brief in Wiki/roster/role-code-reviewer.md.
Review this change: <git diff base..head, or name the files/SHAs>.
Return: Strengths · Issues (Critical/Important/Minor, each with file:line + why) · Verdict (ship / fix-first / reject).
Be concrete. Read-only — change nothing."
```
Give it the diff or the base/head SHAs + changed files; `-C <repo>` lets it read the surrounding code.

## After

Relay the review, then add your take: which issues are real, which miss our context.
Fix Critical before merge. **Codex advises; we decide.**

## Notes

- Read-only only — never a write sandbox for review.
- Fresh session → pass context in the prompt; **never feed it secrets**.
- Setup + gotchas (upgrade CLI if model errors): see [[codex-cross-model-integration]].

**Status:** probation — promote to active after a verified win.
