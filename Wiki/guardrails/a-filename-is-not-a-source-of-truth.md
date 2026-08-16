# Guardrail — a filename is not a source of truth

**Summary**: Which configuration file is **active** is decided by the thing that
loads it — the systemd unit, the service config, the import statement, the
include path — **never** by what the file is called. A file named
`…-production.conf` sitting next to the file the loader actually reads is a trap
that costs exactly one careless "let's use the production one": here that would
have **silently reverted weeks of firewall hardening**. Name backups after *what
they are and when*, never after what they aspire to be.

**Trigger**: homelab-firewall, 2026-08-16. During the configuration review,
`/etc/nftables-production.conf` was found beside `/etc/nftables.conf`. systemd
loads **the latter**. The file whose name said *production* was the **older,
weaker** variant:

| Missing in the `…-production.conf` file | Consequence had it been loaded |
|---|---|
| `ct state invalid drop` | invalid/spoofed-state packets accepted again |
| lateral-movement logging | the zero-baseline inside-detector goes blind ([[detect-lateral-movement-not-egress]]) |
| DNS enforcement for **four** VLANs (it had one) | three segments could pick their own resolver again |
| a hardened `output` chain (it had none at all) | the box's own egress back to `policy accept` ([[remote-network-change-without-lockout]] §7) |

Nothing was broken by it — the danger is entirely in the *name*, which invites a
future reader (or agent) to treat it as authoritative.

**Scope**: every host and repo where a loader selects one file out of several
similar ones — systemd units, `*.d` include directories, nginx/Apache sites,
`dnsmasq.conf` fragments, `.env` files, Kubernetes manifests, application config
search paths, CI workflow files, and any directory containing "backups" of a live
config.

**Enforcement**: advisory — no automated check; caught by the configuration
review

**Justification**: single incident, dated 2026-08-16 (homelab firewall
configuration review, config repo `810138b`)

**Last updated**: 2026-08-16

---

## Rule

1. **Ask the loader, not the directory listing.** Determine the active file from
   the mechanism that reads it:
   - systemd: `systemctl cat <unit>` → the `ExecStart` / `EnvironmentFile` line;
   - a daemon: its own `-f` / `--config` argument as actually invoked
     (`ps`, the unit, the wrapper script), plus every `include`/`conf-dir` it
     pulls in;
   - an application: the resolved import/search path, not the repo layout.
   Read that path, then confirm the *content* is what you expect.
2. **Never infer authority from a name.** `-production`, `-final`, `-new`,
   `-current`, `-good`, `-v2`, `-USE-THIS` are all statements someone made once,
   about a file, at a moment that has passed. They age; the loader does not.
3. **Name backups after what they are and when they were taken**, e.g.
   `nftables.conf.pre-hardening-2026-08-06`. That name states a fact
   (this is the state before that change) instead of an intention, and it sorts
   and expires legibly. A name that describes a *role* competes with the live
   file for authority.
4. **Move backups out of the loader's reach.** A `.disabled` suffix is not
   protection — several daemons read *every* file in their include directory
   regardless of extension ([[dnsmasq-duplicate-dhcp-option-and-conf-dir]]).
   Put the copy in a backup directory, not next to the original.
5. **Before renaming or deleting, prove nothing references it**, then prove the
   **active** file is still valid. Both steps were run here: a grep across units,
   scripts and configs found no reference, and the live ruleset was
   syntax-checked afterwards. A cleanup that breaks the boot path is worse than
   the confusing name it removed.
6. **When two candidate files exist, diff them before choosing** — and expect the
   difference to be *security-relevant*, because the reason a second copy exists
   is usually that someone changed the first one.

## Checks before acting

- **"Which file is live?" is answered by a command, not by a name.** If you
  cannot name the loader, you do not know which file is active — stop there.
- Before adopting, copying or restoring any config: `diff` it against the
  currently loaded one and read the deltas as *changes you are about to make*.
- After a hardening or migration wave, sweep the config directories for
  leftovers and rename them per rule 3 in the same change — the confusing name is
  created by the wave, not by the next reader.
- Same rule inside repos: a file called `config.production.yaml` proves nothing
  about which environment loads it. Check the deployment, not the filename.

## Escalation

If the file the loader reads and the file the *name* claims is authoritative
disagree in a security-relevant way, do not "tidy it up" silently. Report the
delta to the owner, state which one is live, and let the rename happen as a
deliberate step — the discrepancy itself is a finding about how the system was
changed, and it may point at an unfinished migration.

## Related pages

- [[disabled-port-looks-like-a-dead-device]] — the same mechanism on a device
  object: a port comment ("ZU - frei") was read as evidence, though it only
  preserved an assumption made while the device was off.
- [[dnsmasq-duplicate-dhcp-option-and-conf-dir]] — a daemon reading a file you
  did not intend it to read; the reason rule 4 exists.
- [[fehlersuche-grundregeln]] — Regel 5 (*written ≠ active*): this guardrail is
  its file-level form.
- [[single-source-of-truth-for-mutable-facts]] — two copies of a mutable fact
  will diverge; here the divergence was invisible because both had plausible
  names.
- [[remote-network-change-without-lockout]] — §7, the `output`-chain hardening
  that the misnamed file predates and would have undone.
- [[milestone-backup-during-infra-work]] — backups are required; this page says
  how to name and where to put them.
- [[homelab-firewall]] · [[raspberry-pi-network-topology]] — the project and the
  as-built state where this was found.
