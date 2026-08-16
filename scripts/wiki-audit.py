#!/usr/bin/env python3
"""wiki-audit — executable invariants for the knowledge wiki.

Turns the manual review checks into a runnable lint, so future agents can't quietly
drift from reality (the "no enforcement" risk).

Checks (ERROR = fails; warn = report only):
  - broken [[wikilinks]]                         (ERROR)
  - role brief missing a **Status** field        (ERROR)
  - roster count claim != actual role-file count (ERROR)
  - possible secret/credential in a page         (ERROR)
  - orphan pages (no inbound [[link]])           (warn)
  - recall index out of sync with page count     (warn; needs RECALL_DB)
  - role brief without a ~/.claude/agents adapter (warn; needs CLAUDE_HOME)

Usage:  python wiki-audit.py [WIKI_ROOT]      (default: current dir)
Env (optional, enable extra checks): RECALL_DB, CLAUDE_HOME
Exit code = number of ERRORs (0 = clean).
"""
import os, re, sys, glob, sqlite3

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
WIKI = os.path.join(ROOT, "Wiki")
errors, warns = [], []

def rel(f): return os.path.relpath(f, ROOT)

mds = glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True)
pages = {os.path.splitext(os.path.basename(f))[0] for f in mds}
roles = sorted(glob.glob(os.path.join(WIKI, "roster", "role-*.md")))

# 1) broken wikilinks + collect referenced targets (for orphan check)
link_re = re.compile(r'\[\[([^\]|#]+)')
referenced = set()
for f in mds:
    txt = open(f, encoding="utf-8", errors="replace").read()
    for m in link_re.finditer(txt):
        t = m.group(1).strip().split("/")[-1]
        if not t:
            continue
        referenced.add(t)
        if t not in pages:
            errors.append(f"broken link [[{t}]] in {rel(f)}")

# 2) role briefs must carry a **Status** field
for r in roles:
    if not re.search(r'^\*\*Status\*\*', open(r, encoding="utf-8").read(), re.M):
        errors.append(f"role missing **Status** field: {os.path.basename(r)}")

# 3) roster count claims must match the real number of role files
count_re = re.compile(r'(\d{1,2})\s+(?:generic|reusable|agent|pool)[^\n]*?roles?', re.I)
for f in (os.path.join(WIKI, "index.md"), os.path.join(WIKI, "roster", "index.md")):
    if os.path.exists(f):
        for m in count_re.finditer(open(f, encoding="utf-8").read()):
            if int(m.group(1)) != len(roles):
                errors.append(f"roster count says {m.group(1)} but {len(roles)} role files exist ({rel(f)})")

# 4) secrets / credentials (the guardrail pages legitimately describe the patterns)
secret_re = re.compile(
    r'(AKIA[0-9A-Z]{16}'
    r'|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY'
    r'|api[_-]?key\s*[:=]\s*["\'][A-Za-z0-9]{16,}'
    r'|password\s*=\s*["\'][^"\']{6,})', re.I)
for f in mds:
    if "no-secrets" in f or "security-audit" in f:
        continue
    if secret_re.search(open(f, encoding="utf-8", errors="replace").read()):
        errors.append(f"possible secret/credential in {rel(f)}")

# 5) orphan pages (warn) — never referenced by a [[link]] (index/log exempt)
for f in mds:
    name = os.path.splitext(os.path.basename(f))[0]
    if name in ("index", "log") or name not in referenced:
        if name not in ("index", "log") and name not in referenced:
            warns.append(f"orphan (no inbound [[link]]): {rel(f)}")

# 6) recall index freshness (warn) — needs RECALL_DB
db = os.environ.get("RECALL_DB")
if db and os.path.exists(db):
    try:
        n = sqlite3.connect(db).execute("select count(*) from notes").fetchone()[0]
        if n != len(mds):
            warns.append(f"recall index has {n} notes but wiki has {len(mds)} .md files - reindex")
    except Exception as e:
        warns.append(f"recall index check skipped: {e}")

# 7) machinery drift (warn) — role briefs vs ~/.claude/agents adapters
home = os.environ.get("CLAUDE_HOME")
if home and os.path.isdir(os.path.join(home, "agents")):
    briefs = {os.path.basename(r)[len("role-"):-3] for r in roles}
    adapters = {os.path.splitext(f)[0] for f in os.listdir(os.path.join(home, "agents")) if f.endswith(".md")}
    for b in sorted(briefs - adapters):
        warns.append(f"role brief '{b}' has no ~/.claude/agents adapter (drift)")

print(f"wiki-audit @ {ROOT}")
print(f"  {len(mds)} pages, {len(roles)} roles | {len(errors)} error(s), {len(warns)} warning(s)")
for e in errors:
    print(f"  ERROR: {e}")
for w in warns:
    print(f"  warn:  {w}")
sys.exit(len(errors))
