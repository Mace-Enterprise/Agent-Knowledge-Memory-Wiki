# Guardrail — Verify the target repository before acting

**Summary**: Always verify the target path before using context or editing
files. This knowledge library is scoped to `<WIKI_DIR>`.

**Trigger**: A setup session needed an explicit repository-scope correction.

**Scope**: All Claude, Codex/GPT, and future agent work on this knowledge
library.

**Last updated**: 2026-06-19

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: owner directive, dated — 2026-06-18 (Codex session: unrelated repo declared strictly off-limits after a scope error)

---

## Rule

For this knowledge library, the only target repository is:

`<WIKI_DIR>`

Do not use any external repository as authority, template, schema source, review
baseline, or edit target unless the human explicitly asks for cross-repo
comparison.

## Checks before acting

- Verify the working directory before reading or writing.
- If the working directory is not the target path above, switch to the target or
  ask before continuing.
- Do not import external rules, schemas, or frontmatter requirements into this
  repository without explicit user approval.
- Before committing, inspect the diff and confirm every changed path belongs to
  `<WIKI_DIR>`.

## Recall index scope — keep separate projects OUT

The recall engine (`knowledge-recall` MCP) indexes **this library plus explicitly-registered
per-project `.memory/` dirs** (via `RECALL_EXTRA_DIRS`) — and **nothing else**. `WIKI_DIR` =
`<WIKI_DIR>\Wiki`; project memories are opt-in registered paths
(e.g. `<EXTRA_MEMORY_DIR>`, a repo's git-ignored cross-tool working memory). Never index
or import content from **unrelated** projects — in particular:

- **`LLM WIKI`** (`<UNRELATED_REPO_DIR>`) and **`llm-wiki-engine`** — the owner's own,
  unrelated work experiment that *generates* its own knowledge entries. Do **not**
  index it, mine it, or mix its content into this library. (Read only if the owner
  explicitly asks for a one-off comparison; never as a recall/index source.)

Verified 2026-06-19: the index held 76 notes — 71 from this library + 5 from the registered
`ExampleApp/.memory` — and **zero** from `LLM WIKI` / `llm-wiki-engine`.

## Escalation

Stop and ask the human when:

- the requested change could apply to more than one repository;
- a tool cannot access the target repository directly;
- a proposed rule would couple this knowledge library to an external project.

## Related pages

- [[2026-06-18-knowledge-library-reset]]
- [[0001-markdown-native-cross-model-memory]]
