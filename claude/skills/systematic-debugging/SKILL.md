---
name: systematic-debugging
description: >-
  Find the root cause with a disciplined 4-phase process instead of shotgun fixes.
  Use when a bug is non-obvious, intermittent, or a quick fix didn't hold (e.g. a
  timezone/after-midnight calculation that's wrong only sometimes).
---

# Systematic debugging

Fix the **cause, not the symptom**. (Adapted discipline — our own wording.)

## Phase 1 — Reproduce
Get a reliable repro + the exact **expected vs actual**. No repro → make the smallest
input that triggers it first.

## Phase 2 — Isolate / trace
Narrow where behavior diverges: bisect, log at boundaries, check assumptions **with
evidence, not guesses**. One hypothesis at a time; test it before the next.
**Trace backward**: a bug usually surfaces deep in the call chain — follow it *up*
(what called this? what value was passed? where did that value originate?) to the
**original trigger**, not the place the error shows. To trace, instrument *before*
the dangerous operation (log inputs + a captured stack), not after it fails.

## Phase 3 — Fix at the root
Fix the actual cause. If you can't *name* the cause, you're not in Phase 3 yet — go
back to Phase 2. Where it pays, add **defense-in-depth** — validate at each layer so
the same bug becomes impossible, not just absent here.

## Phase 4 — Defend
Add a test/check that would have caught it (regression); confirm it fails-before /
passes-after.

## Discipline
No shotgun edits — change one thing, observe, keep or revert. **Show the result on
sample data**, not just "fixed" (see [[karpathy-loop-and-agent-discipline]]). If
stuck after 2–3 hypotheses, **report back** with what's ruled out — don't spiral.

## Verify before you claim it's fixed (iron rule)
**No completion claim without fresh verification evidence in this same turn.** Before
saying fixed/passing/done: identify the command that proves it → run it fully → read
the actual output (exit code, failure count) → only then state the result *with* that
evidence. "Should work", "looks right", a previous run, or a subagent's success report
are **not** evidence — re-run and check the diff. Skipping this is lying, not finishing.
