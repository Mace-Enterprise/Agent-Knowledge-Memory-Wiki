# Karpathy loop + agent discipline — keep it tight

**Summary**: The operating method behind our 3-layer scaffold — a goal-driven Spec, a fast Verifier loop, a legible Environment — plus the agent discipline that keeps runs from exploding in tokens.

**Type**: experience / methodology

**Stacks**: any

**Provenance**: Idea base — Karpathy's 3-layer AI-coding model (Spec / Verifier / Environment). Validated in this session (2026-06-18): built the scaffold + roster + wiki; L2 proven on ExampleApp (`dotnet test` ExampleUnitTests 21/21).

**Confidence**: high

**Last updated**: 2026-06-18

---

## The loop (Karpathy's 3 layers, as we run them)

1. **Layer 1 — Spec, goal-driven.** Start from the **goal/outcome and its success measure** ("what does good look like, and how will we know?"), *then* derive a small, verifiable spec. Not "implement feature X" — rather "achieve outcome Y, measured by Z". Agile over waterfall: one coherent change per spec.
2. **Layer 2 — Verifier, fast & result-showing.** Verification is the **bottleneck**, not generation. Keep the loop **tight and short**: small diffs, fast/targeted checks. Crucially, **show the actual result** — run on **sample/fixture data** and present the real output (numbers, a table, a screenshot, a before/after), not just a green checkmark. Where output is **visual**, verify visually (screenshot / mock). A pass with no shown result is weak evidence.
3. **Layer 3 — Environment, legible & safe.** The agent must be able to run and observe — in a contained, reproducible environment. Never on the live system/real money (verifier + operations boundaries).

## Recycle first — reuse before rebuild

Before writing new code, check whether we already have it: scan the wiki
(knowledge/experience) and **other projects** for existing **boilerplate, patterns,
modules, or config** that can be adapted. Reuse beats reinvention — it's faster,
fewer bugs, and fewer tokens. The researcher/implementer recall first; the
code-reviewer flags duplication of something the codebase (or another project)
already provides.

## Autonomy slider (keep it on a leash)

Small change → verify → repeat. Human gates at **spec acceptance** and **before merge/deploy**. The more irreversible or outward-facing the action, the tighter the leash. Don't let an agent run many steps without a verification checkpoint.

## Agent run discipline (don't explode in tokens)

Multi-agent work can cost ~15× the tokens of a single pass, and a runaway agent escalates fast. So:

- **Report back / checkpoint.** A working agent surfaces progress at natural milestones (or every few steps) and **does not silently run for a long time**. Long task → break into checkpoints with a short status each.
- **Stay in budget; escalate, don't spiral.** If the task is bigger than expected, blocked, or looping, **stop and report** with what's known and the decision needed — never grind in circles.
- **Hire the minimal team.** The orchestrator picks the fewest roles that cover the work; no default fan-out.
- **Recall before researching.** Read the wiki (index-first) before re-deriving; reuse beats rediscovery.
- **Return conclusions, not transcripts.** Subagents hand back a tight distillation; heavy reading stays in their own context.
- **Index-first, atomic pages, prune as it grows.** Never load the whole wiki; keep pages small; consolidate over time.

## Where we go beyond Karpathy

Persistent **compounding memory** (this wiki: knowledge/experience/journal/adr/guardrails), a reusable **agent roster/team**, a **self-documentation** loop (librarian), **security/supply-chain** vetting, and **cross-tool** operation (Claude + Codex). Karpathy's loop is per-task; ours accumulates across sessions and projects.

## Related pages

- [[dotnet-test-fast-single-class]]
- [[agent-orchestration-options]]
- [[role-orchestrator]]
- [[role-specifier]]
