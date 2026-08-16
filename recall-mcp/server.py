#!/usr/bin/env python3
"""knowledge-recall-mcp — lightweight hybrid recall over a markdown knowledge wiki.

Proven recipe (FTS5 + FastEmbed embeddings + sqlite-vec + Reciprocal-Rank-Fusion),
local-first, no API key. Point it at your wiki via the WIKI_DIR env var.

Usage:
  python server.py index            # (re)build the index over the wiki
  python server.py search "query"   # CLI hybrid search (shows results)
  python server.py read <path>      # print a note
  python server.py serve            # run as an MCP server (stdio)

Config via env: WIKI_DIR, RECALL_DB, RECALL_MODEL.
"""
import os, sys, re, json, glob, sqlite3, hashlib
import uuid, time, math, datetime
from pathlib import Path

# Pin the FastEmbed model cache to a PERSISTENT dir inside the repo (not the volatile
# OS %TEMP%, which Windows Storage Sense / Disk Cleanup wipes — that triggered a silent
# ~87 MB model re-download on the next reindex). The 384-dim MiniLM weights are a core
# runtime asset of the recall engine, so they live with it. Gitignored via .fastembed_cache/.
os.environ.setdefault(
    "FASTEMBED_CACHE_PATH",
    str(Path(__file__).resolve().parent / ".fastembed_cache"),
)
# Load the model fully OFFLINE once it is cached locally. huggingface_hub otherwise
# revalidates the cached weights over the network on every load; under a client that
# spawns this server inside a restricted network namespace (corporate VPN/proxy, slow
# or blocked egress) that metadata check stalls for *minutes* with no timeout — the
# "reindex/search hangs forever" symptom — even though the 87 MB weights are right here.
# The weights ship in .fastembed_cache, so offline load is purely local and instant.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

# Default points at the sibling Wiki/ in this repo; override with the WIKI_DIR env var.
WIKI_DIR = Path(os.environ.get("WIKI_DIR", str(Path(__file__).resolve().parent.parent / "Wiki")))
# Extra roots to index alongside the wiki — e.g. per-project ".memory" dirs (";"-separated).
# Strictly opt-in registered paths; never index unrelated repos.
EXTRA_DIRS = [Path(p) for p in os.environ.get("RECALL_EXTRA_DIRS", "").split(";") if p.strip()]
DB_PATH  = Path(os.environ.get("RECALL_DB", str(Path(__file__).parent / "recall-index.sqlite")))
MODEL    = os.environ.get("RECALL_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DIM      = 384
CHUNK, OVERLAP = 2000, 200
RRF_K    = 60
# Model-aware index key: embeddings from different models/chunkings are NOT comparable.
# The key is stored in the DB; do_index forces a full re-embed on mismatch, do_search
# refuses semantic search against a foreign-keyed index (content-hash alone would
# silently skip unchanged files after a model switch and mix vector spaces).
INDEX_KEY = f"{MODEL}|dim={DIM}|chunk={CHUNK}/{OVERLAP}|schema=1"
# Append-only retrieval log (review-queue input for retros — never automatic decisions).
LOG_PATH = Path(os.environ.get("RECALL_LOG", str(DB_PATH.parent / "recall-retrieval-log.jsonl")))

# --- usage telemetry + ranking signals -------------------------------------------------
# Every search/hit/read is recorded so the wiki's own usefulness can be QUESTIONED with
# data instead of opinion: which pages carry the work, which surface but are never opened
# (their summary is the problem — that is what the agent sees first), which are dead weight.
# The "read" signal is derived, never self-reported: a page counts as useful when an agent
# actually opens it after a search surfaced it. A rule that asks an agent to rate its own
# recall is a rule without a control.
TELEMETRY = os.environ.get("RECALL_TELEMETRY", "1") not in ("0", "false", "no")
# A hit only counts as "confirmed useful" if the read follows the search within this window.
READ_WINDOW_S = int(os.environ.get("RECALL_READ_WINDOW_S", "900"))
# Recency: a mild multiplicative nudge (max +RECENCY_W) so fresh pages win ties without
# ever outranking a clearly better match. Superseded pages are demoted instead of hidden —
# the wiki keeps history on purpose.
RECENCY_W    = float(os.environ.get("RECALL_RECENCY_W", "0.15"))
RECENCY_HALF = float(os.environ.get("RECALL_RECENCY_HALFLIFE_D", "180"))
STALE_FACTOR = float(os.environ.get("RECALL_STALE_FACTOR", "0.6"))
# NOT "tombstone": the protocol wants a killed idea's tombstone to surface PROMINENTLY when
# someone proposes it again. Demoting it would do the exact opposite of its purpose. Whether
# tombstones deserve a positive boost is a separate question - neutral is the safe default.
_STALE_MARKERS = ("historical", "superseded", "obsolete", "deprecated", "retired")
# Append-only chronicles (a wiki changelog, a running log) beat everything on keyword
# search purely by term coverage: they contain every word the wiki has ever used. Measured
# on this wiki, log.md carried the highest hit count of any page (127) against only 49
# opens, and topped the results in two unrelated experiments. It is not noise - people do
# look things up in it - so it is demoted, not excluded. Comma-separated basenames.
CHRONICLE_FILES = tuple(x.strip().lower() for x in
                        os.environ.get("RECALL_CHRONICLE_FILES", "log.md").split(",") if x.strip())
CHRONICLE_FACTOR = float(os.environ.get("RECALL_CHRONICLE_FACTOR", "0.4"))

_SESSION = uuid.uuid4().hex[:8]
_recent_hits = {}   # path -> (epoch, query, rank) for the derived read signal
_telemetry_errors = []   # surfaced by do_stats: a broken meter must not look like a quiet one

# Import the native-extension modules HERE, at module load on the MAIN thread.
# FastMCP runs sync tools on a worker thread, and a *first* import of a C-extension
# (sqlite_vec, fastembed/onnxruntime) from a worker thread can deadlock on Python's
# import lock — intermittently (a race). That was the real "recall hangs for minutes,
# but sometimes returns in ~1s" bug: the hang was `import sqlite_vec` inside the tool
# call, not the model or the network. Importing up front on the main thread makes the
# in-function imports cache hits, so no worker-thread first-import can ever deadlock.
import sqlite_vec as _sqlite_vec_preload          # noqa: F401  (preload on main thread)
try:
    import fastembed as _fastembed_preload        # noqa: F401  (preload on main thread)
except Exception:
    pass

_model = None
def _embed(texts):
    global _model
    from fastembed import TextEmbedding
    if _model is None:
        _model = TextEmbedding(model_name=MODEL)
    return [list(map(float, v)) for v in _model.embed(list(texts))]

def _blob(v):
    import sqlite_vec
    return sqlite_vec.serialize_float32(v)

def _db():
    import sqlite_vec
    db = sqlite3.connect(str(DB_PATH), timeout=10.0)
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=10000")
    except sqlite3.Error:
        pass
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    db.executescript(f"""
        CREATE TABLE IF NOT EXISTS notes(path TEXT PRIMARY KEY, title TEXT, hash TEXT);
        CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(path UNINDEXED, title, content);
        CREATE TABLE IF NOT EXISTS chunks(id INTEGER PRIMARY KEY, path TEXT, text TEXT);
        CREATE VIRTUAL TABLE IF NOT EXISTS vchunks USING vec0(embedding float[{DIM}] distance_metric=cosine);
        CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY, ts TEXT, session TEXT, kind TEXT,
            query TEXT, path TEXT, rank INTEGER, score REAL);
        CREATE INDEX IF NOT EXISTS events_kind_ts ON events(kind, ts);
        CREATE INDEX IF NOT EXISTS events_path ON events(path);
        CREATE TABLE IF NOT EXISTS pending_hits(
            path TEXT PRIMARY KEY, ts REAL, query TEXT, rank INTEGER);
        CREATE TABLE IF NOT EXISTS page_stats(
            path TEXT PRIMARY KEY, hits INTEGER DEFAULT 0, reads INTEGER DEFAULT 0,
            first_hit TEXT, last_hit TEXT, last_read TEXT);
    """)
    return db

def _stored_key(db):
    row = db.execute("SELECT value FROM meta WHERE key='index_key'").fetchone()
    return row["value"] if row else None

_META_FIELDS = ("Summary", "Type", "Status", "Last updated")
def _page_meta(path):
    """Frontmatter-ish page metadata for richer search results (summary-first recall)."""
    try:
        head = Path(path).read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return {}
    meta = {}
    m = (re.search(r"^\*\*Summary\*\*:\s*(.+)$", head, re.M)
         or re.search(r"^description:\s*[\"']?(.+?)[\"']?\s*$", head, re.M))
    if m:
        meta["summary"] = m.group(1).strip()[:300]
    for field in ("Type", "Status"):
        m = re.search(rf"^\*\*{field}\*\*:\s*(.+)$", head, re.M)
        if m:
            meta[field.lower()] = m.group(1).strip()[:60]
    m = re.search(r"^\*\*Last updated\*\*:\s*(.+)$", head, re.M)
    if m:
        meta["last_updated"] = m.group(1).strip()[:20]
    return meta

def _log_retrieval(query, mode, results):
    """Append-only usage log — review-queue material, never an automatic signal."""
    try:
        import datetime
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": datetime.datetime.now().isoformat(timespec="seconds"),
                "q": query[:120], "mode": mode,
                "hits": [r["path"].rsplit("/", 1)[-1] for r in results],
            }, ensure_ascii=False) + "\n")
    except OSError:
        pass

def _now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def _record(db, kind, query=None, path=None, rank=None, score=None):
    if not TELEMETRY:
        return
    try:
        db.execute("INSERT INTO events(ts,session,kind,query,path,rank,score) VALUES(?,?,?,?,?,?,?)",
                   (_now(), _SESSION, kind, (query or "")[:200] or None, path, rank, score))
    except sqlite3.Error as exc:
        _telemetry_errors.append(str(exc)[:120])

def _record_hits(db, query, results):
    """A surfaced page is a HIT. Whether it was useful is decided later, by a read."""
    if not TELEMETRY:
        return
    now_s, now_e = _now(), time.time()
    for rank, r in enumerate(results):
        path = r["path"]
        _record(db, "hit", query, path, rank, r.get("score"))
        db.execute("""INSERT INTO page_stats(path,hits,reads,first_hit,last_hit)
                      VALUES(?,1,0,?,?)
                      ON CONFLICT(path) DO UPDATE SET hits=hits+1, last_hit=excluded.last_hit""",
                   (path, now_s, now_s))
        _recent_hits[path] = (now_e, query, rank)
        db.execute("INSERT INTO pending_hits(path,ts,query,rank) VALUES(?,?,?,?) "
                   "ON CONFLICT(path) DO UPDATE SET ts=excluded.ts, query=excluded.query, "
                   "rank=excluded.rank", (path, now_e, query, rank))
    # expire stale pending hits so they cannot confirm a read hours later
    db.execute("DELETE FROM pending_hits WHERE ts < ?", (now_e - READ_WINDOW_S,))
    db.commit()

def _record_read(path):
    """Derived usefulness: a read that follows a search hit confirms the hit was worth it.

    The pending hit lives in the DB, not in process memory: a CLI search followed by a CLI
    read, a server restart, or a second MCP process would otherwise lose the link and the
    telemetry would silently under-count recall. And the hit is CONSUMED — opening the same
    page five times is one confirmed hit, not five.
    """
    if not TELEMETRY:
        return
    key = str(path)
    # Consume from BOTH stores. Popping only the in-memory copy left the DB row behind, so
    # a second read of the same page found it there and confirmed the hit twice — the
    # double count this fix was meant to remove. The DB row is the authority; memory is
    # only a fast path.
    hit = _recent_hits.pop(key, None)
    try:
        db0 = _db()
        row = db0.execute("SELECT ts, query, rank FROM pending_hits WHERE path=?",
                          (key,)).fetchone()
        if row is not None:
            hit = hit or (row["ts"], row["query"], row["rank"])
            db0.execute("DELETE FROM pending_hits WHERE path=?", (key,))
            db0.commit()
        elif hit is not None:
            hit = None            # already consumed elsewhere -> do not count again
        db0.close()
    except sqlite3.Error as exc:
        _telemetry_errors.append(str(exc)[:120])
    if not hit or (time.time() - float(hit[0])) > READ_WINDOW_S:
        return                      # opened without recall surfacing it -> not a recall win
    try:
        db = _db()
        _record(db, "read", hit[1], str(path), hit[2])
        db.execute("""INSERT INTO page_stats(path,hits,reads,last_read) VALUES(?,0,1,?)
                      ON CONFLICT(path) DO UPDATE SET reads=reads+1, last_read=excluded.last_read""",
                   (str(path), _now()))
        db.commit(); db.close()
    except sqlite3.Error as exc:
        _telemetry_errors.append(str(exc)[:120])

def _recency_factor(meta):
    """Fresh pages get a small nudge; it decays, and never overturns a better match."""
    raw = (meta.get("last_updated") or "")[:10]
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if not m:
        return 1.0
    try:
        age = (datetime.date.today() - datetime.date(*map(int, m.groups()))).days
    except ValueError:
        return 1.0
    return 1.0 + RECENCY_W * math.exp(-max(age, 0) / RECENCY_HALF)

def _chronicle_factor(path):
    """Demote append-only chronicles: they win on term coverage, not on relevance."""
    return CHRONICLE_FACTOR if str(path).replace("\\", "/").rsplit("/", 1)[-1].lower() \
        in CHRONICLE_FILES else 1.0

def _status_factor(meta):
    """Superseded material is demoted, not hidden — the wiki keeps history on purpose."""
    blob = " ".join(str(meta.get(k) or "") for k in ("status", "type")).lower()
    return STALE_FACTOR if any(k in blob for k in _STALE_MARKERS) else 1.0

def _chunk(text):
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i+CHUNK]); i += CHUNK - OVERLAP
    return out or [""]

def _drop(db, path):
    db.execute("DELETE FROM notes WHERE path=?", (path,))
    db.execute("DELETE FROM notes_fts WHERE path=?", (path,))
    for r in db.execute("SELECT id FROM chunks WHERE path=?", (path,)).fetchall():
        db.execute("DELETE FROM vchunks WHERE rowid=?", (r["id"],))
    db.execute("DELETE FROM chunks WHERE path=?", (path,))

def do_index():
    # A wrong or empty WIKI_DIR used to sail through as "indexed_files: 0" and then delete
    # every note from the index, because nothing was seen. An empty root is a configuration
    # error, not a successful run of zero work.
    roots = [WIKI_DIR] + EXTRA_DIRS
    present = [r for r in roots if Path(r).is_dir()]
    if not present:
        raise ValueError(f"no readable index root: WIKI_DIR={WIKI_DIR!r} "
                         f"EXTRA_DIRS={[str(d) for d in EXTRA_DIRS]} - refusing to index, "
                         f"an empty root would wipe the index")
    db = _db()
    # Model-aware index key: on mismatch (or a legacy DB without a key), force a FULL
    # re-embed — the content-hash shortcut below would otherwise keep foreign vectors.
    stored = _stored_key(db)
    has_notes = db.execute("SELECT 1 FROM notes LIMIT 1").fetchone() is not None
    force = has_notes and stored != INDEX_KEY
    files = []
    for _root in [WIKI_DIR] + EXTRA_DIRS:
        files += [Path(p) for p in glob.glob(str(_root / "**" / "*.md"), recursive=True)]
    seen, changed = set(), 0
    for f in files:
        rel = str(f).replace("\\", "/"); seen.add(rel)
        content = f.read_text(encoding="utf-8", errors="replace")
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()
        row = db.execute("SELECT hash FROM notes WHERE path=?", (rel,)).fetchone()
        if row and row["hash"] == h and not force:
            continue
        title = next((l[2:].strip() for l in content.splitlines() if l.startswith("# ")), f.stem)
        _drop(db, rel)
        db.execute("INSERT INTO notes(path,title,hash) VALUES(?,?,?)", (rel, title, h))
        db.execute("INSERT INTO notes_fts(path,title,content) VALUES(?,?,?)", (rel, title, content))
        chs = _chunk(content)
        for ch, v in zip(chs, _embed(chs)):
            cur = db.execute("INSERT INTO chunks(path,text) VALUES(?,?)", (rel, ch))
            db.execute("INSERT INTO vchunks(rowid,embedding) VALUES(?,?)", (cur.lastrowid, _blob(v)))
        changed += 1
    for r in db.execute("SELECT path FROM notes").fetchall():
        if r["path"] not in seen:
            _drop(db, r["path"])
    db.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('index_key',?)", (INDEX_KEY,))
    db.commit()
    return {"wiki_dir": str(WIKI_DIR), "indexed_files": len(seen), "reembedded": changed,
            "index_key": INDEX_KEY, "forced_full_reembed": force}

def do_search(query, mode="hybrid", limit=8):
    # An unknown mode used to return [] and still be logged as a search: a measurement
    # error that also hides the caller's bug.
    if mode not in ("hybrid", "fulltext", "semantic"):
        raise ValueError(f"unknown mode {mode!r} - expected hybrid, fulltext or semantic")
    db = _db()
    _record(db, "search", query)
    if mode in ("hybrid", "semantic"):
        stored = _stored_key(db)
        if stored is not None and stored != INDEX_KEY:
            raise ValueError(
                f"recall index was built with '{stored}' but this process runs "
                f"'{INDEX_KEY}' — semantic scores would be garbage. Re-run "
                f"`server.py index` with the current env (forces a full re-embed), "
                f"or fix RECALL_MODEL/RECALL_DB to match.")
    hits = {}
    if mode in ("hybrid", "fulltext"):
        q = " OR ".join(re.findall(r"\w+", query)) or query
        try:
            rows = db.execute(
                "SELECT path, snippet(notes_fts,2,'[',']','…',15) snip "
                "FROM notes_fts WHERE notes_fts MATCH ? ORDER BY bm25(notes_fts) LIMIT ?",
                (q, limit * 3)).fetchall()
            for rank, r in enumerate(rows):
                e = hits.setdefault(r["path"], {"score": 0.0, "snip": None, "modes": set()})
                e["score"] += 1.0 / (RRF_K + rank); e["snip"] = e["snip"] or r["snip"]; e["modes"].add("fts")
        except sqlite3.OperationalError:
            pass
    if mode in ("hybrid", "semantic"):
        qv = _blob(_embed([query])[0])
        rows = db.execute(
            "SELECT rowid, distance FROM vchunks WHERE embedding MATCH ? ORDER BY distance LIMIT ?",
            (qv, limit * 3)).fetchall()
        for rank, r in enumerate(rows):
            ch = db.execute("SELECT path, text FROM chunks WHERE id=?", (r["rowid"],)).fetchone()
            if not ch:
                continue
            e = hits.setdefault(ch["path"], {"score": 0.0, "snip": None, "modes": set()})
            e["score"] += 1.0 / (RRF_K + rank)
            if not e["snip"]:
                e["snip"] = " ".join(ch["text"][:160].split()) + "…"
            e["modes"].add("sem")
    # Rank on relevance FIRST, then apply the mild recency/status signals. Metadata is
    # read for every candidate, not just the survivors, or a demoted page could never be
    # displaced by a fresher one below the cut.
    cands = []
    for path, e in hits.items():
        meta = _page_meta(path)                       # summary/type/status/last_updated
        boost = _recency_factor(meta) * _status_factor(meta) * _chronicle_factor(path)
        cands.append((e["score"] * boost, boost, path, e, meta))
    out = []
    for adj, boost, path, e, meta in sorted(cands, key=lambda x: -x[0])[:limit]:
        t = db.execute("SELECT title FROM notes WHERE path=?", (path,)).fetchone()
        r = {"path": path, "title": t["title"] if t else path,
             "snippet": e["snip"], "score": round(adj, 4),
             "mode": "+".join(sorted(e["modes"]))}
        if abs(boost - 1.0) > 0.01:
            r["signal"] = round(boost, 2)             # <1 = superseded, >1 = fresh
        r.update(meta)
        out.append(r)
    _log_retrieval(query, mode, out)
    _record_hits(db, query, out)
    db.close()
    return out

def do_read(path):
    p = Path(path)
    if not p.is_absolute():
        p = WIKI_DIR / path
    text = p.read_text(encoding="utf-8", errors="replace")
    _record_read(p.as_posix())
    return text

def do_stats(limit=12, min_hits=3):
    """Is this wiki actually earning its keep? Answers with data, not impressions.

    hit  = a page was surfaced by a search
    read = an agent opened it afterwards (derived, never self-reported)

    The interesting number is not the total but the SHAPE: pages that are surfaced and
    never opened have a summary problem (the summary is what the agent judges), pages
    never surfaced at all are dead weight or badly worded, and a low overall read rate
    means recall is returning plausible-but-wrong pages.
    """
    db = _db()
    def one(q, *a):
        r = db.execute(q, a).fetchone()
        return (r[0] if r else 0) or 0
    searches = one("SELECT COUNT(*) FROM events WHERE kind='search'")
    n_hits   = one("SELECT COUNT(*) FROM events WHERE kind='hit'")
    n_reads  = one("SELECT COUNT(*) FROM events WHERE kind='read'")
    since    = db.execute("SELECT MIN(ts) FROM events").fetchone()[0]
    indexed  = one("SELECT COUNT(*) FROM notes")

    def rows(q, *a):
        return [dict(r) for r in db.execute(q, a).fetchall()]

    workhorses = rows("""SELECT path, hits, reads, last_read FROM page_stats
                         WHERE reads>0 ORDER BY reads DESC, hits DESC LIMIT ?""", limit)
    unread     = rows("""SELECT path, hits, last_hit FROM page_stats
                         WHERE reads=0 AND hits>=? ORDER BY hits DESC LIMIT ?""", min_hits, limit)
    never      = rows("""SELECT n.path FROM notes n
                         LEFT JOIN page_stats p ON p.path=n.path
                         WHERE p.path IS NULL OR p.hits=0 LIMIT ?""", limit)
    # Co-occurrence: pages that keep surfacing for the same query are neighbours in
    # practice, whether or not a wikilink says so. Substrate for a typed graph later.
    together   = rows("""SELECT a.path AS a, b.path AS b, COUNT(*) AS n
                         FROM events a JOIN events b
                           ON a.query=b.query AND a.kind='hit' AND b.kind='hit' AND a.path<b.path
                         GROUP BY a.path, b.path HAVING n>=2 ORDER BY n DESC LIMIT ?""", limit)
    def _label(p):
        # keep the parent dir: several layers have their own index.md, and a bare
        # basename makes two different pages look like one row printed twice.
        parts = str(p).replace("\\", "/").split("/")
        return "/".join(parts[-2:]) if len(parts) > 1 else parts[-1]
    short = lambda xs, *k: [{kk: (_label(x[kk]) if kk in ("path", "a", "b") else x[kk])
                             for kk in k} for x in xs]
    ever_used = one("SELECT COUNT(*) FROM page_stats WHERE reads>0")
    backfilled = one("SELECT COUNT(*) FROM events WHERE session LIKE 'backfill%'")
    live_hits  = one("SELECT COUNT(*) FROM events WHERE kind='hit'  AND session NOT LIKE 'backfill%'")
    live_reads = one("SELECT COUNT(*) FROM events WHERE kind='read' AND session NOT LIKE 'backfill%'")
    db.close()
    return {
        "since": since, "indexed_pages": indexed,
        "searches": searches, "hits": n_hits, "reads": n_reads,
        "read_rate": round(n_reads / n_hits, 3) if n_hits else None,
        # Backfilled reads are ANY read; the live signal only counts a read that follows
        # a search hit within the window. Do not read one rate as if it were the other.
        "backfilled_events": backfilled,
        "live_read_rate": round(live_reads / live_hits, 3) if live_hits else None,
        "live_hits": live_hits, "live_reads": live_reads,
        "pages_ever_used": ever_used,
        "workhorses": short(workhorses, "path", "reads", "hits", "last_read"),
        "surfaced_never_read": short(unread, "path", "hits", "last_hit"),
        "never_surfaced": [x["path"].rsplit("/", 1)[-1] for x in never],
        "co_occurring": short(together, "a", "b", "n"),
        "telemetry_errors": _telemetry_errors[-5:],
    }

def serve():
    from fastmcp import FastMCP
    mcp = FastMCP("knowledge-recall")

    @mcp.tool()
    def search_notes(query: str, mode: str = "hybrid", limit: int = 8) -> list:
        """Hybrid (keyword + semantic) recall over the knowledge wiki. mode: hybrid|fulltext|semantic."""
        return do_search(query, mode, limit)

    @mcp.tool()
    def read_note(path: str) -> str:
        """Read a wiki note by path (relative to the wiki dir or absolute)."""
        return do_read(path)

    @mcp.tool()
    def recall_stats(limit: int = 12) -> dict:
        """Usage statistics for the wiki: which pages actually get used, which surface but are never opened, which are never found at all."""
        return do_stats(limit)

    @mcp.tool()
    def reindex() -> dict:
        """Rebuild the recall index over the wiki (incremental by content hash)."""
        return do_index()

    mcp.run()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if cmd == "index":
        print(json.dumps(do_index(), indent=2))
    elif cmd == "search":
        print(json.dumps(do_search(" ".join(sys.argv[2:])), indent=2, ensure_ascii=False))
    elif cmd == "stats":
        print(json.dumps(do_stats(), indent=2, ensure_ascii=False))
    elif cmd == "read":
        print(do_read(sys.argv[2]))
    else:
        serve()
