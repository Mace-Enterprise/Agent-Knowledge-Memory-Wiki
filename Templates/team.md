# Team — <project name>

**Summary**: This project's agent team — which roles from the global pool it hires,
plus its own domain roles. Read by Claude and Codex.

The global talent pool lives in the knowledge wiki
(`<WIKI_DIR>/Wiki/roster/`). This file is the project's
*composition* of that pool plus domain-specific members.

## Hired from the pool

- orchestrator — plans the team and dispatch order.
- specifier / implementer / verifier — the Karpathy loop.
- code-reviewer — diff quality before merge.
- librarian — files verified learnings to the wiki.
- _(drop any the project doesn't need)_

## Domain roles (project-specific)

Defined for this repo. Claude implementations live in `.claude/agents/`.

- **<domain-role-name>** — <what it does, when to hire>. Implemented by
  `.claude/agents/<name>.md`.

## Workflow

How this team runs a change (e.g. orchestrator → specifier → implementer →
verifier → code-reviewer → librarian). Note any gates (green verify required) and
where the user approves.
