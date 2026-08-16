# ADR 0002: Team-coached self-improvement loop

**Summary**: Adopt a team-level retrospective/continuous-improvement loop that turns finished work and user corrections into concrete, human-gated process/skill deltas, verified over time.

**Status**: accepted

**Date**: 2026-06-20

**Deciders**: Human owner with the agent team (coach + Codex peer).

**Last updated**: 2026-06-20

---

## Context

In-flight reviewers already catch errors before work lands: [[role-code-reviewer]]
challenges the diff, [[role-wiki-critic]] audits the wiki, and a Codex peer gives a
cross-model second opinion. The [[skill-and-agent-probation-lifecycle]] handles
trust (new skills/roles earn "active" only after a verified win).

What is missing is a **signal-driven loop** that turns *finished* work and *user
corrections* into concrete process or skill deltas. Nothing today closes the gap
between "a mistake happened / the user criticized a behavior" and "the operating
brief, guardrail, or team composition changed to prevent it next time". Lessons
evaporate in chat history instead of compounding.

## Decision

Add a team-coached continuous-improvement loop with five parts:

- **(a) Append-only outcome-log** — one entry per run/milestone capturing the
  outcome signal (see [[outcome-log]] + [[team-coached-retrospective-loop]]).
- **(b) /retro ritual** — at a milestone/session end, read the recent outcome-log
  and diffs and produce concrete deltas (never "be more careful").
- **(c) role-coach** — an advisory [[role-coach]] that proposes deltas and
  team-composition tweaks from the log and role track records.
- **(d) Human-gated application** — every process/skill change is owner-approved
  before it lands.
- **(e) Probation-tracked verification** — each delta is provisional and must be
  shown to reduce its target error class over later runs, reusing
  [[skill-and-agent-probation-lifecycle]]; otherwise it is reverted.

## Consequences

- Needs a real **outcome signal** to drive it — the outcome-log must actually be
  appended, or the coach has nothing to read.
- Deltas live in **retrieval** (recall-indexed wiki pages), not the always-on
  system prompt, to avoid context bloat.
- The **Codex peer** supplies an independent, cross-model voice so the loop does
  not self-confirm.
- Adds a lightweight ritual cost; kept tight on purpose (the loop's point is
  anti-vibes, anti-rabbit-hole — see [[karpathy-loop-and-agent-discipline]]).

## Alternatives considered

- **Per-agent self-review** — rejected: an agent grading its own work is
  sycophantic and misses its own blind spots.
- **Autonomous self-rewrite** (agent edits its own briefs unattended) — rejected:
  invites reward-hacking and silent drift; changes to process/skills must be
  owner-gated.
- **Dump all learnings into the always-on prompt** — rejected: context bloat;
  learnings belong in retrieval, surfaced on demand.

## Related pages

- [[team-coached-retrospective-loop]]
- [[role-coach]]
- [[outcome-log]]
- [[skill-and-agent-probation-lifecycle]]
- [[karpathy-loop-and-agent-discipline]]
