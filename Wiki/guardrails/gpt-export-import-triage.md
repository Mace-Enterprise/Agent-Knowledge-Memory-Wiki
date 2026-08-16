# Guardrail — GPT export import triage

**Summary**: GPT exports and memories must be triaged before import. The agent
structures candidate material first; the owner approves what enters the wiki.
Personal or sensitive topics are never imported automatically.

**Trigger**: The owner clarified that GPT exports may contain unrelated,
personal, sensitive, or only partially useful material. Some bits of wisdom may
be valuable, but not everything belongs in the wiki.

**Scope**: GPT memory exports, chat exports, copied conversations, external notes,
and any future bulk import into this knowledge library.

**Last updated**: 2026-06-20

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: owner directive — no incident needed

---

## Rule

Do not bulk-import GPT export material directly into the wiki.

The required flow is:

1. inventory the export;
2. redact or exclude sensitive/private material;
3. produce an import review report;
4. ask the owner for approval by category or batch;
5. import only the approved material.

## Default

If unclear, do not import.

Unclear material goes to one of:

- `Parking Lot`;
- `Needs human confirmation`;
- `Exclude`;
- `Redacted-only candidate`.

## Required triage categories

Every candidate item must be assigned exactly one proposed action:

- `Import to existing project`
- `Propose new project`
- `Cross-project knowledge candidate`
- `Experience candidate — needs verifier`
- `Journal / context only`
- `Parking Lot`
- `Redacted-only`
- `Exclude`
- `Needs human confirmation`

## Provenance citation

Every captured claim must cite the **verbatim source file** it came from. An item
that does not actually appear in its assigned source cluster must get a
**provenance recheck** — and be relocated or dropped — **before** filing. Never
file an item under a guessed source.

Trigger: a GPT-import claim was filed into the wrong journal citing source threads
it did not come from, caught only on owner challenge (2026-06-19; see
[[outcome-log]]).

## Personal and sensitive topics

Personal topics are not automatically excluded, but they require explicit review.

If a personal or sensitive topic contains useful transferable wisdom:

- summarize only the generalized lesson;
- remove identifying details;
- avoid private names, account data, health/financial/legal specifics, and
  emotionally sensitive details unless the owner explicitly approves;
- place it in a separate personal/sensitive review section before any import;
- ask the owner whether it should be excluded, redacted, generalized, or kept as
  private context.

Never assume that indirect project context justifies storing personal material.

## Import review report format

Before writing wiki pages, produce a concise report:

| Candidate | Topic | Proposed action | Sensitivity | Existing mapping | Question |
|---|---|---|---|---|---|
| short id | short label | category | low/medium/high | project/page or none | focused question |

The report should be short enough for the owner to approve quickly.

## Owner approval

The agent structures first; the owner approves.

No new project, personal topic, sensitive topic, or ambiguous cross-project
knowledge is imported without owner approval.

## Related pages

- [[no-unverified-assumptions]]
- [[no-secrets-or-private-account-data]]
- [[project-boundaries-and-shared-experience]]
- [[llm-knowledge-library-purpose]]
- [[outcome-log]]

