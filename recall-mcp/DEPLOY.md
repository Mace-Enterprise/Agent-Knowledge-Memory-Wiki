# Deploying the recall MCP (agent guide)

**Audience: Claude (or another agent).** Follow these steps to make the
`knowledge-recall` MCP server available if it isn't already. Idempotent — safe to
re-run. Replace `<WIKI_DIR>` (the wiki root to index, e.g. the sibling `../Wiki`)
and `<RECALL_MCP_DIR>` (the absolute path to *this* folder).

## 0. Is it already deployed? (check first — don't redo work)
```
claude mcp list
```
- If `knowledge-recall` shows **✔ Connected** → it's deployed. Just keep the index
  fresh: `cd <RECALL_MCP_DIR> && .venv/Scripts/python.exe server.py index`. **Stop here.**
- If it's missing or failing → continue.

## 1. Bootstrap (venv + deps + first index)
Windows (PowerShell):
```powershell
cd <RECALL_MCP_DIR>
$env:WIKI_DIR = "<WIKI_DIR>"
./bootstrap.ps1
```
macOS/Linux:
```bash
cd <RECALL_MCP_DIR>
export WIKI_DIR="<WIKI_DIR>"
./bootstrap.sh
```
First run downloads the embedding model (~90 MB, once). A successful index prints a
page count.

## 2. Register the MCP server (user scope, so all projects see it)
```
claude mcp add knowledge-recall --scope user --env WIKI_DIR=<WIKI_DIR> -- <RECALL_MCP_DIR>/.venv/Scripts/python.exe <RECALL_MCP_DIR>/server.py serve
```
(On macOS/Linux the python path is `<RECALL_MCP_DIR>/.venv/bin/python`.)
For **Codex/GPT**, add the same `command`/`args`/`env` to its MCP config block
(see `recall-mcp/README.md` → "Use (MCP)" for the JSON shape).

## 3. Keep the index current automatically
Add a backgrounded reindex to the **wiki** repo's git hooks so every wiki commit
refreshes the index. In `<WIKI_DIR>/../.git/hooks/post-commit` (or `<WIKI_DIR>/.git/hooks/post-commit`
if the wiki root is the repo root), make it executable:
```sh
#!/bin/sh
# Keep the knowledge-recall index current after every wiki commit (incremental, backgrounded).
WIKI_DIR="<WIKI_DIR>" "<RECALL_MCP_DIR>/.venv/Scripts/python.exe" "<RECALL_MCP_DIR>/server.py" index >/dev/null 2>&1 &
```
The `experience-capture` skill also calls `reindex` after it writes a page.

## 4. Verify
- Restart the client (Claude Code / Codex).
- `claude mcp list` → `knowledge-recall` is **✔ Connected**.
- Call `search_notes("<a topic you just indexed>")` → returns ranked pages.

## Troubleshooting
- **`sqlite_vec` / `fastembed` import error** → re-run `bootstrap.*`; ensure Python ≥ 3.10.
- **0 pages indexed** → `WIKI_DIR` is wrong or empty; point it at the folder that
  contains your `.md` notes.
- **Slow first query** → the model loads lazily on first embed; subsequent calls are fast.
- **German queries** → set `RECALL_MODEL` to a multilingual FastEmbed model and re-index.
