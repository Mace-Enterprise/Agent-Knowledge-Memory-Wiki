# knowledge-recall-mcp

Lightweight **hybrid recall** (keyword + semantic) over a markdown knowledge wiki,
as a local **MCP server** for Claude Code and Codex.

Recipe: **FTS5 + FastEmbed embeddings + sqlite-vec + Reciprocal-Rank-Fusion** —
local-first, no API key.

> For an agent-followable, "deploy this if it isn't already running" walkthrough,
> see **[DEPLOY.md](DEPLOY.md)**. This README is the human quick-reference.

## Recipe
- Keyword: SQLite **FTS5** (BM25).
- Semantic: **FastEmbed** `all-MiniLM-L6-v2` (384-dim, local) → **sqlite-vec** `vec0`
  (cosine), notes chunked ~2000 chars / 200 overlap.
- Fusion: **RRF** (K=60), deduped per note. Incremental re-index by content hash.

## Bootstrap (fresh clone → ready)
One command sets up the venv, installs deps, and builds the index (idempotent):
- Windows: `./bootstrap.ps1`
- macOS/Linux: `./bootstrap.sh`

Then register the MCP server (below) and restart your client.

## Use (CLI)
```
.venv/Scripts/python.exe server.py index             # (re)build the index
.venv/Scripts/python.exe server.py search "a query"  # hybrid search
.venv/Scripts/python.exe server.py read <path>       # print a note
```

## Use (MCP — for Claude/Codex)
Register in your MCP config (then restart the client). Tools: `search_notes(query,
mode, limit)`, `read_note(path)`, `reindex()`. Replace the paths and set `WIKI_DIR`:
```json
{
  "mcpServers": {
    "knowledge-recall": {
      "command": "<RECALL_MCP_DIR>/.venv/Scripts/python.exe",
      "args": ["<RECALL_MCP_DIR>/server.py", "serve"],
      "env": { "WIKI_DIR": "<WIKI_DIR>" }
    }
  }
}
```

## Config (env)
- `WIKI_DIR` — wiki root to index (default: the sibling `../Wiki` in this repo).
- `RECALL_DB` — index path (default: `recall-index.sqlite` here).
- `RECALL_MODEL` — FastEmbed model (default `sentence-transformers/all-MiniLM-L6-v2`;
  swap to a multilingual model if querying in German often).

## Notes
- `reindex` is manual (or wire it to run after wiki writes — see DEPLOY.md's hook).
  The index DB + venv + model cache are git-ignored.
- Recall order: this complements the wiki — it finds pages; the librarian curates.
