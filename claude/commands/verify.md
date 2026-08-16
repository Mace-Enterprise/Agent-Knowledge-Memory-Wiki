---
description: Run the repo's VERIFIER.md and report green/red per acceptance criterion (Layer 2)
argument-hint: "[optional: which spec or which checks]"
---

Verify the current change using the **verifier** agent (Layer 2).

Focus (optional): $ARGUMENTS

Dispatch the **verifier** agent: it runs `VERIFIER.md` (build + tests/checks
ONLY — never the live app or anything outward-facing) and reports a green/red
table mapped to the spec's acceptance criteria. On red, hand back to the
implementer; on green, offer to capture learnings with /learn.
