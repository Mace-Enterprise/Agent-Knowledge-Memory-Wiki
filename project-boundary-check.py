#!/usr/bin/env python3
"""Detect cross-project contamination in per-project working memory.

Why this exists: a project without a working directory of its own has its work
done from somewhere else — and its session state, device facts and handoffs then
land in a FOREIGN project's `.memory/`. That happened here: homelab notes sat in
a trading project's memory and in the wiki's memory for weeks, unnoticed, because
nothing looked. Storage location is not project identity, and nothing was checking
the difference.

The check is deliberately dumb and therefore reliable: each project declares a few
marker terms that only it would use (device names, codenames, domain nouns). If
project A's memory contains project B's markers, that is a boundary violation.

    python project-boundary-check.py [--registry FILE] [--quiet]

Exit 0 = clean, 1 = contamination found (or a project has no working directory).
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = sys.argv[sys.argv.index("--registry") + 1] if "--registry" in sys.argv \
    else os.environ.get("PROJECT_REGISTRY", os.path.join(HERE, "project-boundaries.json"))
QUIET = "--quiet" in sys.argv

if not os.path.exists(REG):
    print(f"project-boundary-check: no registry at {REG}", file=sys.stderr)
    print("  A check that cannot run is a failure, not a pass.", file=sys.stderr)
    sys.exit(1)

_registry = json.load(io.open(REG, encoding="utf-8"))
projects = _registry["projects"]
problems, checked_files = [], 0
FIX = "--fix" in sys.argv

# --- identity reconciliation ------------------------------------------------------------
# Paths are not identities. Each project carries a `.project-id` whose id never changes;
# renaming or moving the directory must therefore not break anything. Walk the scan root,
# find the ids that actually exist on disk, and reconcile.
def _discover(root, depth=3):
    found = {}
    if not root or not os.path.isdir(root):
        return found
    stack = [(root, 0)]
    while stack:
        d, lvl = stack.pop()
        try:
            entries = list(os.scandir(d))
        except OSError:
            continue
        for e in entries:
            if not e.is_dir(follow_symlinks=False):
                continue
            if e.name in (".git", "node_modules", "__pycache__") or e.name.startswith(".venv"):
                continue
            idf = os.path.join(e.path, ".project-id")
            if os.path.isfile(idf):
                try:
                    found[json.load(io.open(idf, encoding="utf-8"))["id"]] = \
                        e.path.replace("\\", "/")
                except Exception:
                    pass
            # Descend either way: an umbrella project contains subprojects, and
            # stopping at the first id hid every one of them (reported LOST).
            if lvl + 1 < depth:
                stack.append((e.path, lvl + 1))
    return found

on_disk = _discover(_registry.get("scan_root"))
moved = []
for p in projects:
    pid = p.get("id")
    if not pid:
        problems.append(f"NO IDENTITY: project '{p['name']}' has no id — "
                        f"a rename would break every reference to it silently")
        continue
    actual = on_disk.get(pid)
    declared = (p.get("root") or "").replace("\\", "/").rstrip("/")
    if actual is None:
        if not os.path.isdir(p.get("root") or ""):
            problems.append(f"LOST: project '{p['name']}' ({pid}) is neither at its "
                            f"declared path nor found anywhere under the scan root")
        continue
    if actual.rstrip("/").lower() != declared.lower():
        moved.append((p, actual))

for p, actual in moved:
    msg = f"MOVED: '{p['name']}' ({p['id']}) is at {actual}, registry says {p['root']}"
    if FIX:
        p["root"], p["memory"] = actual, actual + "/.memory"
        print(f"  fixed -> {msg}")
    else:
        problems.append(msg + "  — rerun with --fix to correct the registry")

if FIX and moved:
    io.open(REG, "w", encoding="utf-8", newline="\n").write(
        json.dumps(_registry, indent=2, ensure_ascii=False) + "\n")

# 1) every declared project must actually have a working directory. The root cause of
#    the contamination was a project that had none, so this is checked first.
for p in projects:
    root = p.get("root")
    if root and not os.path.isdir(root):
        problems.append(f"MISSING WORKING DIRECTORY: project '{p['name']}' declares "
                        f"{root} — work will land in a foreign directory")

# 2) cross-contamination: does one project's memory speak another project's language?
for p in projects:
    mem = p.get("memory")
    if not mem or not os.path.isdir(mem):
        continue
    # `related` = mutual subject matter; `references` = this project legitimately
    # names those (its data sources, its tools). Neither counts as foreign.
    related = set(p.get("related", [])) | set(p.get("references", []))
    others = [(q["name"], q["markers"]) for q in projects
              if q["name"] != p["name"] and q.get("markers")
              and q["name"] not in related]
    own = [m.lower() for m in p.get("markers", [])]
    for fn in sorted(os.listdir(mem)):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(mem, fn)
        try:
            text = io.open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        checked_files += 1
        low = text.lower()
        for other_name, markers in others:
            hits = [m for m in markers if re.search(rf"\b{re.escape(m.lower())}\b", low)]
            # a page that also speaks its OWN language is probably a legitimate
            # cross-reference, not a misfiled page — require a clear majority foreign
            own_hits = [m for m in own if re.search(rf"\b{re.escape(m)}\b", low)]
            # A file that speaks a foreign language and NONE of its own is misfiled,
            # even on a single marker: the first version of this check required two
            # foreign hits and missed a page whose only marker was a device name.
            # Two or more foreign hits also flag when they outweigh the local ones.
            misfiled = (hits and not own_hits) or (len(hits) >= 2 and len(hits) > len(own_hits))
            if misfiled:
                problems.append(
                    f"{p['name']}/.memory/{fn}: speaks '{other_name}' "
                    f"({', '.join(hits[:4])}) — belongs in {other_name}, not {p['name']}")

# --- 3) registered tools whose paths point nowhere -------------------------------------
# A .project-id heals a moved repo. An MCP registered by ABSOLUTE PATH does not heal
# itself: the client fails to start the server quietly and the tools are simply absent,
# with no error where the work happens. So check that what is registered still exists.
def _mcp_registrations():
    out = []
    cfg = os.path.expanduser("~/.claude.json")
    try:
        d = json.load(io.open(cfg, encoding="utf-8"))
    except Exception:
        return out
    def collect(servers, scope):
        for name, m in (servers or {}).items():
            cand = [m.get("command")] + list(m.get("args") or []) + \
                   [v for v in (m.get("env") or {}).values() if isinstance(v, str)]
            flat = []
            for c in cand:
                if not isinstance(c, str):
                    continue
                # env values can be LISTS of paths (RECALL_EXTRA_DIRS uses os.pathsep);
                # treating the whole string as one path produced a false alarm.
                flat.extend(x for x in c.split(os.pathsep) if x.strip())
            for c in flat:
                c = c.strip().strip('"')
                # only absolute paths are checkable; "node" or "python" resolve via PATH
                if re.match(r"^[A-Za-z]:[\\/]", c) or c.startswith("/"):
                    out.append((scope, name, c.replace("\\", "/")))
    collect(d.get("mcpServers"), "user")
    for proj, v in (d.get("projects") or {}).items():
        collect(v.get("mcpServers"), os.path.basename(proj.rstrip("/\\")) or "project")
    return out

seen_paths = set()
for scope, name, path in _mcp_registrations():
    if path in seen_paths:
        continue
    seen_paths.add(path)
    if not os.path.exists(path):
        problems.append(f"DANGLING MCP: '{name}' ({scope}) points at {path} — the server "
                        f"will fail to start silently and its tools just vanish")

if not QUIET:
    print(f"project-boundary-check: {len(projects)} projects, {checked_files} memory files")

if problems:
    for x in problems:
        print(f"  {x}")
    print("")
    print("BOUNDARY VIOLATION — a file living in another project's folder never makes it")
    print("that project's business. Move it, or give the project its own directory.")
    sys.exit(1)

if not QUIET:
    print("  clean")
sys.exit(0)
