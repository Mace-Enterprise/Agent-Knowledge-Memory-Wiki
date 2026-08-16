# Roster — the talent pool

**Summary**: The catalog of **generic, reusable** agent roles any project can hire from. This is the *pool*, not a team. Each project composes its own **team** from this pool plus its own domain roles (see "Per-project teams" below).


---

## Names (the team)

The roles carry first names for easy reference — the `role-*` slug stays the canonical id.

| Name | Role |
|---|---|
| **Max** | [[role-orchestrator]] (lead) |
| **Lisa** | [[role-specifier]] |
| **Bob** | [[role-implementer]] |
| **Elfie** | [[role-verifier]] |
| **Tom** | [[role-qa-test]] |
| **Anna** | [[role-code-reviewer]] |
| **Paul** | [[role-performance]] |
| **Mia** | [[role-researcher]] |
| **Ada** | [[role-analyst]] |
| **Ben** | [[role-librarian]] |
| **Eva** | [[role-wiki-critic]] |
| **Edith** | [[role-wiki-editor]] (copy-edit, probation) |
| **Tim** | [[role-security]] |
| **Nina** | [[role-operations]] |
| **Leo** | [[role-api-integrator]] |
| **Sara** | [[role-ui-ux]] |
| **Cora** | [[role-coach]] |
| **Kai** | [[role-network-sme]] |
| **Linus** | [[role-linux-websec-sme]] (Linux/web hardening, GPT sparring peer, probation) |

Domain (per-project, in their project's `.claude/agents/`): **Finn** — sme-trading · **Lena** — data-scientist.

## Pool vs team

- **Pool (this page)** — generic roles that apply to any project, maintained here in the one wiki. Reusable knowledge.
- **Team (per project)** — which pool roles a project hires, plus project-specific domain roles. Declared **in the repo** so Claude *and* Codex see it.

New/improved pool roles enter here only after they prove out (verified) — same discipline as experience pages. See [[agent-orchestration-options]] for why the team is markdown-native (no runtime framework).

## How to hire

1. The **[[role-orchestrator]]** reads the project's `TEAM.md` + this pool, composes the minimal team, and returns a dispatch plan.
2. Each role page is the **canonical, tool-neutral brief**. The main thread enacts a role via its thin adapter — a Claude subagent (`~/.claude/agents/<role>.md`) or the same page read by Codex — both operate from the one brief.
3. After a verified win, the **[[role-librarian]]** appends to the role's **Track record**.

## Pool roles (generic, reusable)

**Coordination**
- [[role-orchestrator]] — lead / hiring manager; composes the team and the dispatch plan.

**The Karpathy loop**
- [[role-specifier]] — Layer 1. Request → verifiable spec. (≈ business analyst)
- [[role-implementer]] — Layers 1→3. Code to satisfy the spec. (≈ senior developer)
- [[role-verifier]] — Layer 2. Runs the verifier; build/test only. (≈ senior tester)
- [[role-qa-test]] — Layer 2. Builds the tests the verifier runs; regression-test-first. (≈ QA engineer)
- [[role-code-reviewer]] — Layer 2 quality. Reviews the diff for bugs & quality. (≈ senior reviewer)
- [[role-performance]] — Layer 2. Profiles hot paths; before/after numbers. (≈ performance engineer)

**Discovery & decision support**
- [[role-researcher]] — web/codebase investigation → distilled, cited conclusions.
- [[role-analyst]] — deductive analysis → a recommendation; concludes but does not act without approval (read-only).

**Knowledge & quality control**
- [[role-librarian]] — files verified learnings into the wiki. (≈ operating/scribe)
- [[role-wiki-critic]] — audits the wiki and asks questions. (≈ reviewer/critic)
- [[role-coach]] — continuous-improvement manager; reads the outcome-log + track records, proposes process/skill/team deltas (advisory, owner-gated). (≈ engineering manager / retro facilitator) (probation)

**Safety & operations**

Security/Infosec includes reviewing this wiki itself before GitHub publication
for secrets, private account data, sensitive personal material, and other content
that does not belong in a public repository.
- [[role-security]] — vets cloned/forked code (malicious code + prompt injection), drives fork-and-adapt, checks deployment security. (≈ security engineer)
- [[role-operations]] — safe runtime (Docker/venv/sandbox), explains the basics, versioning/deploy. (≈ ops/DevOps)
- [[role-network-sme]] — home/SOHO network architect: topology/NAT/segmentation/DHCP-DNS/hardware-fit at concept level, plain-language for a non-expert (advisory, read-only). (≈ network architect) (probation)
- [[role-linux-websec-sme]] — Linux server & web-service **hardening** SME (SSH/firewall/fail2ban/TLS/exposed-service & app hardening), lock-out-avoidance first; consulted **as a cross-model GPT peer** for sparring (advisory, read-only). (≈ Linux sysadmin + appsec) (probation)

**Design & integration**
- [[role-ui-ux]] — UI/UX proposals shown as sketches/mockups, for projects with a frontend. (≈ UI/UX designer)
- [[role-api-integrator]] — external API/MCP integration, auth, docs (also a developer hat). (≈ integration engineer)

## Per-project teams

Each project picks its team from the pool and adds its own domain roles. Declared in the repo (so every tool sees it):

- `TEAM.md` at the repo root (tool-agnostic, referenced from `AGENTS.md`) — lists the hired pool roles + domain roles, and the workflow.
- `<repo>/.claude/agents/*.md` — project-local Claude subagents for the domain roles (project-local overrides the global pool).

`karpathy-init` scaffolds a starter `TEAM.md`. Example domain roles live in their
project's `TEAM.md`, **not** here — e.g. the trading project adds a
*subject-matter expert (trading)* and a *data scientist* on top of the pool.
