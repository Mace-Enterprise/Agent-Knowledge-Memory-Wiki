# Third-party skills/agents: security-audit before adoption

**Summary**: Anything we pull from GitHub or other external sources — a skill, an agent/role brief, a prompt, a snippet — must pass a security audit **before** it is adopted into our system (global `~/.claude` or a project team). External catalogs are "hiring catalogs" we recruit from on demand; we do not bulk-install.

**Type**: guardrail
**Applies to**: any acquisition of external skills, agents, prompts, or code — **including third-party binaries, packages and services installed on infrastructure** (firewall, router, always-on hosts)
**Owner**: the [[role-security]] runs/owns the audit
**Last updated**: 2026-08-13 (added: **when to engage the security role — proactively**, and the **name-the-trust-root** criterion)

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: needs-review — no trigger recorded at all

---

## Rule

1. **Clone to scratch, never into our git.** Pull external repos into a throwaway area outside all our repos (e.g. `<SCRATCH_DIR>/`). Never commit third-party code/content into the wiki, the engine, or a project repo.
2. **Audit before adopt.** Before any item enters `~/.claude` or a `TEAM.md`, the security role checks for:
   - **Prompt injection / hidden instructions** (e.g. "ignore previous", instructions to exfiltrate, embedded URLs/credentials, invisible unicode).
   - **Exfiltration / phone-home** — does it send data out, fetch+execute remote code, or add network calls?
   - **Destructive or over-broad actions** — `rm -rf`, force-push, mass edits; tool scopes wider than the task needs.
   - **Secret handling** — does it read/log env/keys? (cross-check [[no-secrets-or-private-account-data]]).
   - **Supply chain & license** — pinned deps? permissive license? maintained source?
3. **Assimilate, don't paste.** Rewrite the useful idea **in our own words** into our skill/role/wiki format (shrinks the injection surface — see skill-smith). Record **provenance** (source repo + commit) and the **audit verdict** on the page.
4. **Recruit on demand.** We do not need every skill/agent up front. Adopt only what a real, current need calls for; leave the rest in the catalog for later re-recruiting.
5. **Name the trust root.** "Verified" requires an answer to *what would an attacker have to compromise?* A sha256 **you computed yourself after downloading** is trust-on-first-use, not verification — it detects change on re-download and nothing else. Acceptable roots: an upstream-**published** checksum, signed repository metadata, or a public transparency log. Ranking, the APT-repo paradox, the middle path, and the containment for a binary that must run unattended: [[software-supply-chain-trust-roots]].

## When to engage the security role — proactively, not on request

**Trigger the audit yourself.** On infrastructure projects the security role is
engaged **before** the owner asks, whenever any of these is true:

- third-party **code, a binary, a package or a container** is about to touch a
  host everything else depends on (firewall, router, always-on server);
- a **new service** starts listening, or an existing one gains a new listener;
- a **new network path** is opened (a new port, a new egress destination, a new
  management plane, a new remote-managed device upstream);
- a **model artifact** is involved ([[third-party-model-gate]]).

Recorded because it failed once: on the homelab project the owner had to ask for
it ("*du solltest … auch immer wieder den Security Experten einbinden*") after a
proprietary measurement binary was already being weighed for the firewall. This
guardrail already required the audit — the failure was **not applying it
unprompted**. The audit that followed changed the outcome
([[0003-no-proprietary-speedtest-binary-on-the-firewall]]), which is exactly the
argument for running it before it is requested.

## Why

External skills/agents are executable instructions for our agents. An unaudited one is an untrusted code dependency with prompt-injection reach into our whole system. Treating sources as hiring catalogs (audit → assimilate → verify) keeps us fast without inheriting someone else's risk.

## Related pages
- [[no-secrets-or-private-account-data]]
- [[machinery-sync-engine-template]]
- [[software-supply-chain-trust-roots]] — what actually counts as verification.
- [[third-party-model-gate]] — the same gate for model artifacts.
- [[0003-no-proprietary-speedtest-binary-on-the-firewall]] — a decision this audit produced.
