---
description: Audit the knowledge wiki for correctness, freshness, and consistency (asks questions)
argument-hint: "[optional: section/category, or 'changed since <date>']"
---

Review the knowledge wiki using the **wiki-critic** agent.

Scope (optional): $ARGUMENTS

Dispatch the **wiki-critic**: it reads `Wiki/index.md` first, scopes the review to
stay token-frugal, runs the lint checklist plus provenance/freshness checks, and
reports findings with suggested fixes. It proposes — it does not rewrite pages.
Surface its questions to me; on my OK, hand fixes to the librarian.
