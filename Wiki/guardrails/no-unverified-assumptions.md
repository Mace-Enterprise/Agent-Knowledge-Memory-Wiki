# Guardrail — No unverified assumptions

**Summary**: Agents must not silently assume missing facts, user intent, project
boundaries, source meaning, architecture rules, or import decisions. They must
verify from evidence or ask the human before acting on the unknown.

**Trigger**: The owner explicitly required that the system must move forward
without circular rework, but assumptions are allowed only after consultation.

**Scope**: All Claude, Codex/GPT, and future agent work on this knowledge
library; especially project mapping, GPT memory imports, cross-repo distillation,
knowledge promotion, ADRs, guardrails, commits, and pushes.

**Last updated**: 2026-08-16 (added: dated external facts are never quoted from model
memory; what to do when two sources disagree on a detail; and two sibling instances from
the public release — documentation examples are generated, never recalled; license texts
are norm texts)

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: owner directive, dated — 2026-06-18 (Codex session: assume nothing, verify or ask back)

---

## Rule

Do not treat an assumption as a fact.

Before acting on a missing or ambiguous point, an agent must either:

- verify it from a cited source, repository file, command result, existing wiki
  page, or explicit human statement; or
- ask the human a focused question and wait for the answer.

This includes:

- which repository or project is in scope;
- whether two folders are the same project or separate projects;
- which project is current vs legacy;
- what a source file means when the source is ambiguous;
- whether a lesson is verified enough for `Wiki/experience/`;
- whether GPT memory or chat-export material may be imported;
- whether sensitive or private material is safe to store;
- whether a missing fact should become a wiki claim, decision, or guardrail.

## Dated external facts are never quoted from model memory

Regulatory dates, in-force dates, transition deadlines, norm/standard references
(`EN …`, `ISO …`, `DIN …`, directive and regulation numbers), version numbers of
external specs, and price/licence terms are the **highest-confidence-lowest-reliability**
class a model produces: they come out fluent, specific, and plausibly formatted, and they
are the first thing to have changed since training. Treat them exactly like a secret —
never write one from memory into a document, wiki page, or answer.

- Every such fact must carry a **retrieved source** (the official text, the register entry,
  the vendor's own page), fetched in this session. If it cannot be retrieved, the sentence
  does not get written — write it without the number, or mark it `Unknown:`.
- This applies to documents produced *for* the owner as much as to wiki pages. A wrong
  in-force date in a deliverable is worse than a missing one: it looks authoritative.
- **Incident (2026-08-16)**: two regulatory references in a generated document were stated
  from model memory. Both were confidently wrong and outdated; both survived an open-ended
  review and were only caught when the document was checked against sources. See
  [[adversarial-review-binary-verdict]] for the review shape that catches this.

Two sibling instances, proven 2026-08-16 during the engine's public release, show the same
rule covering material that does not look like a "dated fact" at first glance:

- **Example output in documentation is generated, never recalled.** The public README's
  quickstart shows expected `search_notes` output; it was produced by actually building the
  demo index over the bundled `Wiki/` (48 pages), running the search, and pasting the real
  result. An invented example is the documentation form of a lying instrument — the reader
  compares their own output against fiction and cannot tell which side is broken. Evidence:
  engine repo commit `f31a358`; the JSON in the README matches a live run (verified by that
  run, no attestation record — this was documentation production, not a verifier execution).
- **License texts are norm texts.** When the public repo moved from MIT to PolyForm
  Noncommercial 1.0.0, the license text was fetched verbatim from the canonical
  `polyformproject/polyform-licenses` repo (via the GitHub API), not reproduced from model
  memory. Same rule, same reason: a plausible-but-wrong legal text is worse than none — it
  looks authoritative exactly where authority matters. Evidence: engine repo commit
  `49e2511`.

## When two sources disagree on a detail: remove the detail

The Escalation section below says "stop and ask when sources conflict", and that is right
when the conflict is **load-bearing**. When it is not — two sources give different in-force
dates for the same regulation, two vendor pages give different limits — there is a third
move that is usually better than either picking a side or escalating:

**Delete the disputed detail and keep the statement that both sources support.**

A document rarely needs the exact date; it needs the fact that the obligation exists.
Removing the contested number costs nothing, removes the chance of being confidently
wrong, and does not silently launder a coin-flip into a fact. Picking the "more likely"
source *is* an assumption — the thing this guardrail forbids. Escalate instead when the
disputed detail is what the reader will act on.

## Momentum rule

Avoid circular work. If a fact cannot be verified after checking the relevant
source material:

1. stop the dependent branch;
2. state the exact missing fact;
3. ask one focused question;
4. continue only with independent safe work that does not rely on the unknown.

Do not repeatedly reread the same files or invent a default to avoid asking.

## Working hypotheses

Working hypotheses are allowed only when clearly labeled as hypotheses. They may
live in a session journal or temporary analysis, but they must not be promoted to
project profiles, knowledge pages, experience pages, ADRs, or guardrails until
verified or explicitly confirmed by the human.

## Required language

Use explicit labels:

- `Verified:` for facts backed by a source.
- `Unknown:` for facts not yet established.
- `Needs human confirmation:` for decisions or interpretations that require the
  owner.
- `Hypothesis:` only for temporary reasoning that will not be acted on without
  verification.

## Escalation

Stop and ask the human when:

- the next action would depend on an unverified assumption;
- sources conflict;
- a project boundary is unclear;
- an import could mix projects or leak private material;
- verification is not possible from available files or commands.

## Related pages

- [[repo-boundary-llm-knowledge-library]]
- [[adversarial-review-binary-verdict]] — the review shape that forces such claims to be defended
- [[no-secrets-or-private-account-data]]
- [[project-boundaries-and-shared-experience]]
- [[llm-knowledge-library-purpose]]

