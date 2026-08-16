---
title: Publishing is a content decision, not a string check
type: guardrail
status: active
created: 2026-08-16
---

# Publishing is a content decision, not a string check

**Rule.** Before anything of ours goes public, the gate must answer *two different
kinds of question*, and only one of them can be automated by pattern matching:

1. **Identifier question** — does this text contain a private path, a token, a
   machine name, a project name? A regex answers this.
2. **Content question** — is the knowledge in this page ours to give away? No regex
   answers this. It is a judgement, and it must be **written down per file**, or it
   does not happen at all.

A gate that only asks (1) will confidently pass a page that fails (2).

## Why this exists

The public template shipped eight pages derived from the owner's own projects —
trading role briefs, a market-data vendor's rate-limit knowledge, an
Electron-debugging recipe, a .NET test workflow. They were in from the **first
engine commit, 2026-06-18**, and the roster pair from **2026-06-27**. Two of them
were named explicitly in `sync.sh`'s allowlist, so someone had looked straight at
them and copied them on purpose.

Every leak check in that period passed. They were right to pass: the pages had
already been sanitized. `ExampleApp` had become `ExampleApp`, the vendor had
become `ExampleVendorSdk`, no path, no token, no name. **Sanitization defeats an
identifier check completely while leaving the knowledge fully intact** — that is
the whole failure mode. The owner had said "nur die Engine" repeatedly; nothing in
the machinery ever turned that into a question a file had to answer.

The fix that leaked, too: the first correction added
an exclusion list naming both trading role briefs to the *published* `sync.sh`. **An
exclusion list that names what it excludes republishes it.** The names moved into
the git-ignored substitution map — and the same trap caught this page and the
manifest one level up, where the "deliberately not shipped" note spelled them out
again. A rule about not naming something is not exempt from itself.

## How it is enforced

`content-manifest.txt` in the engine lists every `Wiki/**.md` that may ship, each
with one line saying why it is **machinery** — a description of how the memory
system works — rather than **domain knowledge**, whose value comes from a real
project's stack, vendor, or logic. `leak-check.sh` section 3 fails on any shipped
wiki page missing from that list, and `pre-push` runs the check against the tree
being pushed.

Adding a line to the manifest is cheap. That is deliberate: the cost is not the
typing, it is having to state the reason. Eight pages shipped for eight weeks
because nobody was ever made to write that sentence.

**Verified by** reinstating two of the eight removed pages into the tree: sections
1 and 2 of the check reported `clean`, section 3 refused to publish (2026-08-16).

## Applies to

Any publish target that leaves our control — the public template, a release
artefact, a gist, an issue attachment, a shared document. Ask both questions.

See [[publish-gate-must-fail-closed]] (the gate must not be bypassable) and
[[a-filename-is-not-a-source-of-truth]].
