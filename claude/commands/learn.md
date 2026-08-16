---
description: Capture reusable learnings from this session into the knowledge wiki
argument-hint: "[optional: what to focus the capture on]"
---

Capture what was learned in this session into the knowledge wiki, using the
**experience-capture** skill.

Focus (optional): $ARGUMENTS

Rules:
- Gate on a **green verify** — only file learnings that were actually proven this
  session. If nothing was verified or nothing reusable emerged, say so and stop.
- Separate reusable cross-project learnings (→ wiki `experience/`) from volatile
  project-specific facts (→ per-project memory). Do not put project-specific facts
  in the wiki.
- Dispatch the **librarian** agent to do the write: dedup/merge against existing
  pages, fill the experience-page template, update `index.md` + `log.md`, and
  git-commit in the wiki.
- Report what was filed: page paths, new vs merged, and the commit hash.
