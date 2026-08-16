# Cascaded agent memory — tiny always-on index, topic packs on demand, recall for the rest

**Summary**: Structure an agent's persistent memory as three tiers — a tiny always-loaded index (behavior gates + rare-but-catastrophic guardrails only), on-demand topic packs cut by workflow, and a recall-indexed long tail — so per-session auto-load cost stays small without deleting a single fact. Hard rule: packs are **views** over canonical fact files, never a second source of truth.

**Type**: experience / methodology

**Stacks**: any

**Provenance**: designed + implemented in Claude Code session 2026-07-04 (ExampleApp project harness memory); design adversarially reviewed by GPT-5.5 via the gpt-chat sparring MCP **before** implementation (killed 3 flawed mechanisms pre-build); token effect measured structurally (auto-load ~4–6k → ~1.5k tokens, zero facts deleted).

**Confidence**: medium (single implementation, one session; multi-session benefit — packs actually being loaded when relevant — not yet observed).

**Last updated**: 2026-07-04

---

## Context

Claude Code (and similar harnesses) auto-load a per-project `MEMORY.md` index at the start of **every** session. Ours had grown to ~30 one-line entries (~4–6k tokens), all paid whether relevant to the session or not. Both naive fixes fail: deleting entries loses guardrails; leaving the flat index grows without bound. The fix is a cascade: spend always-on tokens only on what must be known *before any context exists*, and route everything else through on-demand loading or search.

## The pattern: three tiers

- **Tier 0 — always-loaded index (`MEMORY.md`)**: ONLY (a) **behavior gates** that must apply before any context is known — ask-before-acting rules, communication style, mandatory sparring gates — and (b) **rare-but-catastrophic guardrails** — things whose omission breaks a session or leaks secrets. Target **<16 lines**. Everything else becomes a one-line router pointer.
- **Tier 1 — topic packs, loaded on demand**: `topic-<domain>.md` files (e.g. backtesting, data-harvest, ops, pine-tradingview). Loaded only when working in that domain; Tier 0 holds exactly one router line per pack.
- **Tier 2 — recall-indexed long tail**: everything else lives in the wiki / repo-local `.memory/` fact files and is *found*, not preloaded, via hybrid search (`search_notes` — see [[local-recall-engine]]).

Cut packs **by workflow** (backtesting, ops), never **by ontology** (sqlite, python): ontology packs become junk drawers that no working context ever loads deliberately.

## ⚠️ Hard rule: packs are views, not a second source of truth

Topic packs contain **links + one-line hooks only**. Atomic fact files stay canonical ("one fact = one file"). **On conflict, the fact file wins.** Never merge fact content into a pack — duplicated content goes stale silently and creates a divergent second truth. This is the guardrail that keeps the cascade from decaying into copy-paste rot.

## Validated design gotchas (from the GPT-5.5 adversarial review)

The design was cross-model challenged before implementation; three initially-planned mechanisms were killed and two constraints added. We accepted and encoded these decisions:

1. **Retrieval ≠ usefulness.** Don't auto-promote/auto-archive knowledge by retrieval counts: popularity bias buries rare-but-catastrophic guardrails, and "frequently retrieved" can mean badly-ranked or misunderstood, not valuable. Usage logs are a *review queue* for retros — never an automatic lifecycle mechanism; never usage-archive guardrails/ADRs/runbooks.
2. **Eval-query overfit / wording leakage.** Auto-generating a recall eval query from the very note it must find only tests "can I phrase a query from this note". Use curated future-user phrasing, target the canonical note/cluster (not necessarily the newest file), and include both languages the user actually queries in.
3. **Model-aware index key.** A content-hash-only incremental reindex silently skips *everything* when the embedding model or chunk params change — the index cache key must include model name+version, chunk size/overlap, and schema version.
4. **Per-prompt "recall first" nagging fails.** A reminder injected on every prompt habituates and produces ritual compliance searches. Bind recall to real gates instead: before planning, before domain-critical edits, before capture/dedupe. The strongest inbound gate is a real failure — see [[failure-triggered-recall]].
   **Verified counterpart for OUTBOUND reminders (2026-07-04)**: a Stop-hook capture reminder that fires unconditionally re-prompts the model on every stop and **loops** — each forced reply triggers the next stop → chains of "nothing to file". Fix (verified, `~/.claude/scripts/learn-reminder.mjs`): fire only when (a) ≥80 transcript lines grew since the last fire AND (b) a ≥45-min cooldown passed; treat the first stop as baseline only; honor the `stop_hook_active` guard; otherwise exit silently with **no output** so no re-prompt happens.
5. **Dedupe before capture.** A capture workflow must first search for existing similar notes and extend them — otherwise the wiki grows semantic duplicates.

## Evidence

- Implemented 2026-07-04 in the ExampleApp project harness memory (`MEMORY.md` + topic packs); restructure checked the same day.
- Auto-load cost: ~4–6k tokens (≈30-entry flat index) → **~1.5k tokens**, with **zero facts deleted** (moved to packs / the recall tier).
- The design survived a cross-model adversarial challenge (GPT-5.5 via the gpt-chat MCP) that killed three flawed ideas pre-implementation: retrieval-count lifecycle, auto-generated eval queries, per-prompt recall nag.
- Not yet observed: multi-session benefit — hence **medium** confidence.

## Related pages

- [[karpathy-loop-and-agent-discipline]] — the token/run discipline this serves ("recall before researching", index-first, atomic pages).
- [[local-recall-engine]] — the Tier-2 search layer (hybrid FTS+semantic recall MCP); gotcha #3 above applies to its reindex (and is enforced in its code since 2026-07-04).
- [[failure-triggered-recall]] — the concrete "bind recall to real gates" mechanism (failed tool calls as recall trigger).
- [[agent-orchestration-options]] — why shared markdown memory is the token-frugal backbone in the first place.
- [[skill-and-agent-probation-lifecycle]] — the same "evidence-gated lifecycle, no automatic promotion" spirit applied to skills/roles.
