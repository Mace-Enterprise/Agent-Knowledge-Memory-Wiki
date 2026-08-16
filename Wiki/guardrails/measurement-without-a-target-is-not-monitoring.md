# Guardrail — a measurement without a target value is not monitoring

**Summary**: An instrument that **records** a value but carries no **expected
value** produces a log nobody reads and a notification nobody acts on. Every
metric worth measuring must ship with three things: **(a)** its target /
contracted / design value, **(b)** a deviation threshold derived from real
measured data, and **(c)** an edge-triggered alert on crossing it. Without all
three you have telemetry, not monitoring — and the fault can run for weeks in
plain sight. **Counter-rule (§ *When a threshold must not be built*): if the
instrument's spread is wider than the deviation you want to catch, do not put a
threshold on it — put the target value one layer down, where the signal is
deterministic.** **Sibling rule (§ *The wrong probe is not a measurement*): a
value compared against a target is still worthless if the probe asks a question
the subject is not obliged to answer — a device that does not reply to ping is
not offline, it is unmeasured.**

**Trigger**: homelab-firewall, discovered 2026-08-13. A 400-Mbit line delivered
**98 Mbit for two weeks** (2026-07-30 → 08-13, ≈ 75 % of the contracted bandwidth
gone — [[wan-100-mbit-episode-2026-07-30]]). **Three independent watchdogs on the
same box recorded the fault continuously and not one of them raised an alarm:**

- `fw-burnin` logged `speed=100` **264 times a day**. It alerts on link flaps,
  error-counter growth, temperature ≥ 65 °C and kernel errors — but **never
  compares the negotiated speed against an expected value**.
- `fw-speedtest` measured `down=98Mbit` **every day at 10:00** — and compares it
  to **nothing**. It only alerts when the test fails outright (`down=0`).
- The morning digest delivered the number to the owner's phone daily as
  `🚀 ⬇️ 98 Mbit/s` — which **reads as a measurement, not as a deviation**.

**Scope**: any recurring measurement — network throughput and link speed, disk
and memory headroom, backup size and duration, job runtimes, queue depth, API
latency and error rates, battery/temperature telemetry, data-feed row counts.
Also applies to business metrics in a daily report.

**Last updated**: 2026-08-16 (new § *The wrong probe is not a measurement* — the
sibling failure: an ICMP liveness sweep called 9 of 13 reserved devices offline,
including a printer that was reachable on five service ports the whole time)
Earlier: 2026-08-13 (new § *When a threshold must not be built* — the
guardrail's own deliberate non-application, and where the target value went
instead)

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: recurring incident — dated in Trigger, happened more than once

---

## Rule

1. **Write the target down next to the metric**, in the script or its env file,
   not in someone's head: `EXPECTED_LINK_SPEED=2500`,
   `CONTRACT_DOWN_MBIT=2000`. A metric whose "good" value only exists in a
   contract PDF or in the owner's memory is unmonitored by construction.
2. **State where the target comes from** — contract, datasheet, SLA, design
   target, or a measured baseline. A target nobody can justify gets silently
   lowered the first time it is inconvenient.
3. **Derive the threshold from real measured values**, never from a round
   number picked at authoring time (see the second instance below).
4. **Compare, then alert on the transition** — edge-triggered, so a persisting
   bad state does not spam and the recovery is announced
   ([[edge-triggered-vs-polling-alerts]]).
5. **A number in a status report is not a check.** If a human has to remember
   what "good" looks like in order to notice a problem, the check does not
   exist. Print the deviation, not only the value: `⬇️ 98 Mbit/s (Soll 400 —
   ⚠️ 25 %)` is a check; `⬇️ 98 Mbit/s` is decoration.
6. **Count instrumented subsystems, not instruments.** Three watchdogs looking
   at the same subsystem gave a **false sense of coverage** precisely because
   each one's silence was read as "fine". Silence is only evidence if the
   instrument was capable of breaking it.

## Second verified instance — a threshold nobody derived

Same box, 2026-08-09: the AdGuard spike alert `fw-adguard.sh` fired on
`delta ≥ THRESH`, with `THRESH` unset and therefore defaulting to **400 blocks
per 10 minutes** — against a real volume of **281 blocks in 24 h**. The
threshold sat roughly **35× above the entire daily volume**: the alert was
runnable and dead at the same time. Fixed by deriving the threshold from the
measured hourly rates (9–76/h → `THRESH=150`, about twice the observed peak)
and writing it **explicitly** into `/etc/fw-adguard.env` instead of relying on
an invisible default. Detail: [[homelab-firewall]] § (c).

Two rules fall out of that instance:

- **An invisible default is not a configured threshold.** Write it explicitly,
  even when it equals the default.
- **Check the metric's own semantics before thresholding it**: that alert also
  treated a **rolling 24 h statistic** as a monotonic counter, so
  `delta = now − previous` measured the net change of a sliding window and went
  to 0 as old entries aged out. Lowering the threshold would not have repaired
  that ([[fehlersuche-grundregeln]] rule 7 — check the check).

## When a threshold must NOT be built — an unreliable instrument

*(added 2026-08-13, from the deliberate **non-**application of this very rule)*

Applying rule 1 to the daily throughput probe would have meant writing the
contracted rate in as its expected value and alerting on the deviation. **It was
deliberately not built**, and the reasoning is the transferable part.

The probe returned **391**, then **38/45**, then **149/231 Mbit for the same line
within twelve hours** — far-end saturation and, for the last pair, a modified
instrument ([[measure-from-the-position-of-the-complaint]] rule 4). Any threshold
placed on that spread fires without cause. And an alarm that fires without cause
is not merely useless:

> **A muted channel swallows the real event too.** After a few nights of false
> alarms the notification gets muted, filtered or deleted — at which point the
> owner is **worse off than with no alarm at all**, because the same channel is
> the one that would have carried the genuine incident.

So the guardrail's demand does not become "threshold it anyway". It becomes:

1. **Compare the instrument's own spread against the deviation you want to
   catch.** If the noise is of the same order as the signal, the threshold is not
   a monitoring decision, it is a coin toss with a notification attached.
2. **Put the target value where the signal is reliable, not where the question is
   most interesting.** The interesting question ("do I get the throughput I pay
   for?") had no trustworthy instrument; the failure class actually experienced —
   a line silently running at 100 Mbit instead of 2500 for two weeks — is caused
   by the **negotiated link rate**, which is exact, instantly readable, never
   ambiguous, and available 264×/day. The check went there instead, and it
   catches the same incident far more reliably than a throughput threshold ever
   could.
3. **Generalise:** when a guardrail cannot be applied at the obvious place, look
   **one layer down for a deterministic signal** — usually a *negotiated
   parameter* or a *state flag* rather than a *rate*: link speed instead of
   throughput, replica count instead of latency, "backup ran and its size is
   within band" instead of "backup was fast", queue *stuck* instead of queue
   *deep*.
4. **Write the omission down as a decision, not as an oversight.** The contract
   figures were still put into the probe as a **comment block with the
   reasoning**, so the next reader (or the next agent) finds "this was considered
   and rejected because …" instead of an obvious gap, and re-litigates it only
   with new evidence — e.g. a probe whose spread has actually narrowed.

Boundary to the main rule: this is **not** a licence to ship metrics without
comparison. The metric still needs a target *somewhere in its chain*; what this
section says is that the target belongs on the **most deterministic member** of
that chain, and that a noisy metric may legitimately stay a pure log line.

## The wrong probe is not a measurement either

*(added 2026-08-16, homelab-firewall — the sibling failure of the headline rule)*

The rule above says a measurement without an expected value is not a check. The
same day produced its mirror image: **a check whose probe the subject is not
obliged to answer is not a measurement at all**, and it fails in the more
dangerous direction, because it does not stay silent — it produces a confident
number.

A liveness sweep over **13 reserved devices** used ICMP and reported **9 as
offline**. The network printer was among them. It was fully reachable the entire
time:

| Evidence | Reading |
|---|---|
| ARP / neighbour state | `REACHABLE` — the switch and the firewall were exchanging frames with it |
| DHCP | active lease under its own hostname |
| Service ports | **all five** answering (9100 raw print, 631 IPP, 80, 443, 515 LPD) |
| ICMP echo | no reply — **by the device's own choice** |

The conclusion "9 of 12 offline" was worthless, and on the strength of it **two
DHCP reservations were nearly written off as dead hardware**. Re-running the
sweep with a probe the devices must answer cleanly separated the two populations:
genuinely absent hardware showed `INCOMPLETE` neighbour entries and no open
ports; the rest merely filter ping.

**The rule.** For reachability, use a probe the device is **obliged** to answer:

1. **ARP/NDP state is decisive, ICMP is not.** `REACHABLE` (or a fresh entry with
   a MAC) means frames are being exchanged *right now* on L2; `INCOMPLETE` means
   nothing answered the address resolution — and address resolution is not
   optional for an IP host on that segment. ICMP echo **is** optional: firewalls,
   printers, appliances, hardened hosts and half of consumer IoT drop it as
   policy.
2. **Add one service port on the device's own protocol.** A printer answers 9100
   or 631, a switch answers 22 or its management port, a NAS answers 445/5000.
   "Answers the thing it exists to do" is the strongest available liveness
   signal, and it is the one the *user's* complaint is actually about
   ([[measure-from-the-position-of-the-complaint]]).
3. **Two independent negatives before declaring a device absent** — no neighbour
   entry *and* no service port. One negative is an instrument reading, not a
   finding.
4. **A negative result from an optional probe is not evidence.** It is the
   absence of evidence, and it must be reported as such: *"did not answer ICMP"*,
   never *"offline"*. The word chosen in the report is what the next person acts
   on — here it nearly triggered a deletion.
5. **A cross-check that already contradicts you outranks the sweep.** A fixed
   DHCP reservation, an active lease, a rule that references the host: those are
   *statements of intent* and they were sitting there the whole time
   ([[disabled-port-looks-like-a-dead-device]] rule 1 — inventory comes from the
   reservations, not from a live probe).

Generalises beyond ICMP: an HTTP `HEAD` against a service that only implements
`GET`, a TCP connect against a port behind an allow-list, an SNMP poll without a
community string, a "process is running" check for a daemon that forks. **Any
probe the subject may legitimately ignore turns a health check into a
coin toss with a plausible-looking output.**

## Checks before acting

- **For every existing recurring measurement, ask the three questions:** what is
  the target, what deviation matters, and who gets told when it is crossed? Any
  "none" is a gap, not a style choice.
- **Simulate the fault on paper**: "if this value were half of what it should
  be, which line of code notices?" If the answer is "a human reading the
  digest", it is not monitored.
- **Ask whether the subject is obliged to answer the probe.** If it may
  legitimately stay silent, a negative reading proves nothing and must not be
  worded as a finding (§ *The wrong probe is not a measurement either*).
- **Alert on the leading indicator too, not only the outcome.** Here the
  negotiated link speed (`speed=100`) was known **264×/day** and would have
  named the fault on day one; throughput was only the consequence.
- **After a change of the target** — new contract, new hardware, new SLA —
  update the expected value in the same change. A monitor still comparing
  against the old target is worse than none: it reports green.
  Concretely here: the line moved to 2 Gbit, so the monitored **link** target is
  **2500** (there is no 2000 Mbit Ethernet rate).

## Escalation

- If the target genuinely cannot be established (no contract figure, no
  datasheet, unknown baseline), say so and **record a measured baseline plus a
  band** instead — then treat any departure from the band as the alert. Do not
  ship the metric with no comparison at all. ⚠️ If the *instrument* is the
  unreliable part rather than the target, do **not** widen the band until it
  never fires — move the comparison to a deterministic signal instead
  (§ *When a threshold must not be built*).
- If a fault was running while instrumentation existed, capture the miss:
  the useful artefact is not "we fixed it" but "which instrument should have
  said it, and what did it lack".

## Related pages

- [[disabled-port-looks-like-a-dead-device]] — the same family seen from the
  other end: there the *device* looked dead because of the observer's own change,
  here because of the observer's choice of instrument. Both are answered by the
  same cross-check (the DHCP reservation list).
- [[locate-unknown-device-on-the-network]] — the escalation to run *instead of* a
  ping sweep when a device has to be found.
- [[measure-from-the-position-of-the-complaint]] — the instrument side: rule 4
  there (a change to the meter needs its own before/after) is why the throughput
  numbers in § *When a threshold must not be built* cannot be thresholded.
- [[throughput-is-a-path-property]] — the sibling rule from the same session:
  that one is about **where** to measure (the whole path, at the endpoint), this
  one about **what to compare the measurement to**.
- [[wan-100-mbit-episode-2026-07-30]] — the two-week fault this guardrail was
  earned on, with both logs.
- [[edge-triggered-vs-polling-alerts]] — the alert shape once you have a
  comparison: transition-triggered, with grace and silent bootstrap.
- [[unattended-job-failure-alert-on-output-channel]] — the adjacent failure
  mode: the job dies silently instead of alerting at all.
- [[fehlersuche-grundregeln]] — rule 7 (check the check) and rule 8
  (does the source count, or only show?).
- [[karpathy-loop-and-agent-discipline]] — automated checks decide "done", not
  a human glancing at a number.
- [[homelab-firewall]] · [[raspberry-pi-network-topology]] — the project and the
  as-built monitoring where this was found.
