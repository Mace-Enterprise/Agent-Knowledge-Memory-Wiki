---
name: retro
description: >-
  Run a team retrospective at a milestone or session end: read the outcome-log +
  recent diffs and turn finished work AND user corrections into concrete,
  owner-gated improvement deltas (process gate / skill edit / guardrail /
  role-brief / team-composition). Use when the user runs /retro, asks for a
  retrospective / "what did we learn", or criticizes a recurring behavior.
  Implements the team-coached-retrospective-loop methodology in the wiki.
---

# retro — team-coached retrospective

The continuous-improvement ritual. It does NOT make the model smarter; it improves
the **context** the team runs with next time (skills, guardrails, role briefs,
routing) — and only via durable artifacts that get **retrieved** at the right
moment. Canonical mechanics: wiki `experience/methodology/team-coached-retrospective-loop`.

## The outcome-log (the signal — feed it continuously)

The loop is worthless without a signal. During normal work, append one line to the
project's outcome-log (`<repo>/.memory/outcome-log.md`, or the wiki's
`Wiki/journal/outcome-log.md` for wiki work) whenever something is worth learning:

```
<date> · <type> · <one line: what happened> → <delta or "none">
```

Entry **types**: `outcome` (verify green/red), `review-catch` (a reviewer/peer caught
an error before it landed), `provenance`/`redaction` (a sourcing/secret slip),
**`user-correction`** (a behavior the user criticized — verbatim gist). User
corrections are first-class: capture them the moment they happen, not just at /retro.

## The ritual (when /retro is invoked)

1. **Read the signal** — the recent outcome-log entries + the relevant diffs/commits.
2. **Enact role-coach** (advisory; tools: Read/Grep/Glob). For each recurring or
   high-cost entry, propose a **concrete delta** — never "be more careful":
   - a process **gate** (a check added to a skill/workflow),
   - a **skill edit** (hand to skill-smith),
   - a **guardrail** (a rule that prevents the mistake class),
   - a **role-brief** change, or a **team-composition** tweak for next time.
3. **Independent voice** — have the Codex peer (read-only) review the proposed
   deltas (cross-model, so it isn't self-grading). See `codex-as-role` / `peer-review`.
4. **Owner gate** — present the deltas; the owner approves before anything lands.
   No autonomous self-rewrite of rules.
5. **Land + probation-track** — the librarian writes the approved deltas into the
   wiki/skills and adds a probation note: the delta is provisional until a later run
   confirms it reduced its target error class (see `skill-and-agent-probation-lifecycle`);
   otherwise revert. Record the result back in the outcome-log.

## Guardrails for the ritual itself

- **Concrete or nothing** — a delta must be a testable change to an artifact, not advice.
- **Retrieval, not prompt-bloat** — learnings live in recall-indexed pages, not the always-on prompt.
- **One incident ≠ a law** — mark a new rule provisional; confirm over repeats.
- **Independent review** — never let the same agent both do the work and grade it.
- **Stay on the primary thread** — the retro serves the work; don't let it become a rabbit hole.
