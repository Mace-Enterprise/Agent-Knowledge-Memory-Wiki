# Guardrail: when a recorded fact is corrected, sweep ALL pages that state it

**Summary**: Correcting a wrong fact in one wiki page while other pages still
assert the old version creates a **self-contradicting wiki** — the next reader
(human or agent) recalls the stale copy and confidently repeats the mistake.
A fact correction is only done when **every page stating the fact** is updated
in the same change.

**Last updated**: 2026-07-03

**Enforcement**: audit — wiki-audit checks links/orphans; the sweep itself is manual

**Justification**: needs-review — no trigger recorded at all

---

## The rule

1. When the owner corrects a documented fact (hardware exists/doesn't, a
   username, a topology detail), **grep the whole wiki for the fact** (product
   names, IPs/masked IPs, hostnames, usernames — and their variants) before
   committing the fix.
2. Update **all** occurrences in the same commit — runbook, topology page,
   project profile, diagrams, index one-liners.
3. Where the wrong fact caused real confusion, leave a short inline note
   ("an earlier draft wrongly said X — corrected <date>") so a stale copy that
   resurfaces elsewhere is recognizably the outdated one.
4. Recall reads **both** pages later: if two wiki pages contradict each other,
   treat the contradiction itself as the bug — resolve it with the owner, don't
   pick one silently.

## Incident that earned this rule (2026-07-02)

A hardware fact ("there is a TL-SG105E switch") was corrected by the owner and
fixed in the firewall **runbook** — but the **topology page** still showed the
phantom switch. A later session read the topology page, re-asserted the
non-existent switch, and gave wrong advice built on it; the owner had to correct
the same mistake twice. One grep (`SG105E`) at correction time would have
prevented it. (Postscript: hardware can also change back — a real SG105E was
added later; the sweep rule is what keeps every page telling the same story
either way.)

## Related pages

- [[repo-boundary-llm-knowledge-library]] · [[no-unverified-assumptions]]
- [[raspberry-pi-network-topology]] · [[raspberry-pi-firewall]] — the pages involved.
