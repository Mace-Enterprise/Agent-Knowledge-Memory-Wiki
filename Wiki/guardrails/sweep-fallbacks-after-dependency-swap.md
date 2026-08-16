# Guardrail — after swapping a dependency, sweep every fallback and exception for the old name

**Summary**: When you replace a dependency because it failed, every *secondary*,
*fallback*, *backup*, *emergency* and *exception* entry that still names the old
one is a live regression waiting for an outage to expose it — grep the
configuration for the old name and decide about **each** remaining occurrence
explicitly.

**Trigger**: A whole household was moved off a filtering DNS upstream because a
false positive had cost hours of diagnosis; an audit of the resolver's own
configuration then found its `fallback_dns` still naming that same filtering
variant. Second instance the same day: a bypass alarm whose exception set still
described the *old* prescribed path reported the **new, prescribed** path as a
bypass.

**Scope**: Any configuration change that replaces a dependency — resolvers,
upstreams, mirrors, NTP/log/mail servers, API endpoints, package sources,
credentials, routes — and any rule set that names it (detectors, alarms,
allowlists, firewall exceptions, monitoring exclusions).

**Last updated**: 2026-08-13

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: needs-review — trigger present but neither dated nor an owner directive

---

## Rule

A dependency swap is not done when the **primary** points at the new thing.
It is done when **every occurrence of the old name has been decided about**.

Two failure shapes, one cause — a config entry inherits neither the reasoning
nor the correction applied to the primary:

1. **The fallback restores the failure you just removed.** The secondary entry
   still names the component whose behaviour was the reason for the change. It
   is invisible during normal operation: the only time it runs is the moment the
   primary is already down — i.e. exactly when a second, unexplained failure
   costs the most and looks least connected to anything you did. The symptom
   returns identically, with no obvious trigger and no recent change to blame.

2. **The exception set drifts.** A detector, alarm or allowlist was written as
   "everything except the prescribed path". After the architecture moved, the
   prescribed path is a different one — so the rule now excuses the old path and
   **flags the correct one**. A monitor that reports the intended behaviour as a
   violation is worse than no monitor: it trains the operator to ignore it.

The rule therefore is: **after any dependency swap, grep the configuration for
the old identifier and make an explicit decision per hit** — change it, delete
it, or keep it *with a written reason*. "Not mentioned in the change request" is
not a decision.

## Checks before acting

- **Grep by identifier, not by intent.** Search for the old address/hostname/URL
  /key across the whole configuration tree of the changed component *and* of
  everything that talks to it — not only the file you edited.
- **Enumerate the standard hiding places**: `*fallback*`, `*secondary*`,
  `*backup*`, `*alternate*`, `*emergency*`, bootstrap entries, hardcoded
  defaults compiled into a script, the DHCP/second nameserver, the "if the
  primary is unreachable" branch, and the *exception lists* of every detector
  and alarm that watches this subsystem.
- **Ask per hit: what happens when this line actually runs?** If the answer is
  "the failure we just eliminated", it is a regression, not a leftover.
- **Re-read every rule phrased as "everything except X"** after the architecture
  moved: X may no longer be the thing you meant to excuse.
- **Prefer a fallback that fails differently from the primary.** A fallback that
  shares the primary's failure mode is decoration; the point of a second entry
  is a *different* dependency, not a second copy of the same one.
- **Check the runbooks and the as-built page too** — a stale fallback in
  documentation gets typed back into the config by a future session.

## Escalation

If a remaining occurrence cannot be resolved without a decision the human owns
(e.g. "we have no second unfiltered upstream — do we accept the old one as
fallback or accept no fallback at all?"), stop and put the choice in front of
them with the consequence written out. Leaving it unmentioned silently picks the
worse of the two.

## Related pages

- [[fact-correction-sweep-all-pages]] — the same discipline for the wiki: a
  corrected fact must be swept across every page that states it. This guardrail
  is its operational twin (configuration instead of documentation).
- [[fehlersuche-grundregeln]] — rule 4, *silent fallbacks hide breaks*: the same
  invisibility, seen from the debugging side.
- [[dns-sinkhole-hang-looks-like-a-broken-server]] — the failure the fallback
  entry would have restored, and why it was so expensive to diagnose.
- [[0004-local-dns-filtering-upstream-resolves-only]] — the architecture change
  that triggered the audit.
- [[measurement-without-a-target-is-not-monitoring]] — the neighbouring failure:
  a monitor that runs and cannot fire.
- [[remote-network-change-without-lockout]] — the change-execution side (roll
  back by the rule's own identity, never by a shared property).
