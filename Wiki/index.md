# Wiki Index

**Summary**: Table of contents. Memory areas: **Knowledge**, **Experience**, **Journal**, **ADRs**, **Guardrails**, **Projects**, **Roster**.

**Last updated**: (template)

---

## Operating protocol

Canonical, tool-neutral protocol: [WIKI_PROTOCOL.md](../WIKI_PROTOCOL.md). Tool adapters: [AGENTS.md](../AGENTS.md) (Codex), [Claude.md](../Claude.md) (Claude Code).

## Roster (talent pool)

15 generic, reusable agent roles any project can hire — see [[roster/index]].

## Projects

_(none yet — add one profile per project under `Wiki/projects/`, from `Templates/project-page.md`)_

## Knowledge

Distilled, source-backed knowledge. *(examples below — replace with your own)*

- [[agent-orchestration-options]] — (example) why a cross-tool team stays markdown-native vs adopting a runtime framework.
- [[local-recall-engine]] — (example) hybrid (FTS+semantic) recall MCP over the wiki.
- [[codex-cross-model-integration]] — Codex as file-based peer + on-demand read-only CLI (sparring / peer-review / enact any role).

## Experience

Verified reusable development learnings (`Templates/experience-page.md`). *(examples below)*

### patterns

### gotchas
_(none yet)_

### verifiers

### environments

### methodology
- [[karpathy-loop-and-agent-discipline]] — goal-driven spec, fast/result-showing verify, recycle-first, token/report-back discipline.
- [[skill-and-agent-probation-lifecycle]] — new/adopted skills & roles start on probation; promoted to active only after a verified win (librarian auto-records).
- [[new-project-kickoff]] — central best practice for starting a new project: recall → brainstorm → spec → karpathy-init → compose team → gated build → capture.

## Journal

_(none yet — capture in-progress discussion under `Wiki/journal/sessions/`)_

## ADRs / Decisions

- [[0002-team-coached-self-improvement-loop]] — adopt the team-coached retrospective loop (outcome signal → coach-proposed deltas → owner gate → probation). Also the worked example for `Templates/adr.md`.

## Guardrails

- [[no-secrets-or-private-account-data]] — never store/commit secrets or private data.
- [[parallel-agent-collaboration]] — how concurrent agents coordinate without clobbering.
- [[repo-boundary-llm-knowledge-library]] — verify the target repo before editing (retarget to your repo).
- [[machinery-sync-engine-template]] — keep this engine template in step with the live system.
- [[third-party-skill-agent-security-audit]] — audit external skills/agents before adopting them.
- [[no-unverified-assumptions]] — state assumptions as assumptions; verify before relying on them.
- [[gpt-export-import-triage]] — triage chat/memory exports before import: inventory, redact, owner-approved batches; unclear = don't import.
