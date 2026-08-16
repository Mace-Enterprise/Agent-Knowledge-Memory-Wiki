---
name: using-git-worktrees
description: >-
  Create an isolated git worktree for feature work — smart directory choice, a
  .gitignore safety check, and a clean test baseline. Use before parallel/independent
  work that should not disturb the current workspace.
---

# Using git worktrees

Isolated workspaces sharing one repo — work multiple branches at once without
switching. *(Assimilated from obra/superpowers-skills; security-audited 2026-06-18 = clean; our wording.)*

**Status:** probation — promote to active after a verified win where this skill was used and helped (see the skill-and-agent-probation-lifecycle methodology).

## Directory choice (priority order)

1. Existing `.worktrees/` (preferred) or `worktrees/` → use it.
2. A preference in `CLAUDE.md`/`AGENTS.md` → use it without asking.
3. Otherwise **ask** the owner: project-local `.worktrees/` vs a global location.

## Safety (do before creating)

- **Project-local dir must be git-ignored.** Check `.gitignore` for the pattern; if
  missing, add it and commit **first** — otherwise the worktree contents pollute git.

## Create

```bash
proj=$(basename "$(git rev-parse --show-toplevel)")
git worktree add ".worktrees/<branch>" -b "<branch>"
cd ".worktrees/<branch>"
```
Then **auto-detect and run setup** (npm install / dotnet restore / pip install / etc.)
and **verify a clean test baseline** before implementing. If the baseline fails,
report it and ask before proceeding — you can't tell new bugs from pre-existing ones.

## Report

`Worktree ready at <path> · baseline <N tests, 0 fail> · ready to implement <feature>.`

## Notes

Pairs with the `subagent-driven-development` skill (work happens in the worktree) and
the Workflow tool's `isolation: "worktree"` (same idea for parallel agents). Clean up
the worktree when the branch is merged/abandoned.
