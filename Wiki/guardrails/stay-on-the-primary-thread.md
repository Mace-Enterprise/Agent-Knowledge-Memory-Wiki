# Guardrail — Stay on the primary thread

**Summary**: Hold the user's primary goal in front at all times. Details and tangents serve the goal and never replace it; spend effort proportional to a thing's impact on the goal.

**Trigger**: Owner feedback 2026-06-19 — "Hölzchen und Stöckchen" (chasing twig after twig) and "Alice im Wunderland Syndrom im Kaninchenbau" (falling down the rabbit hole): a side-detail had quietly become the primary focus. See [[outcome-log]].

**Scope**: All agent work — research, implementation, capture, and retros. Applies to any tool (Claude, Codex/GPT, subagents).

**Last updated**: 2026-06-20

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: single incident — dated in Trigger

---

## Rule

Keep the user's primary goal explicitly in front of the work:

- **Details serve the goal; they never replace it.** A sub-issue is in service of
  the goal, not a new goal.
- **Spend effort proportional to impact.** A small detail gets small effort; do
  not let a minor tangent absorb the session.
- **When a sub-issue balloons, name it and defer or ask** — do not silently make
  it the main work. State "this is a side-thread; do you want me to chase it now
  or after the main goal?".
- **If unsure what the goal is, default to the user's last stated goal** rather
  than an inferred or self-generated one.

## Why

Unbounded tangents burn budget and tokens, drift from what the user actually
asked for, and bury the deliverable. The cost of a rabbit hole is paid in the
primary goal not getting done.

## Note

The Claude-side feedback memory `stay-on-primary-thread` mirrors this guardrail
for the assistant; this page is the canonical, tool-neutral statement.

## Related pages

- [[no-unverified-assumptions]]
- [[outcome-log]]
- [[team-coached-retrospective-loop]]
- [[karpathy-loop-and-agent-discipline]]
