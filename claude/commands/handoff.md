---
description: Save in-flight session state to <repo>/.memory/session-handoff.md for the next session (any tool)
---

Persist the current working state so the next session (Claude or Codex) can continue seamlessly.

1. Determine the repo root of the current work. If it has no `.memory/` directory, create it
   and ensure it is git-ignored (check `.gitignore`; add `.memory/` if missing).
2. Write (overwrite) `.memory/session-handoff.md` with exactly these sections, max ~40 lines:

```markdown
# Session handoff — <ISO date+time>
Status: unverified, in-flight — journal level

## Task
<what is being worked on and why — 1-3 lines>

## Progress
<what is done; mark explicitly what is verified vs. merely written>

## Decisions
<decisions taken this session, each with its reason>

## Next step
<the single concrete next action>

## Open questions for the owner
<anything blocked on the owner; "none" if none>
```

3. Content rules: facts only, no praise, no prose padding. Everything here is
   journal-level (unverified) by definition — never copy it into the wiki's
   knowledge/experience layers without a green verify.
4. Confirm to the user in one line that the handoff is saved and where.
