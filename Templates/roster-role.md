# Role: <name>

**Summary**: One line — the job this role does.

**Scope**: common (talent pool, reusable across projects) | specialized (one project).

**Layer / domain**: <Karpathy layer 1/2/3, cross-cutting, or a domain like trading>

**Tools (Claude)**: <tools the Claude adapter grants, e.g. Read, Grep, Glob, Bash>

**Status**: probation (adopted YYYY-MM-DD) → active after a verified win | active | deprecated — see [[skill-and-agent-probation-lifecycle]]

**Last updated**: YYYY-MM-DD

---

## When to hire

The trigger — what situation calls for this role.

## Operating brief

*Tool-neutral — Claude, Codex, or any agent enacting this role follows this section.*

The role's actual instructions: what it does, how it works, and its hard
boundaries. This is the canonical definition; tool agent files only point here.

## Hand-offs

- **From** / **To**: which role(s) precede and follow this one.

## Implementations (adapters)

- **Claude subagent**: `~/.claude/agents/<name>.md` (common) or
  `<repo>/.claude/agents/<name>.md` (specialized) — a thin adapter that points here.
- **Codex / other tools**: read this page via the project's `AGENTS.md` / team.

## Track record

*The librarian appends after a verified win: date · project · what worked / limit.*

- <entry>

## Related pages

- [[related-role-or-page]]
