# Guardrail — reconstruct the design target before recommending a component, and confirm it with one closed question

**Summary**: Before recommending, sizing, or approving any component that sits
**on a path**, reconstruct the **driving design parameter** that path exists to
carry — and confirm it with **one closed question** that can be answered in three
words. The dangerous parameter is never the one being discussed; it is the one
that is **absent from the conversation** because everyone already "knows" it.
Design target and current load are **two separate numbers**: a component sized
against the current load silently fails the design.

**Trigger**: homelab-firewall, 2026-08-13. Advising on the upstairs switch, the
assistant optimised on the criteria that were **present in the immediate
conversation** — VLAN capability, fanless, port count — and never reconstructed
the parameter the whole build existed for: the **contracted line speed**. That
parameter was not in the conversation; it lived in an older decision record and
partly only in the owner's head. It was also invisible at the time, because the
line then delivered 400 Mbit, so a gigabit switch looked entirely adequate. When
the line moved to 2 Gbit the gap surfaced: 2.5G at the box, the firewall and the
core switch, then **two 1-Gbit hops** to the PC. Owner's verdict, paraphrased and
recorded on purpose: *"you missed that the whole target architecture was laid out
for a 2 Gbit contract and let me walk into a knife. I'm not blaming you, but you
should perceive more comprehensively and ask about the parameters again — without
being annoying."*

**Scope**: any purchase, sizing, or "is this component good enough" advice where
the component is one hop in a chain — network gear, cables and modules, storage
and bus paths, CI runners and build agents, VM/instance sizing, message brokers,
API gateways. Also applies to non-hardware capacity choices (thread pools,
retention windows, rate limits).

**Last updated**: 2026-08-13

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: recurring incident — dated in Trigger, happened more than once

---

## Rule

1. **Name the path, then its target figure.** Before the recommendation, write
   one line: *"This sits on <endpoint A> → <endpoint B>, whose target is
   <figure>."* If that line cannot be written, the recommendation is not ready
   ([[throughput-is-a-path-property]]).
2. **Reconstruct the figure from the record first** — the project profile, the
   ADR, the decision note, the backlog. **Recall before asking**; the parameter
   here *was* written down, just not in the room.
3. **Then confirm it with exactly one closed question**, answerable in three
   words: *"Target still 2 Gbit end to end?"* — **one question, closed, once.**
   Not an interrogation, and not a silent assumption either. If the answer
   changes the recommendation, say so in the same breath.
4. **Track design target and current load as two numbers.** "It's fast enough
   today" is a statement about the load, never about the design. Record both
   where the component is documented.
5. **A criterion absent from the conversation is not an absent criterion.** The
   ones actually discussed (features, noise, price, port count) are the ones
   least likely to be the trap — they already have everyone's attention.
6. **The asymmetry justifies the question.** Asking costs one line. Not asking
   cost a switch purchase plus a month of a capped path that nobody could see.

## Checks before acting

- **Two-number check**: write the design target and the present load side by
  side. If they differ, the component must be sized against the **larger**, or
  the shortfall must be stated explicitly as accepted.
- **Where does the parameter live?** If the answer is "in the owner's head",
  that is the finding — file it on the project page in the same change so the
  next session does not repeat this.
- **Is the requirement per device or per path?** A per-device tick chain never
  proves a path ([[throughput-is-a-path-property]]).
- **Ask the closed question at the moment of the recommendation**, not later.
  After the purchase it is an autopsy, not a check.
- **Keep it to one question.** If several parameters are unclear, ask the single
  decisive one and state the assumptions you are making about the rest — visible
  assumptions can be corrected, hidden ones cannot
  ([[no-unverified-assumptions]]).

## Escalation

- If the target figure cannot be established at all, **do not recommend a
  specific part**: name the decision it depends on, give the option set with the
  figure each option covers, and stop.
- If a component has already been bought against the wrong parameter, do not
  quietly re-plan around it. Record the gap where the requirement is tracked
  (backlog item + the reason), and check whether a cheap per-hop fix exists — a
  module or a cable at the slow end is often enough, and only visible once the
  hops are enumerated.

## Related pages

- [[throughput-is-a-path-property]] — the companion rule for verification:
  a requirement belongs to the path and is only done when measured at the
  endpoint. This page is the step **before** it, at recommendation time.
- [[no-unverified-assumptions]] — verify or ask; this guardrail gives the
  concrete asking form for capacity/design parameters.
- [[karpathy-loop-and-agent-discipline]] — start from the goal and its success
  measure, not from the prompt in front of you.
- [[measurement-without-a-target-is-not-monitoring]] — the same missing number,
  one layer later: a metric with no target value.
- [[fact-correction-sweep-all-pages]] — when the design target changes, sweep
  every page that carries the old one.
- [[homelab-firewall]] — the project where this was earned (backlog items 3d/5).
