# Role: librarian

**Summary**: Files reusable, verified learnings into the wiki, keeps it consistent, maintains role track records, and commits each write.

**Scope**: common (talent pool — reusable across projects).

**Layer / domain**: Cross-cutting (the learning loop). ≈ operating expert / scribe.

**Tools (Claude)**: Read, Grep, Glob, Write, Edit, Bash.

**Status**: active (baseline pool role) — see [[skill-and-agent-probation-lifecycle]].

**Last updated**: 2026-08-16 (track record: homelab configuration review)

---

## When to hire

After a green verify, or on `/learn` — to capture what was learned.

## Operating brief

*Tool-neutral — Claude, Codex, or any agent enacting this role follows this section.*

You turn what a verified session produced into durable, reusable knowledge. You do
not write product code and you do not verify it — you capture **after** a green
verify. The wiki's canonical protocol is `WIKI_PROTOCOL.md`; **follow it exactly**
(never modify `Raw/` once finalized; always update `Wiki/index.md` + `Wiki/log.md`;
lowercase-hyphen unique basenames; no secrets/account numbers; show a diff and get
approval before committing).

**Routing** (which memory layer): verified reusable dev learning → `experience/`;
distilled source-backed knowledge → `knowledge/`; in-progress/unverified → `journal/`;
durable decision → `adr/`; repeated-mistake rule → `guardrails/`; volatile single-repo
fact → that project's per-project memory (not the wiki).

**Write** (mirrors the ingest workflow): gather candidates + evidence → generalize
(strip secrets/paths) → dedup vs index/category (near-match → merge + bump
`Last updated`/`Confidence`) → fill the template → update index + log → commit.

**Role track records & improvement**: after a verified win, append one line to the
acting role's `Track record` (`date · project · what worked/limit`). If a clearly
better, **verified** way of working emerged, propose an edit to that role's canonical
brief (skill-smith loop) — never rewrite a brief on an unverified hunch.

**Probation lifecycle (auto-record)**: per [[skill-and-agent-probation-lifecycle]],
any skill/role used in this verified win that is still on **probation** gets promoted
to **active** — flip its `Status` field, append to its Track record / skill status
line, and log the transition. Demote/retire one that produced a wrong result, was
redundant, or sat unused. Do this in the same capture pass — it is not optional.

## Hand-offs

- End of the loop. Reports what was filed (paths, new/merged, commit) or why nothing was captured.

## Implementations (adapters)

- **Claude subagent**: `~/.claude/agents/librarian.md` (thin adapter → this page; carries the full operating detail).
- **Codex / other tools**: read this page + `WIKI_PROTOCOL.md`.

## Track record

*Appends after a verified win: date · project · what worked / limit.*

- 2026-06-18 · LLM Knowledge Library · filed the first verified experience page ([[dotnet-test-fast-single-class]]) and the orchestration research; dedups/merges before creating.
- 2026-07-03 · self-host GitLab · captured 3 cross-cutting experience pages + 1 guardrail from a verified session, generalizing beyond the existing GitLab env page (deduped against it, folded the GitLab-specific gotchas back into it); placeholders-only on the public wiki; wiki-audit 0 errors.
- 2026-07-03 · self-host GitLab (wave 2) · captured 3 more gotchas (robocopy `//` in git-bash, `git core.longpaths` on Windows, GitLab default-branch destroy+recreate) + a big methodology page (verified secret-purge recipe including the `refs/original/*` cleanup trap) + a pre-migration secret-sweep guardrail; cross-linked the "Windows/msys traps" cluster; placeholders only; wiki-audit 0 errors.
- 2026-07-03 · ExampleApp market-data harvest · filed 4 experience pages (bulk-export verification checklist, parquet ENOSPC truncation, Polygon ticker-encoding traps, Windows long-running harvest jobs) — deduped first (no near-matches; knowledge pages got cross-links instead of merged content); machine paths fully stripped.
- 2026-07-04 · self-host GitLab Python CI runner + rollout · filed a single coherent environment page ([[selfhost-gitlab-python-ci-runner]]) rather than 3 fragments (Runner install + canary pipeline + universal `.gitlab-ci.yml` + template-repo pattern + the two repo-local override gotchas from the 6-repo rollout — pytest name-collision on `*_test.py` scripts, integration-tests exclusion); rolled the 2 real gotchas from the rollout into the `ci/python-template` README too, so template consumers hit them; placeholders only; wiki-audit 0 errors.
- 2026-07-04 · agent-memory restructure (ExampleApp harness) · filed one methodology page ([[cascaded-agent-memory]]) instead of page + separate guardrail (folded the "packs are views, fact file wins" rule in); deduped first against karpathy-loop / local-recall-engine (no overlap — they cover run discipline and the search engine, not load tiers); kept the unverified items (model swap, eval set, result schema) out of the wiki — backlog only.
- 2026-07-04 · wiki-graph addon fix · filed a pattern ([[force-graph-layout-without-libraries]]) + an environment page ([[headless-preview-canvas-verification]]) from one verified fix; kept the screenshot-verification recipe separate from the layout recipe (different reuse contexts: graph layout vs any hidden-preview canvas page), cross-linked instead of merged.
- 2026-07-11 · Pi firewall alert rewrite · filed one methodology page ([[edge-triggered-vs-polling-alerts]]) generalizing the fix (a stateless 5-min status poll was spamming AP-DOWN → moved AP + IoT device checks to an edge-triggered watcher with state files + grace + silent bootstrap; hard-infra checks stay stateless); cross-linked to raspberry-pi-firewall / linux-network-admin-commands / adguard-home-dns-filtering. Live-verified: zero notifications on bootstrap when 4 new devices were added simultaneously (correct silent-by-design behavior). Placeholders only (real MACs / device labels stay in the operator's private local memory).
- 2026-07-13 · immobilien-screener Stufe-1 scraper · filed 5 new cross-project scraping/anti-bot experience pages (playwright-stealth 2.x Stealth-class API gotcha, scrape-embedded-typed-state pattern, golden-gzip-snapshot verifier, four-state-reachability pattern, headed-browser-via-Xvfb environment) from one green verify (pytest 37/37). Deduped: no prior scraping/Playwright/WAF page existed → all new; the one adjacent page ([[windows-cp1252-piped-python-output]]) was left untouched, not duplicated. Kept the reusable destillate in the wiki and the volatile portal-specific facts (which portal blocks now, concrete field names, venv/profile paths) out — those stay in the project's `.memory/`. Cross-linked the 5 into a coherent scraping cluster; observed 3 unrelated untracked pages from a parallel agent and did NOT stage them.
- 2026-07-14 · ExampleApp backtest→live + scanner ops · resumed after two aborted runs: found their 3 complete untracked pages via `git status` and adopted them instead of re-writing ([[backtest-to-live-parity-gate]], [[asof-replay-mode-daily-scanner]], [[telegram-html-message-line-boundary-chunking]]); merged the glitch-guard lesson into [[backtest-realism-pitfalls]] as item (r) rather than a new page; filed [[regime-conditioned-base-rates]] + [[extended-hours-data-liveness-and-entitlements]] new (no near-match); enriched [[market-data-providers]] with the measured extended-hours entitlements + Yahoo glitch trap; skipped a new page for the systemd Nebenbefund (already covered by [[systemd-timer-persistent-catch-up]]). Numbers filed as evidence, not targets; no positions/account data.
- 2026-07-14 · ExampleApp runner-exit management (d7/d7b) · condensed 5 candidates into 2 pages + 1 guardrail + 1 merge: the two exit-rule findings (tiered trail, profit ladder) share cohort and provenance → ONE coherent pattern page instead of two fragments; the conditioned-cohort methodology merged into [[quant-backtest-anti-overfitting-discipline]] beside its existing entry-vs-management split rather than a new page; [[manage-the-lot-not-the-symbol]] filed under patterns next to the MANAGE contract it refines (caller had labeled it methodology); order hygiene as a proper guardrail. Reconciled an apparent contradiction with [[intraday-runner-stop-and-sizing]] ("no partials") explicitly in the new page instead of leaving two pages that disagree. Privacy held (episode counts + medians only).

- 2026-07-17 · ExampleApp scanner seen-state fixes · filed 2 gotcha pages ([[seen-state-never-truncate-unordered-set]], [[silent-except-hides-dead-features]]) from one verified fix commit + ASOF simulation run; deduped against the state-file/alerting cluster (edge-triggered alerts, unattended-job failure alert, instrument-the-failing-path) — adjacent failure modes, cross-linked instead of merged; kept commit hash + repo as provenance, no volatile ExampleApp facts.
- 2026-07-17 · ExampleApp MARKTBLICK P0-fixes · filed 2 pattern pages from one verified end-to-end run ([[unattended-job-failure-alert-on-output-channel]], [[single-source-of-truth-for-mutable-facts]]) after deduping against the existing alerting cluster (adjacent but distinct → cross-linked, not merged); updated the [[twib]] project profile to the current MARKTBLICK state instead of filing operational facts as lessons; wiki-wide grep confirmed no other page carried the outdated claims; volatile detail left in the project's `.memory/`.
- 2026-07-22 · knowledge-wiki-engine / ExampleApp session · filed 1 methodology page ([[public-demo-mirror-of-private-repo]]) + 1 pattern page ([[session-handoff-for-agent-context-overflow]]) and extended [[pre-migration-secret-sweep]] with the commit-metadata point instead of a separate page (the guardrail is the natural home for a new sweepable-data class); recorded the first verified win (red→green owner test) for the new `/handoff` machinery per [[skill-and-agent-probation-lifecycle]] (status line lives in the machinery itself — transition journaled in the log); preserved a parallel agent's uncommitted mcp-registry/log changes via partial staging, did not commit them.
- 2026-07-24 · homelab-firewall link-negotiation session · filed 2 gotcha pages ([[ethernet-autoneg-diagnosis-order]], [[usb-nic-cdc-mode-blind-and-name-roulette]]) from an observation-verified ops session (ethtool/dmesg measurements, no test suite — provenance labeled accordingly); kept them in the protocol's fixed `gotchas/` category instead of creating a proposed new `networking/` folder; imported the owner-approved ITX decision note verbatim into `Raw/Projects/` (screened for secrets/IPs/MACs first) and linked it from the updated [[homelab-firewall]] profile (Pi→x86 successor decision); redacted a pre-existing real MAC found in the profile while editing; no probation transitions (no subagent roles used).
- 2026-07-22 · ExampleApp MARKTBLICK-v5 deploy · filed 2 pattern pages + 1 gotcha ([[shim-cutover-for-trigger-chains]], [[device-scoped-limited-api-keys]], [[positionally-read-config-preserve-line-order]]) from one green deploy + live-probe verify; dedupe was pre-run via recall by the caller and confirmed against the index (secret-sweep / purge / Pi-onboarding pages adjacent → cross-linked, not merged); again preserved a parallel agent's uncommitted mcp-registry/log changes via HEAD-based partial staging; no probation transitions (no probation roles involved).

- 2026-07-28 · homelab-firewall Protectli V1210 commissioning · filed 1 knowledge page + 3 gotchas and **merged 2 further candidates instead of creating thin pages** — the caller's "new pattern E/F" both landed as §4/§5 of [[remote-network-change-without-lockout]], which is the existing canonical page for that exact topic (the caller had already asked to cross-link to it); respected the owner's explicit instruction that the Protectli gets its **own** page parallel to [[raspberry-pi-firewall]] rather than rewriting the Pi runbook; handled a correction wave properly by **marking** 7 documented-but-unimplemented hardening items as "recommended but NOT implemented" with inline pointers instead of deleting the advice; no real IPs/MACs/hostnames (diff-level grep over every added line); preserved a parallel agent's uncommitted mcp-registry/log changes via HEAD-based partial staging again.

- 2026-07-29 · homelab-firewall V1210 switchover (second pass) · filed 1 gotcha ([[ssh-lockout-after-ip-migration]], four-cause structure with the Erkenntnisweg preserved per explicit owner wish) + 1 methodology page ([[fehlersuche-grundregeln]] — kept SEPARATE from [[instrument-the-failing-path-not-theories]] on purpose: general checklist vs deep-dive case study, cross-linked both ways) and merged 2 further candidates into their existing homes instead of new pages (staged-switchover → protectli §5; boot-log flap signature → ethernet-autoneg gotcha); ran the fact-correction sweep the switchover implied (V1210 → in production, Pi → fallback, across profile/runbooks/index); placeholders only; preserved the parallel agent's uncommitted work via HEAD-based partial staging again.

- 2026-07-30 · homelab-firewall MikroTik core-switch VLAN migration · filed 1 gotcha ([[mikrotik-transparent-bridge-vs-vlan-filtering]] — transparent factory bridge passes tags but segments nothing, + MNDP discovery + factory-subnet reachback) + 1 pattern ([[routeros-vlan-filtering-live-rollout]] — the no-outage `vlan-filtering=yes` flip: stage inert → native management → armed `/system scheduler` rollback + independent-vantage verify) from one live-verified session; deduped wiki-wide (no prior MNDP/MikroTik/RouterOS page → both new); honored the caller's explicit "NEW page + cross-link", NOT a §6 merge into [[remote-network-change-without-lockout]] (self-contained RouterOS procedure with its own lockout trap) — cross-linked both ways to that general principle and to [[stale-dhcp-lease-after-vlan-move]] for the lease side (not duplicated); ran the fact-correction sweep the swap implied ([[raspberry-pi-network-topology]] + [[homelab-firewall]]: core switch = CRS310, old Omada 2.5G retired, downstream Easy-Smart left transparent); MikroTik factory defaults kept (vendor docs, not owner network), owner ifaces/switch/MAC placeholdered; preserved a parallel agent's uncommitted mcp-registry/log work by stashing log.md around my own commit.
- 2026-07-29 · homelab-firewall V1210 bandwidth probe (third pass) · filed the six curl/speedtest measurement traps as ONE combined gotcha page ([[curl-bandwidth-measurement-traps]]) instead of fragments — same build, same provenance, only useful as a chain; per the caller's directive the unrelated `pkill -f` self-match trap went into the same page as a clearly-labeled section after grep confirmed no existing shell-gotcha home; backlog fact-update filed exactly as reported (speedtest ✅, flight-mode ✅ owner/partner-pending, 3 hardening items applied) with the unverified sub-requirements (nachts + idle-gate) explicitly labeled "not individually verified" rather than silently claimed; preserved the parallel agent's uncommitted work via HEAD-based partial staging again.

- 2026-08-06 · homelab-firewall AP migration (EAP650 → 2× MikroTik cAP ac) · filed 5 experience pages + 1 guardrail from 8 candidates and **merged 2 into their canonical homes** instead of thin new pages (the factory-router-class "pingable, no open ports, WinBox-by-MAC" finding became §4 of [[mikrotik-transparent-bridge-vs-vlan-filtering]] — which already owned "find/reach a factory MikroTik" and would otherwise have *contradicted* its switch-class "ports open" statement; the orphaned-port trap became a failure-mode section of [[routeros-vlan-filtering-live-rollout]], since it only exists once filtering is on); kept the two legacy-`wireless` findings as **separate** pages after checking their reuse contexts differ (status-flag semantics apply to any RouterOS AP; the flash budget applies to any 16 MB device); adopted and smoothed the owner's uncommitted SSID-masking + log edits rather than discarding them, and **redacted a real `sta_ip` prefix the owner's own new log line carried** (masking rule) while reporting the 55 pre-existing `192.168.x.y` occurrences as an out-of-scope follow-up instead of silently rewriting five pages; marked the three obsolete Omada sections in [[raspberry-pi-firewall]] as HISTORICAL with pointers instead of deleting them; 0 broken wikilinks.

- 2026-08-07 · homelab-firewall L2-hardening follow-up · handled a **fact-correction wave** first (the CRS326 had gone `vlan-filtering=yes` *after* the previous commit, so freshly written pages were already wrong) before capturing anything new — swept profile/topology/index and the regression tables, and wrote down *why* the closed gap was the dangerous one (untagged sockets landed in the mgmt VLAN; self-tagging bypassed the firewall's L3 segmentation at L2) instead of just flipping a status; filed 2 new gotchas ([[routeros-flag-representation-vs-effect]], [[routeros-import-can-fail-silently]]) and **merged 3 further candidates** into their canonical homes rather than thin pages (the ⚠️ silent-`/import` warning + post-check step + auto-rollback one-liner all went into [[detached-config-change-via-device-scheduler]], which is the pattern being qualified; rule 7 "check the check" + a rule-5 instance into [[fehlersuche-grundregeln]], bumping its "6 rules" wording everywhere incl. the index); corrected a **wrong** claim from my own previous capture rather than leaving it (PMF is not "off" in legacy `wireless` — it does not exist; `management-protection` is MikroTik-proprietary) across 4 pages; executed the owner-approved masking sweep (**60** real `192.168.x.y` occurrences → `xxx.xxx.<VLAN>.<host>`) while deliberately **not** masking the RFC1918 aggregate `192.168.0.0/16`, MikroTik factory `192.168.88.x` and public DNS4EU addresses, and added a notation note to each swept page so examples stay readable; kept the owner's four still-open security items listed as open (shared AP password, WLAN PSK as admin credential, no AP logging, unverified PSK entropy) instead of letting a hardening wave read as "done". Follow-up in the same session: flagged one candidate the caller had classified as as-built-only ([[client-isolation-is-per-interface-not-per-ssid]]) as worth its own page, got the go-ahead, and filed it **vendor-neutrally** (the mechanism is generic, only the fix name is MikroTik) with the measurement recipe rather than the setting — the as-built row now links to it instead of carrying the lesson. Take-away: reporting a routing disagreement beats silently over- or under-filing.

- 2026-08-08 · homelab-firewall WLAN-PSK encoding trap · filed 1 gotcha
  ([[non-ascii-wpa-passphrase-transfer-mangling]]) and **spent as much effort on the four
  cross-page edits as on the page itself**, because the value of this finding is
  *discrimination*: the wiki already held a second "this SSID accepts nobody" case, so
  [[wpa3-transition-disable-blocks-wpa2-fallback]] got a five-row comparison table
  (who fails / when / client message / AP log / where the fix lives) — a lesson that can
  be confused with an existing one is only half filed. Recorded the **flip side** of
  [[routeros-import-can-fail-silently]] honestly (here `/import` was the *working*,
  byte-faithful path) as a qualification rather than letting two pages appear to
  contradict each other. Kept the owner's "it works now" and "do it differently" both
  intact instead of resolving them into one recommendation (the 19-char PSK works, *and*
  ASCII 32–126 is the rule — the reason is the accidental UTF-8 agreement between both
  ends). Rule 7 of [[fehlersuche-grundregeln]] gained its sharpest instance yet: a check
  that reads back through the same path that mangled the value can never fail. Masking
  held: no passphrase, no character of it, no real IPs/MACs; the as-built note on
  [[raspberry-pi-network-topology]] says *that* the kids SSID has a special character and
  how it must be set, never what it is.

- 2026-08-09 · homelab-firewall central-logging session · filed **4 experience pages + 1 pattern** and **extended a methodology page** from a live-verified session (Protectli V1210 + four MikroTik, provenance `37ce6ba`): NEW [[rsyslog-central-receiver-per-host-files]] (with candidate 7 "a receiver brings three disk consumers" **folded in as a §** rather than a thin gotcha, and the "prove the receiver before the senders" isolation step), NEW [[journald-rewrites-kern-facility-userspace]], NEW [[routeros-default-remote-logging-action]], NEW [[routeros-scp-needs-ftp-policy]], NEW pattern [[detect-lateral-movement-not-egress]] (the zero-baseline, privacy-preserving detector); and **extended rule 5 of [[fehlersuche-grundregeln]]** with the config-GENERATING-patch instances (nft patch anchored on an interface name where the file uses `$IOT30` variables; `awk` insert before the `if` block) instead of a new page — the caller flagged it as an extension and it *is* the exact "verify the running state, not the exit code" rule. Judged candidate 4 (scp/`ftp` policy) a **distinct** trap from the adjacent [[mikrotik-transparent-bridge-vs-vlan-filtering]] §4 and gave it its own page, cross-linked. Reciprocally linked the 1/6 candidates to [[dnsmasq-duplicate-dhcp-option-and-conf-dir]] (same "a file the daemon reads you didn't intend / `--test` passes but restart fails" family). Placeholders only (`<mgmt-ip>`, `xxx.xxx.<VLAN>.x`) — grep confirmed no real IPs; 0 broken wikilinks; no probation transitions (no subagents used).

- 2026-08-09 · homelab-firewall SSH key-auth bootstrap · filed 1 gotcha ([[routeros-ssh-key-only-by-key-import]]) — the `always-allow-password-login` name trap: default `no` allows SSH password login only for **keyless** users, so importing a key is what makes a user key-only (the flag is a no-op / `=yes` is anti-hardening), and the setting is **SSH-only** (WinBox password fallback survives → no lockout). Dedupe-first grep confirmed no existing home; wove it into the `routeros-*` gotcha cluster with a **reciprocal** forward-link from [[routeros-scp-needs-ftp-policy]] (the key-upload step that precedes this payoff) rather than leaving the two adjacent findings unlinked; a truth table carries the discrimination (has-key × flag → password allowed?). Placeholders only, 0 broken wikilinks, no probation transitions (experience-capture skill + operator only).

- 2026-08-13 · homelab-firewall WAN 2-Gbit upgrade + link instability · filed **1 guardrail
  + 1 pattern + 1 journal page** and put the larger half of the effort into **two
  extensions** the caller had already routed correctly ([[ethernet-autoneg-diagnosis-order]]
  gained a *Step 0* ahead of its own existing Step 1 — counting link events per interface —
  plus the per-port capability rule and the "at which speeds does it die" discriminator;
  [[fehlersuche-grundregeln]] gained rules **8 and 9**). Judgement call the caller left
  open: "Momentaufnahme ≠ Historie" is **its own rule, not an instance of rule 7** — rule 7
  asks whether *your check* is sound, rule 8 asks whether the *source* can answer at all
  (a correct reading of a display that keeps no counter is still no evidence); cross-linked
  the two rather than folding them. Kept the unresolved root cause **out** of every
  experience page and in a journal page labelled `needs-review` with the decisive number
  (baseline counter = 129) so the pending cable-swap verdict is still reachable days later.
  Wrote down the **honest provenance** the caller offered (the agent called "it settled"
  twice and was wrong both times) — that failure is what makes rule 9 credible. Corrected
  two ✅ that were only partly true (backlog item 3 done for the core switch but not for the
  path to the PC → new sub-item 3d; item 5 re-framed as the check that would have caught it)
  and swept the index's homelab status block, which had gone stale on three items closed
  2026-08-09. Privacy held: no CGNAT/IPv6/MAC, box-side WAN subnet masked, vendor model name
  kept — and the *absence* of a key-file entry for the provider box recorded as a fact.
  0 broken wikilinks.

- 2026-08-13 · homelab-firewall, **second pass** on the same day · the pass was
  mostly **judgement, not typing**: (1) answered the owner's open question "does this
  need a *historical* knowledge type?" by **extending the protocol, not the folder
  tree** — `WIKI_PROTOCOL.md` gained a `Status: historical` + `Valid: <range>` +
  `## Why this is kept` convention, modelled deliberately on the existing **tombstone**
  precedent (a status modifier on a normal page) and explicitly contrasted with it
  (tombstone kills an *approach* and needs `REOPEN_IF`; historical preserves a *fact
  that was true then* and needs a date range), so the answer is reusable instead of a
  one-off; (2) **corrected my own previous conclusion** rather than leaving it: the
  first pass had the WAN patch cable defective "since 2026-07-30" — the log pattern
  (whole days at link 1000, whole days at 100, one fully recovered day) refutes that,
  a damaged pair does not switch back by the day, so the cable explains only the
  same-day flapping and the two-week throughput loss got its own historical page;
  (3) resisted folding the session's strongest lesson into
  [[fehlersuche-grundregeln]] as "rule 10" — those rules are about *finding* a fault
  you are already hunting, [[measurement-without-a-target-is-not-monitoring]] is about
  *noticing* one, and it is the sibling of [[throughput-is-a-path-property]] (*where*
  to measure vs *what to compare against*), so: cross-link, don't merge; (4) rescued
  an orphaned lesson — the AdGuard "threshold 35× above the daily volume" finding was
  sitting inside the project profile and became the **second verified instance** on
  the new guardrail; (5) wrote the owner's advisory complaint down as a rule with its
  constraint intact ("without being annoying" is part of the requirement → *one closed
  question, once*, in [[confirm-the-design-target-before-recommending]]), and named
  the asymmetry that justifies it; (6) re-framed a backlog item that was **wrong about
  the tooling** (a daily throughput probe had existed since 2026-07-29; what was
  missing was the comparison) into 5a/5b instead of leaving "no measurement exists".
  Kept the journal basename `…-unresolved` despite the resolution — it is linked from
  the append-only `log.md` — and made the header status authoritative with a note.
  Privacy held (no CGNAT/IPv6/MAC/credentials); 0 broken wikilinks.

- 2026-08-13 · homelab-firewall, **third pass** on the same day · routed eight
  candidates across **four different layers** instead of filing everything as
  experience: the two DNS changes that were *applied and proven on the wire* became
  experience pages ([[firewall-own-dns-via-resolv-conf-head]],
  [[encrypted-dns-proof-and-bootstrap-leak]]), the resolver-provider facts became a
  **knowledge** page ([[dns4eu-resolver-variants]] — with the two secondaries that
  were *not* measured explicitly marked unknown rather than pattern-guessed), the
  security audit's reasoning became **knowledge** + its choice an **ADR**
  ([[software-supply-chain-trust-roots]] · [[0003-no-proprietary-speedtest-binary-on-the-firewall]] —
  analysis is not a verified change, so it must not enter `experience/`), and the two
  **unfixed** security findings were filed as *open* (project backlog 10 + an as-built
  ⚠️ in the isolation matrix), never as lessons. Kept the process complaint's teeth by
  writing it where it will fire — a **"when to engage the security role"** trigger
  section in [[third-party-skill-agent-security-audit]], not a sentence in a session
  log — and recorded honestly that the guardrail already required it and the failure
  was not applying it unprompted. Carried a **correction of our own earlier framing**
  into the page rather than quietly dropping it (self-computed sha256 ≠ the AdGuard
  upstream-checksum precedent), and ran a wiki-wide **fact-correction sweep** for the
  provider box's vendor (ZTE → Huawei OptiXstar) across index, profile, topology,
  journal and the historical page, leaving the append-only `log.md` history intact.
  Privacy held: no serial/product ID, no CGNAT WAN address, no IPv6 prefix, no MAC;
  RFC1918 masked incl. the box-side WAN subnet (generic pages use placeholders
  throughout), DNS4EU public addresses deliberately unmasked per the existing
  convention. Untracked `.memory/` left untouched. 0 broken wikilinks.

- 2026-08-13 · homelab-firewall, **fourth pass** on the same day · the right answer
  was **no new page**: both generalisable mechanics were merged into the pages that
  already own them, and the effort went into placing them precisely. (1) "`nslookup`'s
  `Server:` line reports who you *asked*" is not a DNS fact but an instance of
  **rule 7** ("check the check") — a diagnostic field filled in *before the answer
  arrives*; generalised in the page to any client that labels its output with the
  endpoint it aimed at. (2) "added the rule ≠ the rule fires" went to **rule 5**
  rather than becoming rule 10: rule 5 is exactly "written ≠ active", and this is its
  sharpest form — the rule *is* in the running state and still never matches, so only
  its own packet counter is evidence. The **recipe** half of the same finding
  (`insert` vs `add`, no-flush live application, `nft -c -f` without applying,
  rollback by handle via comment) went to
  [[remote-network-change-without-lockout]] as **§6**, the production sibling of its
  §4 — deliberately split rule-from-recipe and cross-linked, so neither page grows a
  duplicate. Kept the **accepted** DoH-over-443 gap as an *open* backlog item with its
  three costed options and its dependency on "Stufe 3", never as a solved lesson, and
  did not let the profile's ✅/❌ DoH/VPN table read better than it is. Recorded the
  `!=`-exclusion insight (an enforcement rule whose normal-operation counter is 0
  doubles as a detector) in the as-built and **linked** it to the existing
  zero-baseline detector page instead of restating it. Privacy: segment addresses
  masked / interface variables used, DNS4EU publics left real per convention.
  Untracked `.memory/` untouched. 0 broken wikilinks.

- 2026-08-13 · homelab-firewall, **fifth pass** on the same day · the routing work
  was choosing **four different homes for eight candidates** and refusing two easy
  shortcuts. (1) The architecture change went to an **ADR**, not to `experience/`:
  it is a decision with live alternatives (second instance, per-segment upstream
  ladder, own block page) and its value is the *reasoning*, not a recipe — and the
  ADR states plainly that it **reverses** the shape recorded ten hours earlier
  (global = strictest/children) plus the **honest residue** that the children's
  filtering still depends on the third party. (2) Resisted a rule 10 in
  [[fehlersuche-grundregeln]]: "resolver latency proves nothing about resolver
  correctness" is rule 7 measured on the wrong dimension, and "check a new watchdog
  against a known state" is rule 7 pointed at the instrument — both became
  instances, the *page* that owns the incident is the new gotcha. (3) The
  deletion-loop near-miss went to [[remote-network-change-without-lockout]] §6,
  which already owns "roll back by handle via the comment" — the deleting half of
  a section that only described adding. (4) **Assumption discipline over a tidy
  as-built**: the reported client entries for *all six* segments plus "every
  segment carries the baseline" strongly implies backlog 11 ("Stufe 3") is done,
  but the DHCP state was not part of the report — so it is marked **explicitly
  unproven in three places** (segments table, new §, backlog 11) with the command
  that would settle it, instead of being written as fact. (5) Corrected a table
  from the previous capture in place (the DoT rule is no longer a `drop`) and left
  backlog 14 (a)–(e) standing as open rather than reconstructing them from memory.
  Privacy held: no sinkhole IP, no destination IPs, no VPN-provider resolvers, no
  public address of the line; the two general pages written product-neutrally.
  0 broken wikilinks.

- 2026-08-13 · homelab-firewall, **sixth pass** on the same day · the pass turned on
  one routing call the caller explicitly left open: the session's overarching lesson
  ("five measurements, each correct, none representative") became **its own page**
  ([[measure-from-the-position-of-the-complaint]]) **and** a compact **rule 10** in
  [[fehlersuche-grundregeln]] — not a bullet under rule 7, because rule 7 asks whether
  a *check* is sound while rule 10 asks whether it describes *the situation the
  complaint is about*; the already-filed "fast is not right" instance stayed under
  rule 7 as the labelled boundary case instead of being duplicated. Took the caller's
  hint on the second judgement call too and made it **one** page, not two: the
  `fallback_dns` finding and backlog 14(c) (a bypass alarm's exception set flagging the
  *prescribed* path after the architecture moved) are the same mechanism, so
  [[sweep-fallbacks-after-dependency-swap]] carries both instances and **closes 14(c)**;
  14(d)/(e) closed as two of the five instances on the measurement page, leaving only
  (a)/(b) open rather than reconstructing them from memory. Split the WLAN material by
  layer instead of by session: the **regulatory + capacity facts** went to
  `knowledge/` ([[wlan-channel-width-planning-eu]] — one DFS-free 80 MHz block in the
  EU, PHY ÷ 2, 2.4 GHz stays at 20 MHz), the **two live traps** to a gotcha
  ([[wifi-channel-width-notation-and-extension-direction]] — `20-Ce` is 40 MHz; the
  wrong extension direction pushed a radio into DFS `DP`), and the two remaining
  candidates were **merged**, not filed (radio auto-revert → the device-scheduler
  pattern; "compute both ceilings before optimising a hop" →
  [[throughput-is-a-path-property]]). Recorded the *retracted* 6× claim and the agent's
  own five misdiagnoses as honest provenance — that is what makes both new rules
  credible. Privacy held (no SSIDs/MACs/public addresses; frequencies and RouterOS
  syntax kept as technical fact; items 1–6 written vendor-generic). 0 broken wikilinks;
  `.memory/` untouched; no probation transitions (the acting roles were not reported —
  not assumed).

- 2026-08-13 · homelab-firewall, **seventh pass** on the same day · a deliberately
  small pass whose whole value was **not growing the wiki**: three candidates, **zero
  new pages**. (1) The autoneg finding was a *third* instance of a rule the page
  already owns — but the **mirror image** of the two on it (morning: local side offers
  2.5G, far side refuses; evening: switch offers, device cannot), so it was filed as a
  labelled direction-flip with the generalisation the two instances jointly earn — *the
  advertisement readout answers "whose limit is it" whichever end you suspect* — plus
  the boundary it does **not** answer (whether the limit matters), cross-linked to the
  guardrail that does. (2) Kept the ceiling lesson **inside**
  [[throughput-is-a-path-property]] as rule 6 rather than starting a page: it is the
  exact converse of that guardrail's own thesis (a requirement spans the path / a
  *diagnosis* does not span the path), and its sharpest form is purchase advice, where
  over-specifying costs the owner money. (3) Routed the AP replacement to the **project
  profile**, not `experience/` — a decision with no verified recipe behind it — and
  wrote the **why** at length because the counter-intuitive part (throughput was *not*
  the driver; WPA3/PMF/802.11r were, and are structurally impossible in 16 MB of flash)
  is exactly what gets misremembered as "we bought faster APs". Flipped the two affected
  open items from *accepted* to *planned resolution* instead of closing them, recorded
  the rebuild cost (different config tree, ≈ an evening per AP) so the decision is not
  read as free, and added a follow-up box to
  [[mikrotik-cap-ac-flash-budget-wireless-packages]] so its deliberate "stay legacy"
  trade does not stand as the end state — with the transferable half named: when the
  missing features turn out to be requirements, the **device** changes, not the package.
  Also carried the retracted 2.5G recommendation into the wiki verbatim as provenance,
  since a rule about over-specifying is only credible with the mistake attached.
  Privacy held (no SSIDs/MACs/addresses; product names and standards kept). 0 broken
  wikilinks; `.memory/` untouched; only `Wiki/` staged.

- 2026-08-13 · homelab-firewall, **eighth and final pass** of the same day · took
  the caller's open routing question ("section or own page?") and answered it with
  the *reason* attached: **§7 of [[remote-network-change-without-lockout]]**, because
  the finding shares that page's premise (a change that can sever your own control
  path) and its safety furniture (armed auto-revert, rollback by handle via comment)
  — and wrote the distinction **into the section's first line** so both halves stay
  legible: **§1–§6 protect the *recovery*, §7 protects the *decision to flip***.
  Strengthened the caller's generalisation by finding it already had an independent
  instance in the wiki one layer down ([[routeros-vlan-filtering-live-rollout]]
  stages the whole bridge-VLAN table while `vlan-filtering=no` keeps it inert) and
  cross-linking the two — a general rule with two device classes behind it is a rule,
  with one it is an anecdote. Added **two boundaries the green test does not cover**
  (zero drops prove only what was exercised → keep the log rule permanently; and a
  **broad** rule inside the allow-list lets the flip pass while the real risk stays
  open) — the second one is exactly this session's own residue. Handled the
  deliberately unfinished half as the caller demanded: backlog 10 went from ⚠️ OPEN
  to 🟡 *outer half done, inner open* **with the reasoning and the next step**, and
  the caveat is repeated at **four** places (pattern §7, topology isolation model,
  backlog, index status block) so "output is default-deny" cannot be read as the
  whole job anywhere. Kept invented syntax out of the as-built table (the caller gave
  seven rules and two port sets, not seven command lines) — descriptive rows where
  the exact form was not reported. 0 broken wikilinks; only `Wiki/` staged; not
  pushed, per instruction.

- 2026-08-13 · homelab-firewall, **ninth and closing pass** of the same day ·
  two merges, no new page — and both merges were placed against the caller's
  own routing hint rather than with it, with the reason written down. (1) The
  "changed instrument" lesson went to
  [[measure-from-the-position-of-the-complaint]] as **rule 4** (the caller
  offered "section or sub-rule on the rule-10 material" and left the judgement
  open): the *page* already owns the instrument dimension, so rule 4 reads as
  the counter-direction to rules 1–3 (*where* you measured ↔ *what you changed
  about the meter*) — but in the **checklist** it deliberately did **not**
  become a rule 11: [[fehlersuche-grundregeln]] rule 7 already carries *"a new
  watchdog is checked against a known state first"*, and a changed instrument
  **is** a new instrument, so the bullet was widened to "neu **oder geändert**"
  instead of duplicating a rule. (2) The threshold lesson became the guardrail's
  **counter-rule** — the sharpest thing that can happen to a guardrail is a
  documented case of deliberately *not* applying it, so
  [[measurement-without-a-target-is-not-monitoring]] now carries § *When a
  threshold must not be built* **and** an explicit boundary against its own
  Escalation bullet (do not widen the band until it never fires when the
  *instrument* is the unreliable part). Kept the two same-hour reverts honest at
  three places (they are the agent's own mistakes, made *after* the preventing
  rules were filed the same day) and turned the caller's "not done, deliberately"
  into a **stated** backlog decision (12c) rather than a silent skip; also
  back-annotated backlog 12(a), whose recommended multi-endpoint fan-out is
  exactly the "improvement" that was measured and reverted — so the profile no
  longer recommends what the session refuted. Corrected the index's now-false
  blanket claim ("no target comparison on any throughput **or link** metric").
  0 broken wikilinks; only `Wiki/` staged; not pushed, per instruction.

- 2026-08-15 · homelab-firewall SFP-Modul + Härtungs-Nebenwirkung · **zehn Kandidaten,
  zwei neue Seiten** — der Rest ging dorthin, wo das Thema schon wohnt, und die
  Begründung steht jeweils dabei. (1) Die drei Modul-Lehren wurden **eine** Seite
  ([[copper-sfp-module-link-needs-autoneg-off]]): „Rate am Konverter = Host-Seite" und
  „Modul gehört ans langsame Ende" treten *nur* im Kontext desselben Bauteils auf, also
  Abschnitte statt dünner Einzelseiten — die verallgemeinerbaren Hälften wurden
  stattdessen dort verankert, wo sie ohne das Bauteil gebraucht werden
  ([[throughput-is-a-path-property]] zwei Prüfschritte,
  [[measure-from-the-position-of-the-complaint]] eine Tabellenzeile). (2) Beim
  `advertise=`-Fund **keine neue Regel 11** in [[fehlersuche-grundregeln]]: Regel 5 ist
  exakt „geschrieben ≠ aktiv", und ein `set`, das stumm filtert, ist ihre kleinste
  Form — die *Seite*, die den Fehlertyp besitzt, ist [[routeros-import-can-fail-silently]],
  die dadurch von „`/import` ist unzuverlässig" zu „RouterOS bestätigt nicht, was es
  gespeichert hat" wächst. (3) Der Timer-Fallstrick kam mit seiner **Asymmetrie**
  ins Muster (*Revert*-Timer startet mit dem Risiko, *Vorwärts*-Timer mit dem Menschen),
  und sein Mess-Zwilling — ein 25-Sekunden-Fenster, das niemand angekündigt hatte —
  landete bei der Messmethodik, nicht beim Scheduler: das eine ist ein Ausführungs-,
  das andere ein **Beweisfehler**. (4) Beim Drucker-Vorfall war die Versuchung, ihn als
  Anlagen-Notiz abzulegen; er ist aber ein Muster (zweite Instanz am selben Tag: ein AP
  im geschlossenen Port) und bekam eine eigene Seite mit der korrigierten Definition
  von „ungenutzt" — **Bestand = Reservierungsliste, nicht Link-Zustand** —, plus dem
  ehrlichen Teil: der Ping-Sweep über sechs Segmente war die eigene Fehldiagnose,
  während die feste `dhcp-host`-Zeile die ganze Zeit widersprach. (5) A10 („Absicht an
  das Objekt kommentieren") wurde **kein** eigener Eintrag, sondern der
  Umsetzungs-§ der Regel, die ihn verlangt — und an das bereits existierende
  Spiegelprinzip gekoppelt (nftables-Kommentar = *Identität*, Port-Kommentar =
  *Absicht*), mit dem cross-tool-Argument, dass ein fremder Agent die Wiki-Konvention
  nicht kennt. Faktenkorrektur-Sweep gefahren, weil die Anlage sich unter frisch
  geschriebenen Seiten geändert hatte (Etagenstrecke 2,5G, 18 statt 21 geschlossene
  Ports, Portbelegung, Backlog 3d ⚠️→🟡) — und der **letzte Hop bleibt ausdrücklich
  offen**, inklusive der Warnung, dass die 2,5G am SFP-Port die Host-Seite sind und die
  Anforderung erst am PC erfüllt ist. Datenschutz: MAC/IP/Reservierung des Druckers und
  alle Portzuordnungen nur in `.memory/` (git-ignoriert), im Wiki Platzhalter.
  0 kaputte Wikilinks.

- 2026-08-16 · knowledge-wiki-engine public-mirror rebuild + document production ·
  **five candidates → 3 new pages, 4 extensions**, and the pass's real work was refusing
  two new pages. (1) The leak-check material did **not** become a page: the caller had
  already routed it as an extension, and it belongs there for a sharper reason than
  proximity — [[public-demo-mirror-of-private-repo]] *already contained* the correct
  advice ("neutralize the map, it contains the private strings") and the repo leaked
  twice anyway, so the honest form is a **⚠️ block on that page saying its own advice was
  not enough**, not a second page that would read as if the first had never existed;
  the four enforcement changes (map out of the tool into a git-ignored `sync.map`,
  patterns *derived from* the map, `git ls-files` scope, no extension filter) are written
  as the *enforced version of step 2*, with the meta-lesson stated first. (2) Split the
  same session's publish failures away from the recipe into a guardrail
  ([[publish-gate-must-fail-closed]]) because they are not about *sanitizing* but about
  **how a gate is invoked** — a pipe that replaces the exit code, and `git add -A`
  sweeping in the gate's own aborted-run artifact — and named the family out loud
  (cross-linked to [[silent-except-hides-dead-features]]: the error signal exists and is
  converted away before anyone sees it). (3) The cross-model material went to **three**
  homes rather than one page: the prompt shape earned its own methodology page
  ([[adversarial-review-binary-verdict]] — the cap of 3 and the word "blocker" are the
  mechanism, and the REJECT→APPROVE flip is the signal), the "never state regulatory
  dates from model memory" lesson extended [[no-unverified-assumptions]] — where it also
  earned a **third option** beside its existing "sources conflict → escalate": *delete the
  disputed detail*, because picking the likelier source **is** the assumption the
  guardrail forbids — and the channel facts (credits exhausted → Codex CLI as standby;
  the model/version trap running **the other way**, a default model newer than the
  installed CLI) extended [[codex-cross-model-integration]] as a mirror-image bullet
  beside the trap it inverts. (4) Kept the docx page's centre of gravity on
  *verification*, not generation — the three layout defects are only interesting because
  they were invisible in source and obvious in the render, which is why it is filed as an
  **environment** page and cross-linked to [[headless-preview-canvas-verification]].
  Honoured the caller's exclusion list (no fork URL, no chosen-topic list; measured counts
  kept only as the method's own output) but **kept the two commit hashes as provenance**,
  which the protocol requires of an experience page — reported as a deliberate deviation
  rather than done silently. No probation transitions: every skill/role used
  (`experience-capture`, `knowledge-recall`, the Codex channel) was already active.
  0 broken wikilinks.

- 2026-08-16 · AI-governance deliverable + wiki machinery · **three layers for one
  session**, and the pass's discipline was *keeping them apart*: the sourced legal
  facts went to `knowledge/` ([[ai-regulation-for-deployers-eu-de]]) — deliberately
  **not** `experience/`, since a legal fact has no verifier to be green — while the
  synthesis, the second-hand attributions and two unexamined suspicions went to the
  journal, each with a **status and a dated review**, which is the ADR's own
  lifecycle argument applied to the page that records it. Wrote the **caveats as
  caveats**: two disputed details (the act's entry-into-force day, the MaRisk
  *Novelle* ordinal) are **missing on purpose** with the reason stated in-page, per
  [[no-unverified-assumptions]] — and, applying the same rule unprompted, left out
  DORA's CELEX number and the SCHUFA case number because they were not supplied and
  a norm reference from model memory is exactly what the guardrail forbids. Held the
  line on scope in the other direction too: the `sync.ps1` suspicion was **left
  uninvestigated** (another repo) rather than resolved on the way past. On the ADR
  the only real find was **numbering** — it was written as 0003, a number already
  taken → renumbered to 0005 with the reason in its own header, decision and
  consequences untouched; the single additive edit (a `Related pages` link to the
  journal) is also what removed its orphan warning. Dedup ran by grep, not
  `search_notes` — this subagent had no MCP tools — and is reported as such rather
  than implied. `wiki-audit` green (0 errors); no probation transitions (librarian
  only).

- 2026-08-16 · knowledge-wiki-engine recall telemetry · **three learnings → 1 new page,
  2 extensions**, and the pass's judgement was **not** giving the negative-test lesson its
  own page: the caller left "same page or a sibling" open, but the target page's headline
  rule *is* "prove every new code path fires once", so the complement ("…and prove it does
  **not** fire when it must not") belongs **inside** it as the correction of its own rule —
  a sibling would have left the wiki with two half-rules. Sharpened the escalation instead
  of restating it: the swallowed exception here sat in a **measurement**, so the failure is
  not a dead feature but a **lying instrument** — "a dead feature produces no output and
  someone notices; a dead meter produces zeros, and zeros look like measurements" — with the
  fix shape (`telemetry_errors` **in the stats payload**, WAL + `busy_timeout`, telemetry may
  fail soft but never silent). Made the sister-rule link to [[publish-gate-must-fail-closed]]
  **reciprocal and specific** (pipe converts the exit code away ↔ `except` converts the
  exception away; its rule 5 is the guardrail form of the negative-test rule) rather than
  leaving the generic "same family" line that was already there. On the new pattern page kept
  the **limits** as prominent as the recipe (it measures attention, not correctness; a *good*
  summary suppresses the very signal that would reward it; no automatic lifecycle decisions —
  review queue, per [[cascaded-agent-memory]]). Wrote the ranking change into
  [[local-recall-engine]] as a **convention change, not a feature note**: the protocol's
  "Historical (retained, no longer current)" marker used to be human-readable only and now
  bites (demotion ×0.6, **not** hiding), so marking a page historical is henceforth a
  retrieval decision. Honoured the exclusion: the "`log.md` dominates full-text recall"
  observation was **not** filed — one data point, already journalled with a 2026-08-30
  review. Deliberate non-action reported instead of done silently: `WIKI_PROTOCOL.md`'s
  Historical section still describes the marker as ranking-neutral, but editing it is a
  machinery change carrying the engine-mirror obligation → raised as a follow-up. Latent
  conflict surfaced, not filed: `Type: tombstone` matches the demotion markers while the
  protocol wants tombstones surfaced **prominently** (no tombstone page exists yet, so it is
  unobserved). `wiki-audit` green (243 pages, 0 errors, 0 warnings); no probation
  transitions (acting roles not reported → not assumed).

- 2026-08-16 · knowledge-wiki-engine usage backfill + transcript sweep (**second batch
  of the day**) · **2 new pages, 2 extensions, 1 promotion** — and the pass's real work
  was three discriminations. (1) Kept the backfill methodology as its **own** page rather
  than folding it into [[link-history-from-kernel-events-not-polling]], which already owns
  a "backfill trap": that page seeds a new counter from the **same** ephemeral source it
  replaces (against a falsely reassuring "0 events" on day one), the new page finds a
  **different** artefact that happened to be recording all along — same family, different
  move, so cross-linked both ways instead of merged. (2) Split the session's two mining
  results by outcome, not by session: the backfill *worked* and became methodology, the
  blanket retro-classification *failed* and became methodology too — the negative result is
  the load-bearing half ("the scarce resource is judgement, not extraction"), and the page
  says so in its title. (3) Gave the label-collision defect to
  [[derived-usage-signals-not-self-reports]] as a section rather than a page: correct
  counters plus a confusing report is a **reporting** failure of *that* instrument, and it
  came with a same-family corollary (two definitions under one column heading) that ties it
  to the blended-vs-live rule. On the **promotion**, recorded the uncomfortable part rather
  than tidying it: the pre-agreed trigger for item 3 (`surfaced_never_read`) **never fired**
  — `log.md` *is* read (49×) — and what actually settled it was the hit/read **ratio**
  (127 hits, the most of any page); a decision rule written before the data can be wrong
  about the shape of the evidence and right about the question, and that is now on the page.
  Marked the move explicitly as the **first application of the journal lifecycle** that
  [[0005-attested-promotion-into-the-experience-layer]] proposes instead of a quarantine
  layer, including what it cost (one edit + a paragraph in the target page). Numbers filed
  as evidence with their **limits attached** (regex themes = lower bounds; the corpus
  horizon is the disk, not the history; the project directory is the working directory, not
  the topic — 290 of 332 hits sat under an unrelated project). No owner message quoted; the
  complaint themes are recorded, never their content. `wiki-audit` green (245 pages, 0
  errors, 0 warnings); only `Wiki/` staged; not pushed, per instruction. Engine-template
  mirror still outstanding and reported, not done unasked.

- 2026-08-16 · knowledge-wiki-engine public release (**third batch of the day**) ·
  **three learnings, zero new pages** — all extensions of their canonical homes, as routed
  by the caller: two sibling instances onto [[no-unverified-assumptions]] (README example
  output pasted from a live run, never invented; license texts fetched from the canonical
  source, never from model memory), the 90-second stranger test as the **second proven
  prompt shape** on [[adversarial-review-binary-verdict]] (with the shared mechanism named:
  forcing a format forces findings), and the matching one-line win on
  [[codex-cross-model-integration]]. Handled ADR 0005 on a MODIFIED pre-rule experience
  page with `Verified by: legacy` — no attestation ids invented; the pages state honestly
  that the doc runs were real but were not verifier executions. Honoured the exclusion
  (release process + dual licensing not filed — legal fact-of-the-day, not verified dev
  experience). `wiki-audit` green (245 pages, 0 errors, 0 warnings); committed, not pushed.

- 2026-08-16 · homelab configuration review (**fourth batch of the day**) · **four
  learnings, 2 new pages + 2 extensions**, and the pass's judgement was mostly about
  *which failure each one actually is*. (1) The ICMP finding went onto
  [[measurement-without-a-target-is-not-monitoring]] as a **sibling rule**, not a new
  page: that guardrail owns "a measurement without an expected value is not a check",
  and "the wrong probe is not a measurement either" is its mirror image — filed with
  the sharper half named, that this failure is **worse** than the one the page already
  covers, because a probe nobody must answer does not stay silent, it emits a confident
  number ("9 of 12 offline") that nearly deleted two live DHCP reservations. (2) The
  `ether9` material could have been read as a *new* rule and is not: it is the
  **inverse** of [[disabled-port-looks-like-a-dead-device]] (there the observer's own
  change made a device look dead; here a label made an unobservable port look empty) and
  it belongs inside that page — with the generalisation stated as **"an assumption a
  correct measure does not need must not enter its justification"**, which is the
  transferable half and is *not* about switches at all. Recorded honestly that the
  correction came from the **owner applying the wiki's own rule to the agent**. (3) The
  parser page was written around the **discrimination**, not the bug: the finding
  *count* is the weak tell (a broken tool can produce exactly one plausible finding),
  the **impossible value** in the output is the strong one — and the page was placed as
  the third member of the lying-instrument family with the distinction spelled out (a
  dead feature is noticed; a broken analyser produces output that looks exactly like
  work, and acting on it changes a healthy system). (4) The filename guardrail kept its
  incident's teeth by listing **what the misnamed file was missing** as a table of
  consequences rather than as a story, and by stating that nothing was actually broken —
  the danger is entirely in the name. Held two lines: the requested cross-link to a
  "nested-escaping gotcha filed earlier today" was **not made**, because grep over
  `Wiki/` and today's commits shows no such page — a fabricated wikilink is a broken
  link, so it was reported instead; and both experience pages carry `Verified by:
  legacy` with the reason in their Provenance (live device checks and repo work, **not**
  verifier runs) rather than an invented attestation id, exactly as instructed. Kept the
  two open items **open** in three places (project profile, as-built, index status): the
  stale EAP650 reservations are *pending removal*, not removed, and two wired reserved
  devices still have no documented port — which is precisely why "that port is free" is
  unprovable anywhere in this installation right now. Honoured the exclusion (repo
  consolidation not filed — project structure, already in the repos' `AGENTS.md` and
  ADR 0006). Privacy: RFC1918 masked in the house notation, a device label generalised
  where it named an employer, no env-file contents. Committed, not pushed.

## Related pages

- [[role-verifier]]
- [[role-wiki-critic]]
