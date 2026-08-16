---
name: session-search
description: >-
  Search your own past sessions/transcripts to recall what was already done or
  decided, instead of re-deriving it. Use for "did we already do/discuss X?", or to
  find a prior decision, command, fix, or path across past conversations.
---

# Session search

Cheap full-text recall over past sessions — borrowed from Hermes' "search your own
history" idea, done lightweight with **ripgrep, no database**.

## Where
Claude session transcripts: `~/.claude/projects/<project-id>/*.jsonl`
(one JSONL per session).

## How (token-frugal — grep, then sample; never read a transcript in full)
1. `rg -l "<2–4 keywords>" ~/.claude/projects/*/` → which sessions mention it.
2. `rg -i -C2 "<keywords>" "<that .jsonl>"` → matching lines + a little context.
3. Read only the hits. The JSONL files are large — **never** open one whole.

## Order of recall
Check the **wiki first** (curated, durable memory). Use session-search for things
**not yet filed** there. If a recurring finding turns up, promote it into the wiki
(librarian) so next time it's a cheap wiki lookup, not a transcript scan.
