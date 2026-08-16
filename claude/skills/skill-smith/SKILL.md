---
name: skill-smith
description: >-
  Create and improve our own skills — a verified, token-frugal discipline. Use
  when a repeated workflow should become a reusable skill, or to refine an
  existing skill after a better way proved out. Gates on a real success; keeps
  skills lazily loaded (progressive disclosure).
---

# Skill-Smith

You author and refine our skills the way the librarian files experience: **only
after it proved out**. (Adapts Superpowers' `writing-skills` + Hermes' skill-creation
trigger — rewritten in our own words, never pasted.)

## When to create a skill (trigger)

- After a **successful complex task** (≈5+ tool calls), or after **recovering from a
  dead-end/error** — capture the working path so it isn't rediscovered.
- Do NOT create a skill for a one-off or an unverified hunch.

## How

1. One line: what must this skill make the agent do?
2. Write `SKILL.md`: a **lean description** (for triggering) + the **minimal steps**.
3. Pressure-test (TDD-for-docs): would a *fresh* agent follow it correctly? Imagine
   the failing case and close the loophole/ambiguity.

## Token-frugal: progressive disclosure (hard rule)

Keep `SKILL.md` **short**. Put long detail/examples/scripts in **separate files the
skill references**, loaded only when needed (list → view → view-detail). **Never
preload everything** (the mistake Superpowers' issue #190 documents).

## Verify before persist — probation lifecycle

A new (or newly adopted/harvested) skill starts on **probation**: usable but flagged
unproven via a `**Status:** probation` line. It is promoted to **active** only after a
**verified win** where it was actually used and helped; demoted/retired if it produced
a wrong result, duplicated another, or sat unused. Note provenance (what it was earned
on). The librarian records each transition automatically in the post-verify capture —
see the `skill-and-agent-probation-lifecycle` methodology. Improving an existing skill
uses the same gate: change only after a verified better way emerged, and record it.

## Anti-explosion

Periodically review skills: merge near-duplicates, retire unused. Fewer, sharper
skills beat many.

## Security

When adapting third-party skill wording, **rewrite in our own words** — never paste
verbatim (prompt-injection surface). See [[karpathy-loop-and-agent-discipline]].
