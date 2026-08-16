---
name: condition-based-waiting
description: >-
  Kill flaky async tests/automation by waiting for the actual condition instead of a
  guessed sleep/timeout. Use when tests have arbitrary delays, race conditions, or
  pass/fail inconsistently (especially under load or in CI).
---

# Condition-based waiting

Arbitrary delays guess at timing → races that pass locally and fail in CI. Wait for
the **condition you actually care about**, not a duration. *(Assimilated from
obra/superpowers-skills; security-audited 2026-06-18 = clean; our wording.)*

**Status:** probation — promote to active after a verified win where this skill was used and helped (see the skill-and-agent-probation-lifecycle methodology).

## Pattern

```
# ❌ guess
sleep(50); assert getResult() != None
# ✅ condition
waitFor(lambda: getResult() is not None, timeout=5s); assert getResult() != None
```

A generic poller: loop calling the predicate (fresh each iteration), return on truthy,
**throw on timeout with a clear message**, poll ~10ms (not 1ms — that burns CPU).
Wait for: an event present, a state value, a count reached, a file existing, a
compound condition.

## Common mistakes

- **No timeout** → infinite hang. Always bound it with a descriptive error.
- **Polling too fast** → wasted CPU. ~10ms is plenty.
- **Caching state before the loop** → stale. Call the getter *inside* the loop.

## When a fixed delay IS correct

Only for genuinely timed behavior (debounce/throttle): first `waitFor` the triggering
condition, then wait a **known** interval, with a comment explaining why. Never a bare
guess.
