# Skill & agent probation lifecycle

**Summary**: A newly created or newly adopted skill or agent role starts on **probation**; it earns **active** only after a verified win, and is **demoted/retired** if it doesn't help. The [[role-librarian]] records every transition **automatically** in the same post-verify capture pass.

**Type**: methodology
**Stacks**: any
**Provenance**: adapted from Hermes' candidate→active→shadow skill curator (security-audited reference, 2026-06-19) + our verify-first discipline.
**Confidence**: medium (process adopted; will tighten thresholds with use).
**Last updated**: 2026-06-19

---

## Why

We recruit skills/agents **on demand** (the hiring-catalog model — see [[third-party-skill-agent-security-audit]]). Adopting one is a *hypothesis* ("this will help"), not a proven fact. Probation prevents **adopt-and-forget**: an unproven skill/role is never treated as battle-tested, and a useless one never quietly accumulates.

## States

- **probation** — newly created, or newly adopted (including harvested from external catalogs). Usable, but flagged unproven.
- **active** — earned after a **verified win**: it was actually used on a real task that passed its verifier and it demonstrably helped.
- **deprecated / retired** — didn't help, produced a wrong result, was redundant, or sat unused over a review cycle. Demoted (kept as shadow) or removed.

## Baseline vs newly-adopted

The **founding pool roles** (the original roster) are **active baseline** — the deliberately-designed, in-use team. This lifecycle governs **newly created or newly adopted** skills/roles from here on (e.g. the analyst role, the harvested skills): those start on probation and earn their way to active.

## Promotion criterion

probation → active after **≥1 real task with a green verify where the skill/role was actually used and helped**. Raise the bar to N occurrences over a window if noise appears (Hermes-style: e.g. ≥N runs, ≥X% success). Always record *what it was earned on*.

## Demotion criterion

active/probation → deprecated if it produced a wrong outcome, duplicated an existing item, or went unused across a review cycle. Note *why*.

## Auto-record (the rule)

The **librarian** records every transition **automatically**, as part of the post-verify capture (`/learn` / the experience-capture pass) — not as a separate manual chore:
1. Flip the `**Status**` field on the role page (`Wiki/roster/role-*.md`) or the skill's status line.
2. Append to the role's **Track record** (or the skill's status note): `date · project · what worked / limit`.
3. Add a one-line **`Wiki/log.md`** entry for the transition.

## Where status lives

- **Roles**: a `**Status**` field in the role brief.
- **Skills**: a `**Status**` line in the `SKILL.md`.
- **Transitions**: journaled in `Wiki/log.md`.

## Related pages
- [[third-party-skill-agent-security-audit]]
- [[karpathy-loop-and-agent-discipline]]
- [[role-librarian]]
