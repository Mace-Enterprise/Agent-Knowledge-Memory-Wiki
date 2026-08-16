# Guardrail — a publish gate must fail closed

**Summary**: A check that guards a publish (leak check, secret sweep, sanitizer verification) is only a control if a red result **stops the push**. Never pipe the gate (the pipe returns the *last* command's exit code, not the gate's), never publish the working tree (`git add -A` sweeps in artifacts the gate never saw), and remember that the sanitizer is itself subject to the check it performs. **The enforced form is a `pre-push` hook that checks the commit being pushed** — this page's own rules, written in the morning, were broken again by their author the same afternoon (§ below).

**Trigger**: While republishing a public demo mirror (2026-08-16) the same repo leaked private machine paths **three times in one day**. Every time the gate worked and the publish happened anyway: (1) `bash leak-check.sh | tail -n 1 && git push` — the check correctly printed `LEAK CHECK FAILED`, but the pipeline's exit code was `tail`'s `0`, so `&&` fired and the push went through; (2) a later `git add -A` swept up a leftover **test artifact from an aborted leak-check run** — a file containing the exact path the public repo had just been purged of — which was public for roughly two minutes; (3) in the afternoon, **after this page existed**, the same author piped the same gate into `tail` again and pushed over the red result — this time carrying 23 un-genericized files a dry run had left in the tree (commit `283d861`, repaired in `aecda9f`).

**Scope**: Any automated check that gates an irreversible or externally visible action — publishing a public mirror, pushing to a new remote, uploading a release, sending a report. Applies cross-tool (Claude, Codex, CI scripts, and hand-typed one-liners).

**Last updated**: 2026-08-16

**Enforcement**: hook — .githooks/pre-push refuses the pushed commit; logs events

**Justification**: recurring incident — dated in Trigger, happened more than once

---

## Rule

**1. Never pipe, tee, or wrap a gate.** Run it bare and branch on *its* exit code.

```bash
# WRONG — the pipeline's status is tail's, so a failing gate still publishes
bash leak-check.sh | tail -n 1 && git push

# RIGHT
bash leak-check.sh || { echo "gate red — not publishing"; exit 1; }
git push
```

If output must be shortened, capture it first (`out=$(bash leak-check.sh); rc=$?`) or use
`set -o pipefail` / `${PIPESTATUS[0]}` — but the default, reviewable form is *no pipe at all*.
The same trap hides in `check && push || true`, in `try/except` around a subprocess call, and
in any wrapper that reports "done" because the wrapper succeeded.

**2. Publish from a checked tree, not the working tree.** The gate scans a set of files; the
publish must ship *that* set and nothing else. `git add -A` after a gate run is a different
set — it picks up whatever appeared since, including the gate's own debris. Prefer
`git archive HEAD` / an explicit file list / `git ls-files`, and **clean up test artifacts of
the gate itself** (an aborted run leaves fixtures containing exactly the strings you are
hunting).

**3. The tool that removes secrets contains secrets.** Sanitizers, substitution maps,
redaction tables, and the gate's own test fixtures hold the private strings by construction.
They must be *inside* the scanned set (or moved out of the repo entirely — see
[[public-demo-mirror-of-private-repo]]), never exempted from it.

**4. A gate that cannot run must fail, not pass.** Missing rules file, missing dependency,
timeout, empty pattern list, zero files scanned — all of these are **red**. Test this
explicitly: delete the rules file and assert a non-zero exit.

**5. Prove the gate fails.** A gate is not verified by a green run. Inject a known-bad string
and confirm a non-zero exit **and** that the offending line is printed. Green-only evidence
proves nothing about the branch that matters.

## Checks before acting

- Does the publish command depend on the gate's own exit status — no pipe, no `tee`, no
  wrapper swallowing it?
- Was the gate run against **the exact tree that will be published** (and after the last
  edit, not before it)?
- Are the sanitizer, its map/rules, and the gate's test fixtures inside the scanned set?
- Has the gate been proven to go red — injected bad string, and missing-rules-file case?
- Are there leftover artifacts from an aborted gate run in the tree? (`git status` before
  staging; never `git add -A` into a publish.)
- If a leak did reach the remote: the exposure window is not undone by a force-push — see
  [[public-demo-mirror-of-private-repo]] on SHA-reachable residual commits, and
  [[git-history-secret-purge-recipe]] if history must be cleaned.

## Why this shape of failure keeps recurring

The error signal existed and was converted away before anyone saw it. That is the same family
as [[silent-except-hides-dead-features]] (a broad `except` turns a permanent bug into a
plausible-looking absence) and [[unattended-job-failure-alert-on-output-channel]] (a job that
fails quietly looks like a quiet day). Here the conversion is a **pipe**: an exit code, which
is the entire output that mattered, replaced by an unrelated one. When a signal is the only
thing standing between you and an irreversible action, check what happens to that signal on
its way to the decision.

## The enforced form — a pre-push hook

Everything above is a rule, and a rule was not enough: it was written in the morning and
broken by its own author the same afternoon, by the same mechanism. Between the two there
was no new information. The page is a file; nothing loads it at the moment a shell command
is typed. **Compliance is not a control.**

The control belongs at the choke point. `.githooks/pre-push` in the engine repo:

- it checks the **commit being pushed**, not the working tree — exported with
  `git archive` into a temporary directory. Those two differ exactly when it matters: a
  dirty tree, a stale branch, an orphan publish branch built moments earlier;
- a **missing prerequisite refuses the push** (here: the substitution map). A check that
  cannot run is a failure, not a pass;
- deleting a remote ref is skipped — there is no tree to inspect;
- enable with `git config core.hooksPath .githooks`. A hook nobody enables is not a
  control either, so this belongs in the repo's bootstrap instructions.

Verified on all four paths, and the negative ones are the point: a commit carrying a real
path is refused with the offending line named, and a missing map refuses. A gate whose red
path was never demonstrated is not a gate.

This is the same move as [[0005-attested-promotion-into-the-experience-layer]] makes for
the experience layer: stop asking the author to assert that a check ran, and put the check
where the action passes through.

## Escalation

- If a gate goes red and the publish is time-critical: **do not bypass it**. Report the hit to
  the owner and let them decide; a bypass is an owner decision, never an agent's.
- If a leak already reached a public remote: stop, tell the owner immediately with the exposure
  window (from → to), then purge; treat anything credential-shaped as compromised and rotate
  per [[pre-migration-secret-sweep]].
- If the gate cannot be made to run in the publish path (no shell, foreign CI), do not publish
  manually "just this once" — raise it as a missing control.

## Related pages

- [[public-demo-mirror-of-private-repo]] — the publish recipe this gate protects
- [[pre-migration-secret-sweep]] — what to sweep for before any push to a host
- [[git-history-secret-purge-recipe]] — cleanup when something did get through
- [[silent-except-hides-dead-features]] — the **sister rule** and same family: there a broad
  `except` converts the error signal away instead of a pipe. Its two later sections sharpen
  this page's rule 5 in the other direction — the *negative* test is the one that carries the
  proof — and name the worst variant: when the swallowed path is a **measurement**, the
  output is not a missing feature but a **plausible wrong number**.
- [[no-secrets-or-private-account-data]]
- [[secure-repos-to-git-remote]]
