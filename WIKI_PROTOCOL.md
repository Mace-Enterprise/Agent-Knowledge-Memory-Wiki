# WIKI_PROTOCOL — shared memory protocol

**Summary**: Canonical, tool-neutral operating protocol for the knowledge
library. Claude, Codex/GPT, and future agents use this file as the shared source
of truth.

**Last updated**: 2026-08-13 (new memory-layer convention:
[Historical (retained, no longer current)](#historical-retained-no-longer-current)
— a `Status: historical` + `Valid:` date-range + "why kept" modifier on a normal
page, not a new folder)

---

## Purpose

This repository is a durable memory system for projects, research, decisions,
development experience, and reusable agent/team knowledge.

The goal is compounding memory:

- useful discussion is captured instead of disappearing in chat history;
- raw sources are preserved separately from interpreted knowledge;
- verified development learnings are promoted into reusable experience pages;
- decisions and rejected alternatives remain visible;
- Claude and Codex/GPT can work from the same protocol.

## If you are an agent opening this repository

Treat this repository as the owner's cross-project memory and coordination layer.
It is not just a folder of notes and it is not a normal application source repo.

This is the **cross-project** layer. Each project repo also keeps its **own** volatile,
cross-tool working memory in `<repo>/.memory/` (git-ignored, referenced from that repo's
`AGENTS.md`, read by Claude *and* Codex, and indexed by the recall MCP alongside this wiki
via `RECALL_EXTRA_DIRS`). Durable/reusable knowledge lives **here**; repo-only volatile
facts live **there**; this wiki's project profile (`Wiki/projects/<project>.md`) links to it.

When Claude, Codex/GPT, or another agent opens it, the expected interpretation is:

- **Understand context quickly**: read the index, protocol, and relevant pages so
  you inherit prior discussions, decisions, constraints, and verified lessons.
- **Avoid repeating old work**: use journals, ADRs, guardrails, experience pages,
  and knowledge pages before re-researching or re-deciding a topic.
- **Preserve important thinking**: when a session contains useful context,
  corrections, decisions, or unresolved questions, capture it before it
  disappears in chat history.
- **Promote only when earned**: move material from journal to knowledge,
  experience, ADR, or guardrail only when it has the right evidence or decision
  status.
- **Work across tools**: write in plain Markdown so Claude, Codex/GPT, and future
  agents can all read and improve the same memory.

The first read path for a new agent is:

1. `AGENTS.md` or `Claude.md`, depending on the tool.
2. This `WIKI_PROTOCOL.md`.
3. `Wiki/index.md`.
4. Any linked pages relevant to the task.
5. `Wiki/log.md` when the recent evolution of the wiki matters.

The key outcome is not "more notes". The outcome is compounding operational
memory: future agents should understand what happened, why decisions were made,
what has already been verified, what must not be repeated, and what still needs
the human's decision.

## Repository scope

The target repository is:

`<WIKI_DIR>`

Treat only this repository as authority for this knowledge library. If a tool
starts in a different working directory, verify the path before reading or
writing.

## Directory map

```text
Raw/                       immutable human-curated sources
Raw/Projects/              source-level project descriptions
Templates/                 page templates used by agents
Wiki/index.md              table of contents and navigation entrypoint
Wiki/log.md                append-only operation log
Wiki/projects/             distilled agent-ready project profiles
Wiki/knowledge/            distilled knowledge from Raw/ or cited research
Wiki/experience/           verified reusable development learnings
  patterns/
  gotchas/
  verifiers/
  environments/
  methodology/
Wiki/journal/sessions/     captured discussion and in-progress reasoning
Wiki/adr/                  architecture/decision records
Wiki/guardrails/           safety, scope, privacy, and operating constraints
Wiki/roster/               reusable agent-role talent pool
```

Use the actual casing above. Do not invent parallel lowercase folders.

## Memory layers

### Raw

`Raw/` contains source material supplied or curated by the human. **While the raw
format is still being designed, a raw source may be restructured or translated.**
Once a source's format is finalized, treat it as **immutable** — do not rewrite or
"clean up" finalized raw sources. The distilled, agent-ready version always lives
in `Wiki/projects/`, `Wiki/knowledge/`, etc., never by overwriting the raw source.
See [[2026-06-18-raw-format-design-phase]].

### Projects

Use `Raw/Projects/` for source-level project descriptions and `Wiki/projects/`
for distilled, agent-ready project profiles.

Keep distinct projects distinct. A project page owns its goal, scope, source
context, tools, team, current state, and open questions. Similar lessons across
projects should be linked through shared `Wiki/knowledge/` or `Wiki/experience/`
pages, not copied into each project.

### Journal

Use `Wiki/journal/sessions/` for valuable discussion, working context, partial
reasoning, corrections, and unresolved questions. Journal pages may contain
unverified claims, but they must label their status clearly.

Journal first when losing context would hurt future work.

### Knowledge

Use `Wiki/knowledge/` for distilled, reusable knowledge. A knowledge page should
cite raw sources, web research, or journal/ADR context where the claim came
from. Claims without evidence are marked as needing verification.

### Experience

Use `Wiki/experience/` for reusable development learnings earned by a verified
change. An experience page needs concrete provenance: project/repo, commit/PR
or working context, verifier command/result, date, and confidence.

Never promote a guess into experience.

### ADRs / decisions

Use `Wiki/adr/` when the team chooses a direction that affects future work.
Record context, decision, consequences, alternatives considered, and status.

### Guardrails

Use `Wiki/guardrails/` for rules that prevent repeated mistakes: scope
boundaries, privacy constraints, secret-handling, and process gates.

### Tombstones (negative knowledge)

A **tombstone** records a refuted approach so it is not silently re-explored.
It is not a layer of its own: cross-project refutations live in `Wiki/knowledge/`
or `Wiki/experience/`, project-specific ones in that repo's `.memory/`. Frontmatter
`Type: tombstone` plus a short contract block: `CLAIM` (what is dead and under which
assumptions), scope, `EVIDENCE`, and a **mandatory `REOPEN_IF`** — the concrete
conditions under which the idea may be retried. A tombstone without reopen
conditions is an innovation ban, not knowledge. When a killed idea is proposed
again, recall should surface its tombstone prominently. Template:
`Templates/tombstone.md`.

### Historical (retained, no longer current)

Some facts stop being true but stay worth keeping: they explain old logs, old
decisions, or a vendor/provider behaviour that can recur with different hardware.
**This is not a new layer and not a new folder.** Like tombstones, it is a
**status convention** on a page in its normal layer (usually `Wiki/knowledge/`,
sometimes `Wiki/experience/`). Deleting such a page loses evidence; leaving it
unmarked makes the wiki lie about the present.

Mark it with three things, all mandatory:

- `**Status**: historical` in the header block, plus a first line that says
  plainly **what is no longer current and since when**;
- `**Valid**: YYYY-MM-DD … YYYY-MM-DD` — the explicit date range the page
  describes (open-ended `… (Ende offen)` is allowed only while the range is
  genuinely still running);
- a `## Why this is kept` section — one paragraph naming the future reader who
  would need it (e.g. "it explains two weeks of throughput logs" / "the same
  provider-side behaviour can recur with a different box"). A historical page
  without a stated reason to keep it is clutter, not memory.

Rules of use:

- **Never silently rewrite a historical page into the present tense.** When the
  situation changes again, write the new state where it belongs and link back.
- **A whole page** goes historical when its subject is gone; **a section** inside
  a still-current page is marked inline instead:
  `> ⚠️ **HISTORICAL since YYYY-MM-DD.** …` with a pointer to the successor
  (precedent: the Omada sections in [[raspberry-pi-firewall]]).
- Index it under **`Historical / interesting`** in `Wiki/index.md`, not only in
  its topic block, so a reader browsing the current state does not trip over it.
- Distinguish from a **tombstone**: a tombstone kills an *approach* and must
  carry `REOPEN_IF`; a historical page preserves a *fact that was true then*.
  A historical page needs no reopen condition — it needs a date range.
- No separate template: it is a status modifier on the page's normal template.

### Roster and teams

`Wiki/roster/` is the generic talent pool. Each project composes its own team
from that pool plus domain-specific roles, ideally in a project-local `TEAM.md`.

Each role page is the **canonical, tool-neutral operating brief** for that role.
Tool-specific agent files (`~/.claude/agents/<role>.md` for common roles, or a
project's `.claude/agents/`) are **thin adapters** that point to the role page, so
Claude, Codex, or any tool enacts the same brief. Specialized (project-specific)
roles live in the project, not the pool. The `librarian` maintains each role's
**Track record** after a verified win.

## Capture and promotion workflow

1. **Orient**: read `Wiki/index.md` and any directly relevant pages.
2. **Confirm scope**: verify the repository path before editing.
3. **Capture**: if the discussion contains reusable context or a correction,
   create/update a session journal page.
4. **Distill**: promote stable source-backed material into knowledge pages.
5. **Verify**: promote reusable development learnings into experience pages only
   after a green verifier.
6. **Decide**: record durable design choices as ADRs.
7. **Protect**: record repeated-risk rules as guardrails.
8. **Link**: add wikilinks between related pages.
9. **Index/log**: update `Wiki/index.md` when navigation changes and append to
   `Wiki/log.md` after every operation.

## Page format

Use simple Markdown and wikilinks. A normal page starts with:

```markdown
# Page Title

**Summary**: One to two sentences describing this page.

**Last updated**: YYYY-MM-DD

---
```

Knowledge pages add `**Sources**`. Experience pages add `**Type**`,
`**Stacks**`, `**Provenance**`, and `**Confidence**`. Journal, ADR, guardrail,
and roster pages follow their templates in `Templates/`.

## Linking convention

- Link between pages with wikilinks: `[[page-name]]` using the target's filename
  without the `.md` extension.
- **Page basenames are globally unique** across `Wiki/`, except `index.md`
  folder indexes. A flat `[[name]]` must resolve unambiguously no matter which
  subfolder the page lives in.
- Filenames are lowercase-with-hyphens (no spaces, underscores, or CamelCase),
  except conventional `index.md` pages.
- Folder indexes must be linked path-qualified, e.g. `[[roster/index]]`; use a
  normal Markdown link for the root `Wiki/index.md` when needed.
- Every new page should have at least one inbound link (avoid orphans) and a
  `## Related pages` list of outbound links.

## Provenance rules

- Knowledge: cite raw source files, research sources, or internal pages.
- Experience: cite the project/repo, commit/PR or working state, verifier
  command/result, and date.
- Journal: cite the session/date and mark status as captured, unresolved, or
  promoted.
- ADR: cite relevant pages and alternatives considered.
- Guardrail: cite the incident, risk, or rule that made the guardrail necessary.

## Assumption discipline

Hard rule: do not turn assumptions into facts, plans, wiki content, commits, or
external actions.

When a fact, source, project boundary, user intent, architecture rule, or import
decision is missing, an agent must do one of two things:

1. verify it from the repository, cited source material, a command result, or an
   explicitly provided human statement; or
2. ask the human before proceeding with any action that depends on it.

Working hypotheses are allowed only as clearly labeled hypotheses, preferably in
journal/working context, and must not be promoted to `Wiki/knowledge/`,
`Wiki/experience/`, project profiles, ADRs, or guardrails until verified.

To keep momentum, an agent should not loop over the same uncertainty. If a fact
cannot be verified after the relevant source checks, stop that branch, state the
specific missing fact, ask a focused question, and continue only on independent
safe work that does not depend on the assumption.

See [[no-unverified-assumptions]].

## Bulk import triage

Bulk imports, especially GPT memories or chat exports, require a review report
before any wiki write. The agent structures candidate material first; the owner
approves what enters the wiki.

Default: unclear material is not imported.

Personal or sensitive topics require explicit owner review. They may contain
transferable wisdom, but must be separated, redacted/generalized, and approved
before import. Never assume that indirect project context justifies storing
personal material.

See [[gpt-export-import-triage]].

## Privacy and security

Hard rule: do not store secrets, API keys, tokens, passwords, private account
data, private credentials, or unredacted sensitive logs anywhere in this
repository, and do not commit or push them to GitHub.

This applies to `Raw/`, `Wiki/`, `Templates/`, logs, journals, project profiles,
chat/GPT memory imports, screenshots, copied terminal output, and source
documents.

Before writing, committing, or pushing, inspect the diff and redact sensitive
values. Replace sensitive values with placeholders such as `<redacted-api-key>`
or `<redacted-account-id>`. If a source cannot be safely redacted, do not import
it.

Keep credentials outside Git, e.g. in environment variables, local user settings,
or a secret manager. Strip or generalize absolute machine paths unless the path
itself is the operational point of the page.

See [[no-secrets-or-private-account-data]].

## Team challenge workflow

For larger changes, use the roster as a challenge system:

1. **Orchestrator** defines the minimal team and dispatch order.
2. **Specifier** turns the goal into acceptance criteria.
3. **Researcher** gathers missing source/codebase context when needed.
4. **Implementer** makes the change.
5. **Verifier** runs the agreed checks.
6. **Code reviewer** challenges the diff.
7. **Wiki critic / librarian** decides what should be captured, promoted, or
   linked.

Unresolved disagreements are not hidden. Capture them in a journal page or ADR
with the current status and the next decision needed from the human.

## Parallel agent collaboration

Claude, Codex/GPT, and background agents may work on the same repository at the
same time. Treat the worktree as shared mutable state.

Before editing, check current Git status, read the current target files, and
inspect relevant diffs. Preserve unknown or unrelated changes. Use minimal
targeted patches. Do not restore, reset, reformat, stage, commit, push, or
cleanup another agent's work without explicit owner approval.

If a change overlaps another agent's work and the safe merge is not obvious,
stop and ask. Final reports must say which files changed, which parallel changes
were observed but not touched, and which checks ran.

See [[parallel-agent-collaboration]].

## Lint/audit checklist

When auditing the wiki:

- broken wikilinks;
- orphan pages;
- duplicated or near-duplicated pages;
- claims without provenance;
- stale inferred claims;
- pages in the wrong memory layer;
- missing index/log entries;
- sensitive material that should be redacted;
- drift between `AGENTS.md`, `Claude.md`, and this protocol.

## Maintenance and freshness

Every page carries `**Last updated**`; revisit pages on a light cadence so the
library stays trustworthy rather than accreting stale claims:

- **Experience**: re-check when the source project changes materially, or about
  quarterly. If still valid, bump `**Last updated**` and, with new evidence, raise
  `**Confidence**`; if contradicted, demote or correct it.
- **Knowledge**: re-check when its cited sources change, or about yearly.
- **Journal**: transient — promote to knowledge/experience/ADR/guardrail when
  earned, or mark `needs-review`; older captured sessions remain as history.
- **ADRs**: do not edit away a decision — supersede it with a new ADR and set the
  old one's status to `superseded`.
- **Guardrails**: re-check when the underlying risk changes; keep the triggering
  incident cited.
- **Roster**: update a role's track record when it is used; review it when its
  implementation changes.

Run the Lint/audit checklist (the `wiki-critic` role) periodically — e.g. when the
wiki has grown noticeably, or before relying on it for a significant decision.

## Git rule

Writes should be reviewable. Show a diff before committing and get user approval
unless the user explicitly requested an automatic commit. Never force-push or
rewrite history for this repository unless the user explicitly asks.
