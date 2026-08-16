# Guardrail — Parallel agent collaboration

**Summary**: Claude, Codex/GPT, and any background agents must treat this
repository as a shared, concurrently edited worktree. They must coordinate by
checking current state, preserving each other's changes, and stopping when a
change would overwrite unclear work.

**Trigger**: The owner explicitly warned that Claude Code and Codex may work in
parallel and must cooperate without breaking each other's changes.

**Scope**: All Claude, Codex/GPT, subagent, and future-agent work on this
knowledge library and any project repo where multiple agents are active.

**Last updated**: 2026-06-18

**Enforcement**: advisory — no choke point; git status discipline only

**Justification**: owner directive — no incident needed

---

## Rule

Assume the worktree can change while you are working.

Before editing, an agent must:

- check `git status --short --untracked-files=all --branch`;
- read the target files in their current state;
- inspect relevant diffs when a target file is already modified;
- identify whether changes are its own, the human's, Claude's, Codex's, or
  unknown.

If ownership is unknown, treat the change as someone else's work and preserve it.

## Safe editing rules

- Use minimal, targeted patches.
- Prefer additive changes over rewrites when parallel work is active.
- Do not reformat, reorder, rename, or mass-edit unrelated content.
- Do not use `git restore`, `git reset`, forced checkout, or destructive cleanup
  unless the owner explicitly approves the exact scope.
- Do not stage, commit, push, or publish broad mixed changes while another agent
  is active unless the owner explicitly approves the scope.
- If the same file was changed by another agent, inspect the diff and merge
  compatibly; if unsure, stop and ask.
- If two agents disagree or the correct merge is unclear, capture the conflict
  as `Needs human confirmation` instead of guessing.

## Communication rules

Each agent should report:

- which files it changed;
- which parallel/unrelated changes it observed but did not touch;
- which checks it ran;
- which assumptions remain unverified;
- whether the work is committed, staged, or only in the worktree.

For larger work, use the [[role-orchestrator]] to sequence agents instead of
letting multiple agents edit the same files independently.

## Handoff rules

When handing off to another agent:

- state the exact branch/worktree state;
- list changed/untracked files;
- identify owned vs unrelated changes;
- name any files that must not be overwritten;
- point to the relevant protocol, guardrail, project, and roster pages.

## Stop conditions

Stop and ask the owner when:

- a requested change overlaps unknown work;
- a file has changed since it was last read;
- a commit would mix unrelated Claude/Codex/human changes;
- a cleanup operation would remove or rewrite another agent's work;
- a conflict requires interpretation rather than a mechanical merge.

## Related pages

- [[no-unverified-assumptions]]
- [[repo-boundary-llm-knowledge-library]]
- [[gpt-export-import-triage]]
- [[no-secrets-or-private-account-data]]
- [[role-orchestrator]]
- [[role-librarian]]
- [[role-wiki-critic]]

