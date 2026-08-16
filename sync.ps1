#!/usr/bin/env pwsh
# Windows wrapper for sync.sh — refreshes this engine template from the live system
# via git-bash. See sync.sh for what it does. Review `git diff` afterwards, then push.
#
#   ./sync.ps1 -WikiSrc "D:/path/to/live/wiki" -RecallSrc "D:/path/to/knowledge-recall-mcp"
param(
  [Parameter(Mandatory=$true)][string]$WikiSrc,
  [Parameter(Mandatory=$true)][string]$RecallSrc,
  [string]$GptChatSrc = "",
  [string]$ClaudeHome = "$HOME/.claude"
)
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:WIKI_SRC = $WikiSrc
$env:RECALL_SRC = $RecallSrc
$env:GPTCHAT_SRC = $GptChatSrc
$env:CLAUDE_HOME = $ClaudeHome
bash "$dir/sync.sh"
