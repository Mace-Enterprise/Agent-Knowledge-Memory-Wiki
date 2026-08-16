---
description: Turn a request into a small, verifiable spec (Layer 1)
argument-hint: "<what you want to build>"
---

Write a spec for the following request using the **specifier** agent (Layer 1):

$ARGUMENTS

Dispatch the **specifier** agent: it recalls relevant wiki patterns, reads the
code the change touches, and produces `specs/<slug>.md` with verifiable acceptance
criteria mapped to `VERIFIER.md` steps. Present the spec for my acceptance before
any implementation. If the repo has no spec scaffold yet, suggest /karpathy-init.
