---
name: brainstorming
description: >-
  Turn a rough idea into a validated design BEFORE any code or spec — Socratic
  questions (one at a time), 2–3 explored alternatives, incremental sign-off. Use
  when the partner describes a feature/project idea and the shape isn't settled yet.
---

# Brainstorming → design

Refine an idea into a grounded design through questions and alternatives, validated
in small steps. Feeds the specifier (`/spec`) a settled starting point instead of a
vague prompt. *(Assimilated from obra/superpowers-skills; security-audited 2026-06-18 = clean; our wording.)*

**Status:** probation — promote to active after a verified win where this skill was used and helped (see the skill-and-agent-probation-lifecycle methodology).

## Process

1. **Understand** — check the current project state; ask **one question at a time**
   (prefer multiple-choice). Pin down purpose, constraints, success criteria.
2. **Explore** — propose **2–3 genuinely different approaches**; for each: core shape,
   trade-offs, complexity. Ask which resonates. Apply **YAGNI** ruthlessly.
3. **Design incrementally** — present in small sections (architecture, data flow,
   error handling, testing); after each ask "does this hold so far?"
4. **Hand off** — when approved, hand the design to the specifier; if implementation
   follows, set up an isolated workspace via the `using-git-worktrees` skill.

## Go backward when it helps

A new constraint or a gap surfacing in Phase 2/3 → return to Phase 1. Don't force
linear progress — flexibility beats rigid phase order.

## Discipline

One question per message in Phase 1; explore before settling; never skip straight to
a design the partner hasn't validated. Token-frugal: this is dialogue, not essays.
