#!/usr/bin/env bash
# Write an attestation when a verifier passes — the second half of ADR 0005.
#
# Until now an experience page asserted "verified" and nothing stood behind the claim: the
# author typed it, the audit believed it. The point of an attestation is that the CHECK
# leaves the proof, not the author. So this wrapper runs the command, and only a green exit
# produces a record.
#
#     ./attest.sh <label> -- <command...>
#
# On success it prints the attestation id, e.g. att-2026-08-16-3f9a1c07. Put that id in the
# page:  **Verified by**: att-2026-08-16-3f9a1c07
# wiki-audit resolves it against the log and rejects an id that does not exist.
#
# The id carries a hash of timestamp+command+pid, so it cannot plausibly be invented from
# memory. That is the whole mechanism: not cryptography, just "you cannot write down an id
# for a run that never happened".
#
# The log is append-only evidence and is never committed.
set -uo pipefail

LOG="${ATTESTATION_LOG:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/recall-mcp/attestations.jsonl}"

label="${1:-}"
[ -z "$label" ] && { echo "usage: attest.sh <label> -- <command...>" >&2; exit 2; }
shift
[ "${1:-}" = "--" ] && shift
[ $# -eq 0 ] && { echo "usage: attest.sh <label> -- <command...>" >&2; exit 2; }

cmd="$*"
started="$(date -Iseconds 2>/dev/null || date)"
repo="$(git rev-parse --show-toplevel 2>/dev/null || echo '-')"
commit="$(git rev-parse HEAD 2>/dev/null || echo '-')"
dirty="clean"
git diff --quiet 2>/dev/null || dirty="dirty"

echo "attest: running -> $cmd"
"$@"
rc=$?
finished="$(date -Iseconds 2>/dev/null || date)"

if [ $rc -ne 0 ]; then
  echo "attest: command exited $rc — NO attestation written." >&2
  echo "        A failed verifier does not become evidence." >&2
  exit $rc
fi

sum="$(printf '%s|%s|%s|%s' "$started" "$cmd" "$$" "$commit" \
       | sha256sum 2>/dev/null | cut -c1-8)"
[ -z "$sum" ] && sum="$(date +%s | tail -c 9)"
id="att-$(date +%Y-%m-%d)-$sum"

mkdir -p "$(dirname "$LOG")" 2>/dev/null
esc() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr -d '\n'; }
printf '{"id":"%s","label":"%s","cmd":"%s","exit":0,"started":"%s","finished":"%s","repo":"%s","commit":"%s","worktree":"%s"}\n' \
  "$id" "$(esc "$label")" "$(esc "$cmd")" "$started" "$finished" \
  "$(basename "$repo")" "$commit" "$dirty" >> "$LOG"

echo ""
echo "attest: PASSED — attestation written"
echo "  id:   $id"
echo "  use:  **Verified by**: $id"
[ "$dirty" = "dirty" ] && echo "  note: worktree was dirty at verification time (recorded)"
