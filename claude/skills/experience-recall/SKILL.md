---
name: experience-recall
description: >-
  Look up prior development learnings in the knowledge wiki before starting
  non-trivial work, so past patterns, gotchas, and verifier/environment recipes
  are reused instead of rediscovered. Use before designing or implementing a
  change, or when the user asks "have we solved this before / what do we know
  about X".
---

# Experience recall

Query the cross-project experience library before acting, so you reuse what the
team already learned.

## Preferred: the recall MCP

If the **`knowledge-recall`** MCP is registered, use it first — it's hybrid
(semantic + keyword) recall over the whole wiki and finds by *concept*, not just
exact words:
- `search_notes(query, mode="hybrid", limit=8)` → ranked pages with snippets.
- `read_note(path)` → the full page.

Then read the top 1–3 hits and cite them. If the MCP is **not** available, fall
back to the index-first + grep procedure below.

## Where to look (fallback when the MCP isn't registered)

The wiki at `<WIKI_DIR>` (canonical protocol:
`WIKI_PROTOCOL.md`):

- `Wiki/index.md` — the table of contents. Read this **first**; scan the relevant
  layers for the task.
- `Wiki/experience/<category>/*.md` — verified learnings (patterns / gotchas /
  verifiers / environments / methodology).
- `Wiki/knowledge/*.md` — source-distilled knowledge.
- `Wiki/adr/*.md` — past decisions (why we chose X); `Wiki/guardrails/*.md` — rules
  that constrain how to act; `Wiki/journal/sessions/*.md` — prior discussion/context
  (may be unverified — treat as leads, not facts).

## Procedure

1. Read `Wiki/index.md`. Identify candidate pages by title/description and by the
   current task's stack (e.g. dotnet/wpf) and category (a bug → gotchas; "how do I
   run/test this" → environments/verifiers).
2. Grep the experience folders for keywords from the task if the index is thin.
3. Read the 1–3 most relevant pages in full.
4. Apply what you find. **Cite the page** you used (e.g. "per
   [[ib-eventaggregator-ui-thread]]") so the user sees the library paying off.
5. If nothing relevant exists, say so briefly and proceed — and remember this gap
   may become a new experience page once the work is verified (see `/learn`).

Keep it lightweight: this is a read-only lookup, not a full audit.
