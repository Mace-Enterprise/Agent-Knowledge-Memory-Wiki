---
name: subagent-driven-development
description: >-
  Execute a plan by dispatching a FRESH subagent per task with a code-review gate
  between tasks — fresh context each time, issues caught early. Use when a plan has
  mostly independent tasks and you want continuous progress with quality gates.
---

# Subagent-driven development

Run a plan task-by-task: a fresh subagent implements each task, a reviewer checks it
before the next. Fresh context per task = no pollution; review between = early catch.
*(Assimilated from obra/superpowers-skills; security-audited 2026-06-18 = clean; our wording.)*

**Status:** probation — promote to active after a verified win where this skill was used and helped (see the skill-and-agent-probation-lifecycle methodology).

## Process

1. **Load plan** → a task list (one item per task).
2. **Per task**: dispatch a fresh implementer subagent — "implement exactly task N,
   write/keep tests, verify, commit, report what changed + test results." It returns a
   summary, not a transcript.
3. **Review**: dispatch the code-reviewer on that task's diff (base→head SHA). It
   returns Strengths / Issues (Critical·Important·Minor) / verdict.
4. **Apply feedback**: fix Critical now, Important before the next task; dispatch a fix
   subagent if needed (don't hand-fix — context pollution).
5. **Next task**; after all tasks, one **final review** of the whole change.

## Red flags

Never skip the review between tasks, proceed with unfixed Critical issues, or dispatch
**multiple implementer subagents in parallel on the same worktree** (they conflict —
use separate worktrees if truly parallel).

## Cost / when not to

Each subagent fan-out costs ~15× the tokens of a single pass — use this for genuinely
independent tasks, not tightly-coupled ones (do those manually) and not when the plan
still needs revision (brainstorm/spec first). See [[karpathy-loop-and-agent-discipline]].
For deterministic fan-out over many items, prefer the Workflow tool.
