# Guardrail — No secrets or private account data

**Summary**: Secrets, API keys, private credentials, private account data, and
unredacted sensitive logs must not be stored in this knowledge library and must
not be committed or pushed to GitHub.

**Trigger**: The owner explicitly required that no secrets, API keys, or private
account data are saved or uploaded.

**Scope**: All `Raw/`, `Wiki/`, `Templates/`, logs, journals, project profiles,
commits, pushes, and future imports into this repository.

**Last updated**: 2026-06-18

**Enforcement**: hook — leak-check.sh (engine) + wiki-audit secret regexes; logs events

**Justification**: owner directive, dated — 2026-06-18 (Codex session: founding GUARDRAILS instruction, no secrets stored or pushed)

---

## Rule

Never store or commit:

- API keys, tokens, passwords, private keys, seed phrases, cookies, or session
  identifiers;
- private account numbers, broker/account identifiers, customer data, or billing
  identifiers;
- unredacted sensitive logs, screenshots, exports, config files, or stack traces;
- environment files or settings that contain credentials.

This applies even when the data appears inside a chat export, GPT memory export,
debug log, screenshot, raw project note, copied terminal output, or pasted source
document.

## Required handling

- Redact sensitive values before adding material to `Raw/` or `Wiki/`.
- Replace secrets with placeholders such as `<redacted-api-key>` or
  `<redacted-account-id>`.
- Summarize the operational lesson without preserving the sensitive value.
- Keep credentials outside Git, e.g. in environment variables, local user
  settings, or the relevant secret manager.
- If a source cannot be safely redacted, do not import it.

## Checks before acting

Before writing, committing, or pushing:

- scan new/changed files for secrets and private account data;
- inspect `git diff` for accidental sensitive material;
- verify that raw imports and session journals are redacted;
- have [[role-security]] / Infosec review the wiki content before GitHub
  publication when imports, pasted exports, project profiles, logs, or sensitive
  topics changed;
- stop if uncertain whether a value is sensitive.

## Escalation

Stop and ask the human before continuing when:

- a source contains credentials or private account data;
- a task appears to require storing a secret in the repository;
- a log or screenshot may contain account identifiers;
- a GitHub push would include unreviewed raw imports or pasted chat exports.

## Related pages

- [[repo-boundary-llm-knowledge-library]]
- [[llm-knowledge-library-purpose]]
- [[project-boundaries-and-shared-experience]]
- [[role-security]]
