# Guardrail — secure repositories to a Git remote

**Summary**: A repo isn't safe until its work is **committed AND pushed to a remote**.
Local-only commits are not a backup — a disk loss wipes them. Treat pushing as part of
"done", not an optional follow-up.

**Trigger**: A freshly built repo (`sec-edgar-mcp`) was left `git init`'d locally with no
remote, and pushing was framed as an optional afterthought; separately the wiki had 16
committed-but-unpushed commits sitting unsecured until an explicit local/Git reconciliation
caught them. (2026-07-01)

**Scope**: Every repo we own or actively work in under `<SOURCES_DIR>`. Applies cross-tool
(Claude and Codex).

**Last updated**: 2026-07-01

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: needs-review — trigger present but neither dated nor an owner directive

---

## Rule

When work lands in a repo, the unit of work is **not done** until it is:
1. **committed** with a clear message, and
2. **pushed** to a remote (so it's backed up off the local disk).

If a repo has **no remote**, that's a gap to close, not to ignore: **ask** the owner for
visibility (default **private** for personal tooling) and host, then create the remote and
push. Do not leave a new repo local-only and move on.

## Checks before acting

- After building/changing a repo: is HEAD pushed? (`git log @{u}..` empty, or `git status -sb` shows nothing "ahead").
- Does the repo have a remote at all? (`git remote -v`). If not → ask + create + push.
- Before creating/pushing a **new** remote: confirm **private vs public** (creating/pushing is outward-facing and hard to reverse) and that no secrets/keys/data are staged — see [[no-secrets-or-private-account-data]].
- Periodic reconciliation across `<SOURCES_DIR>`: flag dirty trees, no-remote repos, and unpushed commits.

## Escalation

- **Only auto-push our own session work.** Pre-existing dirty working trees or **other**
  unpushed commits (parallel-agent / owner WIP, data files, large CSVs) are the owner's
  call — report them, don't commit or push them unasked.
- If a push would upload large data files or anything possibly sensitive, **stop and ask**
  (show what would be uploaded) rather than pushing blindly.

## Related pages

- [[no-secrets-or-private-account-data]] — never push secrets/keys/private data
- [[parallel-agent-collaboration]] — don't clobber concurrent/others' work
- [[machinery-sync-engine-template]] — a sibling "do X in the same change" gate
