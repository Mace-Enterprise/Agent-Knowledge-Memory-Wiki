# New-project kickoff (best practice)

**Summary**: The standard, structured way we start any new project or major new workstream — recall-first, goal-driven spec, scaffolded contracts, a composed minimal team, a gated build loop, captured learnings. **This is the default for every new project, not a suggestion** — we don't improvise the start.

**Type**: methodology
**Stacks**: any
**Confidence**: medium (consolidates existing machinery; tighten with use).
**Last updated**: 2026-06-19

---

## Principles (the spine)

- **Karpathy 3 layers**: every project carries a **Spec** (Layer 1), a **Verifier** (Layer 2), an **Environment** (Layer 3).
- **Recall before build, capture after green.** Reuse the wiki; file verified learnings back.
- **Minimal team, token-frugal.** Hire only the roles the work needs; fan out deliberately (~15× cost). New roles/skills enter on **probation**.
- **Verify-first.** Nothing is "done" without fresh verification evidence.
- **External code = hiring catalog.** Security-audit and assimilate in our own words; never run unaudited code blind.
- **Owner gates.** Owner accepts the spec before build; approves commits/pushes; branch off `main`.

## The flow (0 → 7)

0. **Recall** — search the wiki (`experience-recall` / recall-MCP `search_notes`) for prior patterns, gotchas, verifier/environment recipes, and related projects. Don't rediscover.
1. **Brainstorm** — `brainstorming` skill: turn the idea into a validated design (2–3 alternatives, incremental sign-off) *before* speccing.
2. **Spec** — `/spec` + [[role-specifier]]: a goal-driven, verifiable spec (goal + success measure + acceptance criteria that map to verifier steps). Owner accepts it.
3. **Scaffold contracts** — `/karpathy-init`: generate `specs/SPEC.md`, `VERIFIER.md`, `ENVIRONMENT.md`, `TEAM.md`, and wire `AGENTS.md` (incl. the "keep the wiki fed" block). It detects the stack and reuses wiki verifier/environment recipes.
4. **Compose the team** — [[role-orchestrator]] reads `TEAM.md` + the pool ([[roster/index]]) and hires the minimal team plus any **domain SMEs** (project-local `.claude/agents/`). New roles/skills → probation ([[skill-and-agent-probation-lifecycle]]).
5. **(If pulling external code/skills)** — run the [[third-party-skill-agent-security-audit]] first; adopt only what's needed, assimilated in our words.
6. **Build loop** — orchestrator → specifier → implementer → verifier → code-reviewer → librarian. Gate: **owner-accepted spec** before implementing, **green verify** before "done" (verification-before-completion). Use `subagent-driven-development` for independent tasks.
7. **Capture** — `/learn` / experience-capture → [[role-librarian]] files reusable learnings (experience / knowledge / adr / guardrails), updates `index.md`/`log.md`, reindexes recall, and auto-records any probation promotions.

## Gates (do not skip)

- [ ] Owner accepted the spec before implementation began.
- [ ] Green verify (fresh evidence) before any "done" claim.
- [ ] Branch off `main`; owner approval before commit/push.
- [ ] External code/skills security-audited before adoption.
- [ ] No secrets/private data in the repo or the wiki.

## Quick checklist (copy at kickoff)

- [ ] 0 recalled prior wiki pages
- [ ] 1 design validated (brainstorm)
- [ ] 2 spec written + owner-accepted (goal + acceptance criteria)
- [ ] 3 `/karpathy-init`: SPEC / VERIFIER / ENVIRONMENT / TEAM + AGENTS wired
- [ ] 4 team composed (pool + domain SMEs; probation)
- [ ] 5 external code audited (if any)
- [ ] 6 build loop ran with the green-verify gate
- [ ] 7 learnings captured + recall reindexed

## Related pages

- [[karpathy-loop-and-agent-discipline]]
- [[skill-and-agent-probation-lifecycle]]
- [[third-party-skill-agent-security-audit]]
- [[role-orchestrator]]
