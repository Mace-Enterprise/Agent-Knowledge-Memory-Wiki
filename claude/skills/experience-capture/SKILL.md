---
name: experience-capture
description: >-
  Capture reusable development learnings from the current session into the
  knowledge wiki, after work has passed its verifier. Use when the user runs
  /learn, or at the end of a verified task to file what was learned. Gates on a
  green verify, then dispatches the librarian agent to write and commit.
---

# Experience capture

Turn what this session produced into durable, reusable knowledge — but only what
was actually proven.

## Gate first

Capture **only after a green verify** (tests/build/checks passed, or a concrete
verified before/after). If nothing was verified, or nothing reusable emerged, do
nothing and say so. Never record unverified guesses.

## What counts as reusable

A learning worth filing generalizes beyond this one repo: a reusable **pattern**,
a **gotcha** (trap + how to avoid), a **verifier** recipe (how to check a stack),
an **environment** recipe (how to run/observe a stack), or a **methodology**
insight → `Wiki/experience/`. Volatile, single-repo facts (a path, current bug
state, a queued task) go to that project's per-project memory — not the wiki.

If something valuable emerged but isn't verified yet (an open question, a
correction, in-progress reasoning), it belongs in `Wiki/journal/sessions/`, not
experience. The **librarian** routes per `WIKI_PROTOCOL.md` (experience / knowledge
/ journal / adr / guardrails).

## Procedure

1. Briefly list the candidate learnings you see in the session and which look
   reusable vs project-specific.
2. **Dedupe gate (before any write):** for each candidate, run the
   `knowledge-recall` MCP's `search_notes` first. If an existing page already
   covers the topic, the instruction to the librarian is **extend that page**,
   not create a new one — pass the hit paths along. Only genuinely uncovered
   learnings become new pages. (Without this gate the wiki grows semantic
   duplicates and recall quality decays.)
3. **Dispatch the `librarian` agent** to do the write. Give it: the candidates,
   the evidence (which verifier step passed), the project + commit/PR for
   provenance, **and which skills/roles were actually used** in this verified win.
   The librarian follows the wiki protocol — dedup/merge, fill the experience-page
   template, update `index.md` + `log.md`, and git-commit. It also runs the
   **probation lifecycle**: any skill/role used here that is still on probation gets
   promoted to active (status flip + track-record + log) — automatically, per the
   skill-and-agent-probation-lifecycle methodology.
3. Relay what the librarian filed (page paths, new vs merged, commit hash), or why
   nothing was captured.
4. **Keep recall current**: if anything was written to the wiki, refresh the recall
   index so semantic search isn't stale — call the `knowledge-recall` MCP's
   `reindex` tool (or run `python server.py index` in
   `<RECALL_MCP_DIR>`). It's incremental (content-hash), so it only
   re-embeds changed pages — cheap. (Skip if nothing was written.)

This skill is the shared entrypoint for both the `/learn` command and the
session-end (Stop hook) capture pass.
