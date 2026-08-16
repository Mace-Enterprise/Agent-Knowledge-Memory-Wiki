# Guardrail — offer wiki-capture at task/session end after a green verify

**Summary**: After a green verify (or at the end of a task/session that produced reusable learnings), the assistant must **proactively offer** to capture them into the wiki (`/learn` → the librarian) — it is part of "done", not an optional afterthought the owner has to remember to ask for.

**Trigger**: Across a self-hosted-GitLab build session that produced several verified, cross-cutting learnings, the assistant repeatedly **failed to proactively offer** `/learn` / wiki-capture at milestones and session end, despite the global working agreement requiring capture after a green verify. The owner had to prompt it. (2026-07-03)

**Scope**: Every project and session, cross-tool (Claude and Codex). Complements the global working agreement's "After a green verify, capture reusable learnings" loop.

**Last updated**: 2026-07-03

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: single incident — dated in Trigger

---

## Rule

When a unit of work reaches a **green verify** and produced anything reusable (a pattern, gotcha, verifier/environment recipe, methodology, decision, or a repeated-mistake rule), the assistant **proactively offers wiki-capture** before moving on or ending the session:

- Name the concrete candidates worth filing (one line each) and the likely layer (experience / knowledge / journal / ADR / guardrail).
- Offer to run `/learn` (or hand to the **librarian** role) to file them per `WIKI_PROTOCOL.md`.
- Do this at **milestones** too, not only at the very end — don't let a long session's learnings evaporate because capture was deferred to a "later" that never came.
- Capture **only what was actually verified**; label unverified material as journal/hypothesis. Do not fabricate learnings to have something to file.

The owner may decline — but the **offer is the assistant's job**, not the owner's to remember.

## Checks before acting

- Did this session reach a green verify and produce reusable learnings? → offer capture.
- Are the candidates already covered by an existing page? → propose *merge/enrich*, not a duplicate.
- Is anything to be filed unverified? → route to journal with an explicit status, don't promote.
- After capture: reindex the recall engine so semantic search stays current.

## Escalation

- If the owner declines capture, note it and move on — do not re-nag.
- If a "learning" cannot be verified, do not file it as experience/knowledge; offer a journal entry instead and say so.

## Related pages

- [[karpathy-loop-and-agent-discipline]] — the capture step of the loop
- [[role-librarian]] — who files verified learnings
- [[secure-repos-to-git-remote]] — a sibling "part of done, not optional" gate
