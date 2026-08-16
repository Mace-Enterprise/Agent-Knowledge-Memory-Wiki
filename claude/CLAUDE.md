# Global working agreement

## The loop (Karpathy's 3 layers)

Work in three layers on every non-trivial change:

1. **SPEC** — **goal-driven**: start from the goal/outcome + its success measure ("what does good look like, how will we know?"), then a small, verifiable spec. Don't implement against a vague prompt.
2. **VERIFIER** — automated checks decide "done", not vibes; verification is the bottleneck, so keep the loop fast (small diffs, targeted checks). Run the verifier before claiming a change works.
3. **ENVIRONMENT** — know how to run and observe the app (contained/reproducible). Describe runs via the project's environment contract.

## Agent run discipline (don't explode in tokens)

- **Report back / checkpoint** at milestones — don't run silently for long stretches.
- **Stay in budget; escalate, don't spiral** — if blocked, looping, or scope grew beyond the spec, stop and report with what's known and the decision needed.
- **Minimal team** (no default fan-out — multi-agent ≈15× tokens), **recall before researching**, **return conclusions not transcripts**, **index-first** on the wiki.
- See [[karpathy-loop-and-agent-discipline]].

## Where project contracts live

Each repo should carry tool-agnostic contracts, referenced from its `AGENTS.md`:
`specs/SPEC.md` (Layer 1) · `VERIFIER.md` (Layer 2) · `ENVIRONMENT.md` (Layer 3).

- **Read `AGENTS.md` first** in any repo; follow its pointers. A parallel GPT/Copilot agent reads the same files — keep them tool-agnostic and in sync with code in the same change.
- If these contracts are missing, suggest **`/karpathy-init`** to scaffold them.
- **Every new project or major workstream starts with the central `new-project-kickoff` best practice** (recall → brainstorm → spec → karpathy-init → compose team → gated build → capture). This is the **default, not optional** — don't improvise the start.

## Knowledge wiki (the cross-project brain)

The cross-project knowledge home is the wiki at **`<WIKI_DIR>`**. Its **canonical, tool-neutral protocol is `WIKI_PROTOCOL.md`** (`Claude.md`/`AGENTS.md` are thin adapters that point to it). `Wiki/index.md` is the table of contents.

- ⚠️ **Scope**: this wiki is `<WIKI_DIR>`. Verify you're in that path before reading/writing; don't pull any other repository in as authority unless explicitly asked.
- **Before** non-trivial work, recall relevant prior pages: prefer the **`knowledge-recall`** MCP (`search_notes`, hybrid semantic+keyword) if registered; else the **experience-recall** skill / read `Wiki/index.md`. Reuse, don't rediscover.
- **After** a green verify, capture reusable learnings (run **`/learn`** / the **experience-capture** skill → the **librarian** files them, following `WIKI_PROTOCOL.md`); then **reindex** the recall engine so semantic search stays current (incremental). Only file what was actually verified.

## Knowledge routing (which memory layer)

Per `WIKI_PROTOCOL.md`, the wiki has these layers — route to the right one:

- **Reusable dev learnings**, verified (patterns, gotchas, verifier/environment recipes, methodology) → `Wiki/experience/<category>/`.
- **Distilled, source-backed knowledge** → `Wiki/knowledge/` (with citations).
- **Valuable in-progress discussion / corrections / open questions** → `Wiki/journal/sessions/` (may be unverified, but label status).
- **Durable design decisions** (with alternatives) → `Wiki/adr/`.
- **Rules that prevent repeated mistakes** (scope, privacy, process gates) → `Wiki/guardrails/`.
- **Reusable agent roles** (the talent pool) → `Wiki/roster/`; per-project teams live in each repo's `TEAM.md`.
- **Volatile, project-specific facts** (one repo only — a path, a current bug state) → that repo's **`.memory/`**: git-ignored, **cross-tool** (read by Claude *and* Codex, referenced from the repo's `AGENTS.md`), and indexed by the recall MCP alongside the wiki (register the dir via `RECALL_EXTRA_DIRS`). Not the central wiki; the central wiki's project profile links to it. (Claude's harness `~/.claude/projects/<id>/memory/` may keep a thin auto-load pointer to it.)

## Engine template — keep it in sync

The reusable, content-free form of this whole system (protocol, templates, roster, the `~/.claude` machinery, and the recall MCP) lives in a separate repo: **`knowledge-wiki-engine`** (`<ENGINE_DIR>`). **Whenever you change the machinery** — `WIKI_PROTOCOL.md` / templates / roster / generic guardrails / methodology, the `~/.claude` agents-skills-commands, or the recall MCP — **mirror it into the engine in the same change** via its `sync.ps1` / `sync.sh`, then commit+push. It must not drift from the live wiki + `~/.claude`. Never copy project content into it (it stays content-free). See its `machinery-sync-engine-template` guardrail.

## Acquiring external skills/agents (hiring catalogs)

External skill/agent libraries (Superpowers, subagent catalogs, Hermes, etc.) are **hiring catalogs** we recruit from **on demand** — we do not bulk-install. Anything pulled from GitHub or elsewhere must pass a **security audit before adoption** into `~/.claude` or a project `TEAM.md`: clone to a scratch area outside our repos (never commit third-party code), check for prompt-injection/hidden instructions, exfiltration/phone-home, destructive or over-broad tool scopes, secret handling, and license; then **assimilate in our own words** (never paste verbatim) with provenance + the audit verdict. The security role owns the audit. See the `third-party-skill-agent-security-audit` guardrail.

The same discipline applies to **third-party model artifacts** (embedding models, local LLMs — ONNX/GGUF/safetensors weights): **never download or run a new model without the owner's per-action OK and the security role's audit** — provenance + pinned revision, safe format only (never pickle-based `.bin`/`.pt`), sha256-recorded, behaviorally A/B-evaluated before production. See the wiki's `third-party-model-gate` guardrail.

## Parallel-agent etiquette

Repos may be edited concurrently by a GPT/Copilot/Codex agent. Re-check `git status` / HEAD before and after a unit of work; never assume the tree is unchanged from last turn.
