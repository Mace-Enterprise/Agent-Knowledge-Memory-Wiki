# Register a new MCP of ours in the registry — in the same change

**Summary**: When we add or configure a new MCP **of ours**, add a row to
[[mcp-registry]] in the same unit of work (and a project page for a substantial one),
so the catalog never drifts from what we actually run.

**Type**: guardrail
**Trigger**: an MCP we run is invisible to agents/skills until someone documents it; the catalog silently goes stale when a new server is wired up but not recorded.
**Scope**: any add/change/removal of one of **our** MCP servers (CLI `~/.claude.json` or desktop/surface). Claude's built-in host MCPs are out of scope.
**Last updated**: 2026-07-01

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: needs-review — trigger present but neither dated nor an owner directive

---

## Rule

When you add, reconfigure, rename, or retire one of **our** MCP servers, in the **same
change**:

1. Add / update / remove its row in [[mcp-registry]] (id, purpose, when-to-use,
   configured-where, status), and bump the registry's `**Last updated**`.
2. For a **substantial** MCP, also create or update its project page under
   `Wiki/projects/` and deep-link the registry row to it.
3. Keep the registry's `**Sources**` provenance honest (our `~/.claude.json` config +
   live `claude mcp list` verification + the per-MCP project pages).
4. Update `Wiki/index.md` / `Wiki/log.md` as usual for any navigation change.

The registry duplicates *know-how* (purpose, gotchas, status), **not** live state —
agents must still re-verify availability per session.

## Checks before acting

- Is this one of **our** MCPs (not a built-in host MCP)? If host/environment-standard, do not catalogue it.
- Does the registry row's status reflect reality (✔ / 🟡 / ✘) as of this change?
- For a substantial MCP: does a project page exist and is the row deep-linked to it?

## Escalation

If it's unclear whether a server is "ours" vs a built-in host MCP, or whether it's
substantial enough to warrant a project page, ask the owner before writing.

## Related pages

- [[mcp-registry]]
- [[trading-mcp-inventory]]
- [[machinery-sync-engine-template]]
