# Guardrail — storage location is not project identity

**Summary**: A file living in another project's folder never makes it that project's
business. Every project gets its own working directory and a **stable id** that survives
renaming and moving; cross-project contamination and lost projects are detected by
`project-boundary-check.py`, not by hope.

**Trigger**: 2026-08-16 — homelab work had been running out of a trading project's working
directory for weeks, because homelab had no directory of its own. Its session state and
device facts sat in two foreign `.memory/` folders. Nobody noticed, because nothing was
looking. The owner's correction was blunt and correct: *that must not happen*, and *the
reviewer/auditor has to check for it too*.

**Scope**: every repository under the projects root; the reviewer, auditor and wiki-critic
roles.

**Enforcement**: audit — `project-boundary-check.py` (engine repo), run from the wiki
pre-commit hook and standalone; emits guardrail events

**Justification**: single incident, dated — 2026-08-16, three misfiled files recovered from
two foreign repos

**Last updated**: 2026-08-16

---

## Rule

1. **Every project has its own working directory.** A project without one does its work
   somewhere else, and its memory lands in a foreign repo. This is the root cause, not
   sloppiness — homelab had a wiki profile, its own guardrails and topology pages, and no
   directory.
2. **The code may live elsewhere.** A working directory holds the project's *contracts and
   memory*; it does not have to hold the source. Analysis contexts stay where the app loads
   them from, and still are separate projects.
3. **Every project carries a stable id** in `.project-id`. The id never changes — not on
   rename, not on move, not when the project itself is renamed. Paths change; identities
   must not, or every cross-repo reference rots silently.
4. **References resolve through the id**, and the registry maps id → current path. A moved
   project is *found again* by walking the disk for its id, and the registry is corrected
   (`--fix`) instead of the reference simply breaking.
5. **Markers must be unmistakable.** The check flags a memory file that speaks another
   project's language and none of its own. Generic words ("overlay", "guardrail", "config")
   produce false alarms, and a checker that cries wolf gets switched off — the first version
   did exactly that and had to be sharpened.

## Checks before acting

- Before working on a project: am I **in its directory**? If it has none, that is the first
  thing to fix, before any other work.
- Before writing to `.memory/`: does this fact belong to **this** project, or is it here
  only because I happened to be in this directory?
- Reviewer / auditor: run `project-boundary-check.py`. It reports contamination, projects
  without a working directory, projects that moved, and projects with no id at all.

## Escalation

A `LOST` result — an id that exists in the registry but nowhere on disk — means a project
was deleted or moved outside the scan root. Stop and ask the owner; do not silently drop
the registry entry, because that is how a project's history disappears.

## Related pages

- [[0006-where-durable-project-knowledge-lives]]
- [[repo-boundary-llm-knowledge-library]]
- [[publish-gate-must-fail-closed]]
- [[stay-on-the-primary-thread]]
