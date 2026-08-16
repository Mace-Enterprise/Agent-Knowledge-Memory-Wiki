#!/usr/bin/env bash
# Fail-closed leak check for the public template.
#
# Two sources of forbidden strings:
#   1. the left-hand side of every rule in the substitution map (sync.map) — if a
#      string is worth replacing, it is worth failing the build over;
#   2. a generic pattern set (home dirs, drive paths, tokens, keys, IPs, e-mails).
#
# Scope: files that would actually be published — tracked files in a git repo,
# every file otherwise. Untracked build junk (.venv, worktrees, runtime logs) is
# deliberately out of scope; it never reaches the remote. The map file itself is
# excluded — it is git-ignored and must keep the real strings to do its job.
#
#   ./leak-check.sh [tree-root] [map-file]
#
# Exit 0 = clean, 1 = leak found (or map missing). Run before every publish.
set -uo pipefail

ROOT="${1:-$(cd "$(dirname "$0")" && pwd)}"
MAP="${2:-$ROOT/sync.map}"

# Placeholders and documentation examples are allowed to look like real paths.
ALLOW='path/to|yourname|<[A-Z_]+>|example\.(com|org)|YourProject|Your Live Wiki|YourDataVendor|0\.0\.0\.0|127\.0\.0\.1|noreply@|@anthropic'

cd "$ROOT" || exit 1

# Record that this control ran. A rule nobody can measure is a rule nobody can defend.
# shellcheck source=/dev/null
[ -f "$(dirname "$0")/guardrail-log.sh" ] && . "$(dirname "$0")/guardrail-log.sh"
type gr_log >/dev/null 2>&1 || gr_log() { :; }

# --- file list: what would actually be published ---
if git rev-parse --git-dir >/dev/null 2>&1; then
  mapfile -t FILES < <(git ls-files)
  scope="tracked files"
else
  mapfile -t FILES < <(find . -type f -not -path '*/.git/*' -not -path '*/.venv*/*' \
                            -not -path '*/node_modules/*' | sed 's|^\./||')
  scope="all files"
fi
# never inspect the map itself or this script
FILTERED=()
for f in "${FILES[@]}"; do
  case "$f" in sync.map|sync.map.example|leak-check.sh) continue ;; esac
  [ -f "$f" ] && FILTERED+=("$f")
done
echo "scope: ${#FILTERED[@]} $scope"

# grep -I silently skips anything it considers binary, so one stray NUL byte can hide a
# leak from this check. That is not hypothetical: it happened on 2026-08-16 and produced a
# green run over a file containing a real path. Refuse to be blind — report them instead.
binary=0
for f in "${FILTERED[@]}"; do
  if [ -s "$f" ] && LC_ALL=C grep -qP '\x00' "$f" 2>/dev/null; then
    echo "  NOT TEXT (skipped by grep, cannot be checked): $f"
    binary=$((binary + 1))
  fi
done
if [ "$binary" -gt 0 ]; then
  echo "  -> $binary file(s) unreadable by the text check; treat as unverified"
fi

scan() {  # scan <regex> -> prints hits, returns 0 if any hit
  printf '%s\0' "${FILTERED[@]}" \
    | xargs -0 grep -InIE -- "$1" 2>/dev/null \
    | grep -vE "$ALLOW"
}

leak=0

echo "== map-derived strings =="
if [ ! -f "$MAP" ]; then
  echo "  FATAL: no substitution map at $MAP"
  echo "  Copy sync.map.example to sync.map and fill in your real paths."
  exit 1
fi
n=0
while IFS= read -r line; do
  case "$line" in ''|'#'*) continue ;; esac
  pat="${line%% => *}"
  [ "$pat" = "$line" ] && continue
  n=$((n + 1))
  hits=$(scan "$pat")
  if [ -n "$hits" ]; then echo "$hits" | head -n 5; leak=1; fi
done < "$MAP"
[ "$leak" -eq 0 ] && echo "  clean ($n rules checked)"

echo "== generic secrets / machine paths =="
GENERIC='[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9._-]+'
GENERIC+='|[A-Za-z]:[\\/]+Sources'
GENERIC+='|/home/[a-z][a-z0-9._-]*'
# Kept in step with pre-migration-secret-sweep.md — that guardrail listed provider
# patterns this check did not have, which made the weaker of the two the one that ran.
GENERIC+='|glpat-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}'
GENERIC+='|github_pat_[A-Za-z0-9_]{20,}|sk-(proj-)?[A-Za-z0-9_-]{20,}'
GENERIC+='|(AKIA|ASIA|AROA|AIDA)[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}'
GENERIC+='|xox[baprs]-[0-9A-Za-z-]{10,}|https://hooks\\.slack\\.com/services/[A-Za-z0-9/]+'
GENERIC+='|eyJ[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}'
GENERIC+='|[Aa]uthorization: *[Bb]earer +[A-Za-z0-9._-]{20,}'
GENERIC+='|BEGIN [A-Z ]*PRIVATE KEY'
GENERIC+='|([0-9]{1,3}\.){3}[0-9]{1,3}'
GENERIC+='|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
hits=$(scan "$GENERIC")
if [ -n "$hits" ]; then echo "$hits" | head -n 15; leak=1; fi
[ "$leak" -eq 0 ] && echo "  clean"

echo "== content scope (machinery vs. domain knowledge) =="
# A string check cannot answer this one. Rename the project and every pattern goes
# quiet while the knowledge stays the owner's — which is how eight project-derived
# pages sat in the public template from the first commit. So the answer is written
# down per file in content-manifest.txt, and an unlisted page fails the check.
MANIFEST="$ROOT/content-manifest.txt"
if [ ! -f "$MANIFEST" ]; then
  echo "  content-manifest.txt missing — cannot decide what may ship"
  leak=1
else
  unlisted=0
  for f in "${FILTERED[@]}"; do
    case "$f" in Wiki/*.md) ;; *) continue ;; esac
    if ! grep -qF -- "$f " "$MANIFEST"; then
      echo "  UNLISTED: $f"
      unlisted=$((unlisted+1))
    fi
  done
  if [ "$unlisted" -gt 0 ]; then
    echo "  -> state in content-manifest.txt why each is machinery, or drop it"
    leak=1
  else
    echo "  clean ($(grep -c "|" "$MANIFEST") pages carry a written reason)"
  fi
fi

if [ "$leak" -ne 0 ] || [ "$binary" -gt 0 ]; then
  echo ""
  echo "LEAK CHECK FAILED — do not publish this tree."
  gr_log "no-secrets-or-private-account-data" "blocked" "leak-check refused a tree"
  exit 1
fi
gr_log "no-secrets-or-private-account-data" "checked" "${#FILTERED[@]} files clean"
echo ""
echo "leak check passed — tree is safe to publish"
