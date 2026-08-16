#!/usr/bin/env bash
# Append-only event log for guardrails — so "does this rule actually bite?" becomes a
# question with an answer instead of an impression.
#
# Measured on this system: the owner's most frequent complaint over 51 days was that rules
# do not bite, and for two of the three top complaints a guardrail already existed. Nobody
# could tell which rules were working, because nothing recorded whether they ever ran.
#
# Source it and call gr_log:
#     . "$(dirname "$0")/guardrail-log.sh"
#     gr_log <guardrail-slug> <checked|blocked|violated|bypassed> [detail]
#
# Events:
#   checked  — the control ran and let the action through
#   blocked  — the control ran and STOPPED the action (the rule earned its keep)
#   violated — the rule was broken and noticed afterwards (advisory rules, owner reports)
#   bypassed — the control was deliberately skipped (--no-verify and friends)
#
# The absence of events is itself a signal: a push that landed with no preceding `checked`
# was not gated. Do not delete this file to "clean up" — it is the evidence.
GUARDRAIL_LOG="${GUARDRAIL_LOG:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/recall-mcp/guardrail-events.jsonl}"

gr_log() {
  local slug="${1:-unknown}" ev="${2:-checked}" detail="${3:-}"
  local ts repo
  ts="$(date -Iseconds 2>/dev/null || date)"
  repo="$(git rev-parse --show-toplevel 2>/dev/null || echo '-')"
  detail="${detail//\"/\'}"; detail="${detail//$'\n'/ }"
  mkdir -p "$(dirname "$GUARDRAIL_LOG")" 2>/dev/null
  printf '{"ts":"%s","guardrail":"%s","event":"%s","repo":"%s","detail":"%s"}\n' \
    "$ts" "$slug" "$ev" "$(basename "$repo")" "${detail:0:200}" >> "$GUARDRAIL_LOG" 2>/dev/null || true
}
