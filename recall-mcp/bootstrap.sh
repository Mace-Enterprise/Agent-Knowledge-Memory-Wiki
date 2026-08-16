#!/usr/bin/env bash
# Bootstrap knowledge-recall-mcp from a fresh clone: create venv, install deps,
# build the index. Idempotent — safe to re-run.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi
if [ -f .venv/Scripts/python.exe ]; then PY=.venv/Scripts/python.exe; else PY=.venv/bin/python; fi

echo "Installing dependencies..."
"$PY" -m pip install --quiet --upgrade pip
"$PY" -m pip install --quiet -r requirements.txt

echo "Building the recall index over the wiki..."
"$PY" server.py index

echo ""
echo "Bootstrap complete."
echo "Next: register the MCP server (see README.md 'Use (MCP)') and restart your client."
