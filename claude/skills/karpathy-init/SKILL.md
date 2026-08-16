---
name: karpathy-init
description: >-
  Scaffold the Karpathy 3-layer development contracts into a repository — SPEC
  (specs/), VERIFIER.md, ENVIRONMENT.md — and wire them into AGENTS.md so every
  agent (Claude, GPT/Copilot, Codex) follows them. Use when a repo has no
  specs/VERIFIER.md/ENVIRONMENT.md yet, or when the user runs /karpathy-init.
  Generic across stacks (.NET, Node, Python, Go, Rust, other).
---

# karpathy-init

Generate the three tool-agnostic, in-repo contracts that make a project legible
to any agent. Output is plain markdown — no Claude-only syntax — so a parallel
GPT/Copilot agent benefits too.

## Safety: never destroy existing intent

- **Never overwrite** an existing `specs/SPEC.md`, `VERIFIER.md`, `ENVIRONMENT.md`,
  or `AGENTS.md` without first showing the user a diff and getting an OK.
- **Append** to an existing `AGENTS.md`; do not clobber existing pointers (e.g.
  ExampleApp's `project_instructions.yaml` references).
- If a contract already exists, offer to *update/refresh* it instead of recreating.

## Step 1 — Detect the stack

Look for these markers (a repo may have several; list them all):

| Marker | Stack | Build | Test | Run |
|---|---|---|---|---|
| `*.sln`, `*.csproj` | .NET / C# | `dotnet build <sln>` | `dotnet test` | `dotnet run --project <startup>` |
| `package.json` | Node/JS/TS | `npm run build` (if present) | `npm test` | `npm start` / `npm run dev` |
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python | `pip install -e .` / `uv sync` | `pytest` | `python -m <pkg>` |
| `go.mod` | Go | `go build ./...` | `go test ./...` | `go run .` |
| `Cargo.toml` | Rust | `cargo build` | `cargo test` | `cargo run` |
| none of the above | other | ask the user | ask the user | ask the user |

Read the actual scripts/targets (package.json `scripts`, csproj, Makefile, CI
files) and use the **real** commands, not the generic guesses above. Identify the
test project(s) and the startup project specifically.

## Step 2 — Recall before scaffolding

Use the **experience-recall** skill: check the wiki for existing `verifiers/` and
`environments/` recipes for this stack, and reuse them in the generated files.

## Step 3 — Generate the contracts

Create these files (lowercase paths as the repo prefers). Fill bracketed parts
from Step 1.

### `specs/spec-template.md`
```markdown
# Spec: <short title>

**Status**: draft | accepted | implemented | verified
**Owner**: <who>
**Updated**: YYYY-MM-DD

## Goal & success measure
The outcome to achieve and how we'll know it succeeded (the metric/observable).
Goal-driven: everything below serves this. Not "implement X" but "achieve Y, measured by Z".

## Intent
The refined request — what outcome, for whom, and why. Not how.

## Acceptance criteria
Each box is verifiable and maps to a VERIFIER step.
- [ ] <criterion 1> — verify: <how>
- [ ] <criterion 2> — verify: <how>

## Constraints / guardrails
Rules the change must respect (architecture, style, safety).

## Out of scope
What this change deliberately does NOT do.

## Verification hook
Which VERIFIER.md steps prove this spec is satisfied.
```

### `specs/SPEC.md`
```markdown
# Specs index

How we work: every non-trivial change starts as a spec here (copy
`spec-template.md`), gets accepted, then implemented, then verified.

## Active
- _(none yet)_

## Done
- _(none yet)_
```

### `VERIFIER.md`
```markdown
# Verifier — how correctness is decided

Automated checks decide "done", not vibes. Run these before claiming a change works.

## Build
- `<build command>`

## Tests
- `<test command>`  (fast subset: `<targeted test command>`)

## Lint / static checks
- `<lint command, if any>`

## Domain checks
- <project-specific verification, e.g. replay/reconciliation, golden files>

## Definition of done
- Build is clean, all relevant tests green, each acceptance criterion in the spec checked.
```

### `ENVIRONMENT.md`
```markdown
# Environment — how to run and observe

## Run
- `<run command>` (startup project/entry: <...>)

## Dependencies & how to mock
- <external services; how to run in mock/offline mode>

## Configuration
- <config file locations, local override, required env/secrets — names only>

## How to observe
- <logs, UI, screenshots, MCP bridges, data windows>

## Safety
- <anything an agent must NOT do automatically — e.g. never start the live app,
  connect to production, place orders, or touch real money/data>
```

### `TEAM.md` (the project's team)
Scaffold a starter team composed from the global pool (wiki `roster/`). Use the
wiki `Templates/team.md` shape. Hire the loop roles by default; add a domain-role
placeholder for the user to fill. Project-local Claude subagents for domain roles
go in `<repo>/.claude/agents/`. Keep it short:
```markdown
# Team — <project>
## Hired from the pool
- orchestrator, specifier, implementer, verifier, code-reviewer, librarian
## Domain roles (project-specific)
- <name> — <what/when>. Implemented by `.claude/agents/<name>.md`.
## Workflow
- orchestrator → specifier → implementer → verifier → code-reviewer → librarian
  (gate: green verify before done; user approves the spec).
```

### `.memory/` (per-project memory — cross-tool, local)
Scaffold the repo's **own** working memory — git-ignored, read by Claude **and** Codex,
indexed by recall alongside the wiki. Create `.memory/MEMORY.md`:
```markdown
# <project> — project memory (cross-tool, local)
Git-ignored working memory for **<project>**, read by Claude and Codex (referenced from
`AGENTS.md`). Complements the central wiki: durable/reusable knowledge → the wiki
(profile `Wiki/projects/<project>.md`); volatile, this-repo-only facts (bug state, local
paths, queued work) → here. Indexed by the `knowledge-recall` MCP alongside the wiki.
## Entries
- _(none yet)_
```
Then: add `.memory/` to `.gitignore` (volatile/private — never committed/pushed); and
register the dir in the recall reindex hook's `RECALL_EXTRA_DIRS` so `search_notes`
surfaces it during work on this project.

## Step 4 — Wire into `AGENTS.md`

Create `AGENTS.md` (or **append** a section if it exists):

```markdown
## Development loop (Karpathy 3 layers)

ALL agents (Claude, GPT/Copilot, Codex) MUST:
- Layer 1 — read `specs/SPEC.md` and the relevant spec before implementing.
- Layer 2 — run `VERIFIER.md` before calling a change done.
- Layer 3 — use `ENVIRONMENT.md` to run/observe the app.
- Team — see `TEAM.md` for this project's roles and workflow.
- Wiki — feed the shared knowledge library (see "Knowledge wiki" below).

Keep these contracts in sync with the code in the same change.

## Knowledge wiki — keep it fed

This project contributes to the shared knowledge library at
`<WIKI_DIR>` (canonical protocol: its `WIKI_PROTOCOL.md`).
Every agent (Claude, Codex/GPT, Copilot) working here MUST:
- Before non-trivial work: recall relevant prior pages (start at `Wiki/index.md`).
- After a verified change: capture reusable learnings — experience / knowledge /
  adr / guardrails — and update its `Wiki/index.md` + `Wiki/log.md`. (Claude: `/learn`
  or the `librarian` role.)
- Keep volatile, project-specific facts in this repo's `.memory/` (git-ignored, cross-tool — read by Claude *and* Codex, recall-indexed); start at `.memory/MEMORY.md`. Not the central wiki. Never store secrets.
```

(If this environment's knowledge-library path differs, set it once here — Codex and
other tools read this block, so the path must be explicit in the repo.)

If the repo already points agents at other instruction files (YAML, etc.), keep
those and add this block alongside — do not replace them.

## Step 5 — Report

List what was created vs appended, the detected stack(s) and the real commands you
filled in, and any `<...>` placeholders the user still needs to fill. Suggest the
first spec to write with `/spec`.
