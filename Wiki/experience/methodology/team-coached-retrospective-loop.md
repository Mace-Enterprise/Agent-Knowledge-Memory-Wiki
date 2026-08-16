# Team-coached retrospective loop

**Summary**: The mechanics of the continuous-improvement loop — an append-only outcome-log, a `/retro` ritual, a coach that proposes concrete deltas, an owner gate, and probation-tracked verification. Implements [[0002-team-coached-self-improvement-loop]].

**Type**: methodology

**Stacks**: any

**Provenance**: LLM Knowledge Library — process machinery; seeded from owner corrections 2026-06-19 (see [[outcome-log]]). Verified incrementally as deltas reduce their target error class.

**Confidence**: medium

**Last updated**: 2026-06-20

---

## Context

In-flight reviewers catch errors *before* work lands; this loop captures what
*finished* work and *user corrections* teach, and converts it into concrete
process/skill changes. Use it at a milestone or session end, after a green (or
red) verify, especially when a reviewer/peer caught something or the user
criticized a behavior.

## Insight / Recipe

The loop: **artifact → retrieval → outcome → retro → new artifact.** Each pass
turns signal into a durable, retrieval-indexed delta. Cross-link
[[karpathy-loop-and-agent-discipline]].

### 1. Outcome-log format (append-only)

The single source of signal: [[outcome-log]]. One entry per run/milestone:

```
date · type · task · verify (green/red) · what a reviewer/peer caught · what a memory/claim got wrong · USER-CORRECTION (verbatim gist of the criticized behavior)
```

Entry **types** (a behavioral correction is a first-class input, not an
afterthought):

- `outcome` — the run finished; verify result + notable result.
- `review-catch` — a reviewer/peer caught a defect before it landed.
- `provenance/redaction` — a sourcing or privacy slip (wrong source thread,
  near-secret).
- `user-correction` — the owner criticized a behavior (verbatim gist).

Keep entries to one line; the log is read, not admired.

### 2. /retro ritual

At a milestone/session end, the coach reads the recent outcome-log + diffs and
produces **concrete deltas**, each one of:

- a process gate, a skill/role-brief edit, a new/edited guardrail, or a
  team-composition tweak.

Never a vague "be more careful". A delta names the target error class and the
exact artifact it changes.

### 3. Who runs it

- **[[role-coach]]** runs the retro (advisory only).
- A **Codex peer** gives the independent, cross-model second opinion so the loop
  does not self-confirm.

### 4. Human-gate

Every process/skill change is approved by the owner before it lands. The coach
proposes; it never auto-applies.

### 5. Probation-track

Each delta is **provisional**. Confirm it actually reduced the target error class
over later runs (reuse [[skill-and-agent-probation-lifecycle]] — provisional →
confirmed, else revert). A delta that does not move the signal is reverted, not
kept "just in case".

## Evidence

Seeded from two real owner corrections on 2026-06-19 (rabbit-hole drift; a
mis-sourced GPT-import claim caught on owner challenge), each converted into a
named delta — see [[outcome-log]]. Confirmation accrues as those deltas
(guardrail [[stay-on-the-primary-thread]]; provenance-citation rule in
[[gpt-export-import-triage]]) demonstrably reduce repeats over later runs.

## Related pages

- [[0002-team-coached-self-improvement-loop]]
- [[role-coach]]
- [[outcome-log]]
- [[skill-and-agent-probation-lifecycle]]
- [[karpathy-loop-and-agent-discipline]]
- [[stay-on-the-primary-thread]]
- [[gpt-export-import-triage]]
