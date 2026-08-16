# Agent orchestration options (2026): what fits a cross-tool, token-frugal team

**Summary**: For a local, cross-tool team (Claude Code + Codex + others) that minimizes tokens and wants self-improving agents, the answer is to stay **markdown/prompt-native** — no runtime framework. Use AGENTS.md as the contract, this wiki as shared memory, native subagents sparingly, and a verified self-improvement loop.

**Sources**: Web research, 2026-06-18 (see links below).

**Last updated**: 2026-06-18

---

## The decision

Two independent research passes converged: **do not adopt a runtime multi-agent framework** (LangGraph, CrewAI, AutoGen/AG2, OpenAI Agents SDK, Microsoft Agent Framework, Google ADK). They solve a *different* problem — orchestrating model API calls *inside one Python/.NET process* — and cannot make Claude Code and Codex collaborate as peer CLI agents. They also add infra we rejected and tend to be token-heavy (multi-agent runtimes can use ~15× the tokens of plain chat; conversational ones like AutoGen are worst) (source: Anthropic multi-agent research; Glean token-efficiency).

## Comparison (runtime frameworks)

| Framework | Runtime | Model | Infra weight | Token | Fit |
|---|---|---|---|---|---|
| LangGraph | Py/TS, state graph | agnostic | heavy (checkpointer + server) | medium | overkill |
| CrewAI | Py, role crew | agnostic | light | low (chatty) | misfit |
| AutoGen/AG2 | Py, group chat | agnostic | moderate | lowest (chattiest) | deprecated → MAF |
| OpenAI Agents SDK | Py/TS, handoffs | agnostic (OpenAI gravity) | light | high (leanest SDK) | closest SDK, still in-process |
| MS Agent Framework | Py/.NET, workflows | Azure gravity | heavy | medium | overkill/semi-locked |
| Google ADK | multi-lang, workflows | Gemini/Vertex gravity | light→heavy | medium | overkill |
| **MCP + A2A (protocol)** | any, local stdio | **agnostic** | **lightest** | **highest** | **best fit** |

The only genuinely cross-tool, vendor-neutral layer is the **protocol** (MCP for tools, A2A for agent-to-agent) — not a framework. Every framework above now speaks MCP anyway.

## Recommended combination (no framework)

1. **Contract = `AGENTS.md`** — the one file read by Codex, Claude, Cursor, Copilot, Gemini and 20+ tools (now stewarded by the Linux Foundation's Agentic AI Foundation). Keep it small; use nested per-subproject files. Point `CLAUDE.md` at it or keep them in sync. (source: agents.md)
2. **Shared memory = this wiki** — the highest-leverage token move: every agent reads prior conclusions instead of re-deriving them. This is exactly Anthropic's "subagents write to the filesystem and return a lightweight reference" pattern. (source: Anthropic context engineering)
3. **Execution = native subagents, used surgically** — each runs in its own context window and returns a ~1–2k-token conclusion, not a transcript. Powerful (orchestrator+workers beat single-agent by 90%+ in Anthropic's eval) but ~15× the tokens — so fan out deliberately, not by default.
4. **Self-improvement = adopt the pattern, own the loop** — search the library first → generate a skill only if missing → **verify** it → persist. This is the Voyager/OS-Copilot/SAGE result (SAGE reports +8.9% completion while cutting output tokens 59%). Gate every new skill behind a verification step before it enters the [[index]].
5. **Superpowers: cherry-pick, don't blanket-install.** It is MIT-licensed and its `writing-skills` meta-skill (TDD-for-docs: write failing pressure-tests → write the skill → tests pass → refactor) is the best "skills that write skills" discipline. But installed wholesale, its mandatory `using-superpowers` protocol preloads all skill metadata (open issue #190: ~22k tokens / 11% of context) and runs a full-ceremony cycle — both fight the token goal. Lift the *technique and skill texts*, not the plugin. (source: obra/superpowers, issue #190)

## How this maps to what we already built

- The [[index]] + experience pages = shared memory (point 2). ✓
- `specifier`/`implementer`/`verifier`/`librarian` subagents = surgical execution (point 3). ✓
- The librarian's "only file after a green verify" rule = the verification gate of the self-improvement loop (point 4). ✓
- Next additions: an **agent roster** under `wiki/roster/` (the "Agent Employees" catalog) and a **`writing-skills`-style discipline** for creating/improving agent & skill definitions, gated by verification.

## Related pages

- [[package-local-mcp-server-as-mcpb]]
- [[cdp-debug-electron-desktop-apps]]
