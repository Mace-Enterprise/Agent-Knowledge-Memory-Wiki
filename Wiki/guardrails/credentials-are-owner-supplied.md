# Guardrail — Credentials are owner-supplied; never write one into a file the owner is editing

**Summary**: An agent does not invent access credentials for the owner's devices —
the owner supplies them. If a value must be written into the owner's credential
store anyway, **read it back and find it again** before activating it on the device;
a secret that exists only on the device is a single point of failure, and on
appliances without password recovery it means factory reset plus full
reconfiguration.

**Trigger**: 2026-08-06, homelab AP commissioning. The agent generated an admin
password, appended it to the owner's credential file, then set it on the device. The
owner was **restructuring that same file at that moment** and replaced the block.
The password then existed nowhere: the device kept running but was unadministrable
for **both** parties. RouterOS has no password-recovery path → reset button + complete
reconfiguration from scratch.

**Scope**: Any agent action that creates, rotates, or stores an access credential
(device admin passwords, SSH keys, API tokens, PSKs) for the owner's systems — in
any repository or on any host.

**Last updated**: 2026-08-06

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: recurring incident — dated in Trigger, happened more than once

---

## Rule

1. **The owner supplies credentials.** Ask for the value, or hand a generated
   candidate to the owner **in the conversation** and let them place it. Do not
   silently write into their credential store.
2. **Never write into a file the owner may be editing right now.** A credential file
   is shared mutable state during a live session, exactly like a repository worktree
   ([[parallel-agent-collaboration]]) — last writer wins, and a whole-block rewrite
   destroys your append without any error.
3. **If a write happens anyway: write → read back → *find the value* → only then
   activate.** Re-reading the file is not enough; you must locate the exact value you
   wrote. Off-by-one/offset errors in a read-back check are real and have occurred —
   a read-back that "looks fine" without matching the value proves nothing.
4. **Never activate a credential on a device before the stored copy is confirmed
   findable.** Order matters: store and verify first, set on the device second. The
   reverse order is what turns a file mishap into a bricked appliance.
5. **A secret that exists only on the device is a single point of failure.** Before
   changing any credential, know the recovery path for that device class — and if
   the answer is "reset and reconfigure", treat the change as a risky operation.

## Checks before acting

- Is this credential something the owner can supply? (Default: yes — ask.)
- Is the owner currently working in the target file or on the target device?
- Where is the authoritative copy going to live, and who else writes to it?
- What is the recovery path for this device if the credential is lost? (Appliance
  firmware — RouterOS, switches, IPMI — commonly has **none**.)
- After writing: does a fresh read of the file contain the exact value? Did I match
  it, not merely re-read the file?

## Escalation

Stop and ask the human when:

- the credential store is being edited concurrently, or its structure is unclear;
- the read-back does not reproduce the value exactly;
- the device has no documented recovery path and physical access is not available;
- a credential is about to be rotated on a device that is the only path into itself
  (management-only-over-itself situations).

## Related pages

- [[no-secrets-or-private-account-data]] — what must never be stored in the wiki at
  all; this guardrail governs the operational side (who creates and stores a
  credential and in which order).
- [[parallel-agent-collaboration]] — the shared-mutable-state discipline this
  incident is an instance of.
- [[device-scoped-limited-api-keys]] — how credentials should be scoped when they do
  have to be distributed.
- [[detached-config-change-via-device-scheduler]] · [[remote-network-change-without-lockout]]
  — the other half of "don't lock yourself out of the box you are configuring".
- [[fehlersuche-grundregeln]] — rule 5: a written fix is not an active fix (here: a
  written secret is not a stored secret until you have found it again).
