#!/usr/bin/env pwsh
# Bootstrap knowledge-recall-mcp from a fresh clone: create venv, install deps,
# build the index. Idempotent — safe to re-run.
$ErrorActionPreference = "Stop"
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $dir

if (-not (Test-Path ".venv")) {
  Write-Host "Creating virtual environment (.venv)..."
  python -m venv .venv
}
$py = Join-Path $dir ".venv/Scripts/python.exe"

Write-Host "Installing dependencies..."
& $py -m pip install --quiet --upgrade pip
& $py -m pip install --quiet -r requirements.txt

Write-Host "Building the recall index over the wiki..."
& $py server.py index

Write-Host ""
Write-Host "Bootstrap complete."
Write-Host "Next: register the MCP server (see README.md 'Use (MCP)') and restart your client."
