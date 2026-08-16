# Guardrail — sweep for secrets *before* migrating any old code to a git host

**Summary**: Before pushing any pre-existing code convolution — personal archives, old private forks, foreign-account clones, backup folders, "legacy" project drops — to **any** git host, including a private self-hosted one, run a broad secret-pattern sweep first. "Private" is not a security control: SSH keys can be stolen, backups leak, the instance may later change visibility, and operators may export or migrate the repos.

**Trigger**: A GitHub→self-hosted-GitLab migration of ~17 repos + several nuggets + a 240 MB legacy archive finished with a "we're done" moment. A secret sweep run *after* that moment surfaced a real OpenAI API key **and** a real AWS access key in the archives — both had to be revoked at the vendor, then purged from history via [[git-history-secret-purge-recipe]]. The sweep would have caught them pre-push at a fraction of the cost. (2026-07-03)

**Scope**: Every migration/import of pre-existing code into any git host — public *or* private. Applies to Claude, Codex, and any other agent driving a migration.

**Last updated**: 2026-07-22

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: single incident — dated in Trigger

---

## Rule

**Before the first `git push` of any migration/import, run a broad secret sweep across the entire source tree(s).** Do not defer this to "we can rewrite history if we find something later" — history rewrites are expensive, revoke-and-rotate is disruptive, and the exposure window between push and discovery can never be undone.

Recommended sweep patterns (grep/ripgrep against the working tree, and separately against `git log -p` if the source is already a git repo):

- **OpenAI**: `sk-[A-Za-z0-9_-]{20,}` (both classic and `sk-proj-…` forms)
- **AWS access key ID**: `A(KIA|SIA|GPA|IDA|ROA|IPA|NPA|NIA|CA|KP|3T)[A-Z0-9]{16}` (the full AWS prefix table — not just `AKIA`)
- **AWS secret access key** (contextual): 40-char base64-ish next to a key ID; harder to regex safely, but pairs of hits often appear together
- **Google API**: `AIza[a-zA-Z0-9_-]{35}`
- **Google OAuth**: `[0-9]+-[a-z0-9]+\.apps\.googleusercontent\.com`
- **Slack tokens**: `xox[baprs]-[a-zA-Z0-9-]+`
- **GitHub PAT (classic)**: `ghp_[a-zA-Z0-9]{36}`
- **GitHub fine-grained PAT**: `github_pat_[a-zA-Z0-9_]{80,}`
- **Private keys**: `-----BEGIN (RSA|OPENSSH|EC|PGP|DSA|ENCRYPTED)? ?PRIVATE KEY-----`
- **Bearer tokens** (contextual): `Bearer [a-zA-Z0-9._-]{20,}`
- **Hardcoded passwords** (contextual): `["']?password["']?\s*[:=]\s*["'][^"']{4,}["']`
- **JWT tokens**: `eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}`
- **Twilio**: `AC[a-f0-9]{32}` / `SK[a-f0-9]{32}`
- **Stripe**: `sk_live_[a-zA-Z0-9]{24,}` / `pk_live_…`
- **npm token**: `npm_[a-zA-Z0-9]{36}`

If the source is *already* a git repo, run the sweep against **all reachable content**, not just the tip:

```bash
for pat in "$patterns"; do
  git log --all -p -S "$pat" --oneline | head
done
# or use a tool: gitleaks / trufflehog on the whole history
```

Tools that automate this well: `gitleaks`, `trufflehog`, `detect-secrets`. Use them; the pattern list above is a fallback so you can still sweep in a bare shell.

**Commit metadata counts as sweepable data.** Content sweeps miss it entirely: the git AUTHOR/COMMITTER identity (real name + email) lives in the commit **object**, not in any file. Before any push to a new host, check

```bash
git log --format='%an %ae %cn %ce' | sort -u
```

and neutralize if needed — `git commit --amend --reset-author` under a neutral identity (e.g. `<account>@users.noreply.github.com`) for a single-commit publish, or a history rewrite for multi-commit cases; verify via the destination host's API (commit.author fields), not just locally. (Added 2026-07-22: a public demo mirror passed the full content sweep and still leaked the real name + email in its commit object — see [[public-demo-mirror-of-private-repo]].)

## Checks before acting

- Have you run the sweep on the **complete** source tree — including any nested `_archive/`, `Backup/`, `.old/`, forks, and separate submodules?
- If the source is already a git repo: has the sweep covered **all reachable history**, not just the working tree?
- Is there any `.env`, `credentials.json`, `secrets.yml`, `*.pem`, `*.key`, `*.pfx` file in the tree that should be gitignored/removed before the push?
- Are large binary blobs (databases, PST/OST, log dumps) also sensitive? They can hide credentials too — either exclude or sweep.
- Have you checked the **commit metadata** (`git log --format='%an %ae %cn %ce' | sort -u`) — does the author/committer identity belong on the destination host?

## If a secret is found

1. **Revoke at the vendor first** (rotate the key, invalidate the token). This is the only step that actually reduces exposure.
2. **Redact + purge from git history** per [[git-history-secret-purge-recipe]]. Do not simply overwrite the current commit — the value stays in ancestors.
3. Only after revoke + purge + verified fresh-clone check, push to the destination.
4. If the source was ever public (or has been shared): assume compromise; monitor for abuse via the vendor's audit log for a reasonable window.

## Escalation

- If you find a secret you cannot revoke (someone else's account, or shared/team credentials): **stop and ask the owner** before pushing anywhere. Do not silently redact-and-push — the owner needs to coordinate rotation.
- If the migration is time-sensitive and a sweep-then-purge is impractical, either delay the push or push only to a *private* dead-letter repo with **no** users besides the operator until the sweep + purge are complete. "Private on the same host" is not a substitute — see the trigger above.
- If a category of secret slips a first pass (a novel token format not in the pattern list), extend this guardrail with the new pattern and re-file.

## Related pages

- [[no-secrets-or-private-account-data]]
- [[git-history-secret-purge-recipe]]
- [[public-demo-mirror-of-private-repo]]
- [[gitlab-default-branch-protection-destroy-recreate]]
- [[secure-repos-to-git-remote]]
- [[selfhost-gitlab-lowram-vps]]
