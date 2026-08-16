# Local recall engine (knowledge-recall-mcp)

**Summary**: Our lightweight, local recall engine for this wiki. It combines keyword search (FTS5) and semantic search (FastEmbed + sqlite-vec), fuses the two with Reciprocal Rank Fusion (RRF), and exposes them as an MCP server for Claude and Codex. It replaces heavier options — Hermes' FTS-only recall and the LLM WIKI multi-tenant engine — with just the recall recipe.

**Sources**: `<RECALL_MCP_DIR>/` (our repo), [[agent-orchestration-options]], the Hermes/Basic-Memory reference review.

**Measured quality (2026-06-19)**: **16/16 hit@5, 0% miss-rate** on a 16-query eval set (`scripts/recall-eval-set.json` run via `recall-mcp/eval.py`) — the expected page is in the top-5 (usually #1–2) for every test query. So "recall first" returns the right page, not nonsense. Re-run the eval after large content changes.

**Reference performance (2026-06-30, warm server, ~120-file wiki)**: search is **sub-50 ms** — hybrid average **16 ms** (max 53 ms), semantic average **11 ms**, fulltext average **0.2 ms**. The only wait is a **one-time ~1.3 s model load at server startup** (then the `_model` global stays warm). If a search ever *hangs*, it is **not** the engine — suspect the FastMCP version regression (below) or a model **re-download** (cache gotcha below).

**Last updated**: 2026-08-16 (usage telemetry + derived read signal, recency /
status ranking nudges, `recall_stats`; plus the **first measured usage** from the
1657-event backfill — see below)

---

## Gotcha — pin FastMCP to 2.x (3.x regressed stdio tool-calls)

**Symptom**: the MCP client repeatedly shows the server "still connecting" then
"disconnected/reconnected" in a loop, and **tool calls never return** — while the
server *looks* fine. Verified 2026-06-26: under **FastMCP 3.4.2** the stdio
handshake (`initialize`, `tools/list`) succeeds and stdout is clean, but
**`tools/call` hangs and produces no response**, so the client times out and drops
the connection. Downgrading to **FastMCP 2.14.7** fixed it — tool calls respond
normally. `requirements.txt` is now pinned `fastmcp>=2.0,<3`.

**Diagnosis recipe** (reusable for any stdio MCP):
1. CLI path works? `python server.py search "x"` → isolates server logic from MCP.
2. Drive the protocol directly: pipe `initialize` + `notifications/initialized` +
   `tools/list` into `server.py serve`, **hold stdin open** (`{ printf …; sleep N; }`)
   so EOF doesn't trigger shutdown. Confirm stdout is *only* JSON-RPC (banners must
   go to **stderr**, or they corrupt the stream).
3. Then send a real `tools/call`. If handshake responds but `tools/call` doesn't →
   suspect a FastMCP/SDK version regression, not your code.

**Don't downgrade in place.** `pip install "fastmcp<3"` over a 3.x install left a
mixed-version venv (mismatched files → `ImportError: PrivateKeyJWTClientAuthenticator`).
A live MCP process also **locks** venv files on Windows (pywin32/pydantic_core),
so force-reinstall can't overwrite them. Fix: build a **fresh venv** (`.venv-new`),
verify a `tools/call` responds, then repoint the `.claude.json` `command` to it and
restart the client; delete the old locked venv after the old process exits.

## Gotcha — preload native (C-extension) modules on the MAIN thread (fixed 2026-06-30)

**Symptom**: `search_notes`/`reindex` **intermittently** hung — sometimes ~1 s, sometimes
**2–4 minutes** (or "forever"), across client restarts. Misleading because the engine,
driven from the CLI or even by hand over the MCP protocol, was consistently ~1.4 s.

**Root cause** (found by step-timed logging written to a *file*, since the client swallows
stderr): the hang was **`import sqlite_vec` executed for the first time inside a FastMCP
tool call**. FastMCP runs sync `@mcp.tool()` functions on a **worker thread**, and a
first-time import of a **C-extension** from a non-main thread can **deadlock on Python's
import lock**. It's a race — sometimes the import completes (~1 s), sometimes it deadlocks
(minutes, no timeout). The CLI path never hit it because it imports on the main thread.
It was **not** the model, the network, the model cache, or DB locks — all of which we
ruled out first and wasted time on.

**Fix**: import the native modules (`sqlite_vec`, `fastembed`) at **module load on the main
thread**, so the lazy in-function imports become cache hits and no worker-thread
first-import ever happens. Verified 3/3 deterministic ~1.4 s. Engine commit `d5cce3b`.

**Reusable rule**: in *any* MCP server whose tools run on a worker thread (FastMCP, etc.),
**preload C-extensions at import time on the main thread**. Lazy first-imports inside tool
handlers are a latent intermittent deadlock.

**Diagnosis lesson**: when a hang is intermittent and the CLI path is fine, instrument the
*actual serve path* with **file-based** step logging and bisect to the exact line — don't
keep theorising (we burned cycles on cache/network/locks first). Also: don't kill the MCP
server processes mid-session to "retry" — it only spawns a respawn loop (captured in the
`never-kill-mcp-mid-session` harness memory).

## Gotcha — pin the FastEmbed model cache out of %TEMP% (fixed 2026-06-30)

**Symptom**: `reindex` (and the first semantic/hybrid search of a session) felt
slow, or appeared to "run forever". **Root cause**: `server.py` set no `cache_dir`, so FastEmbed
cached the **87 MB MiniLM model in the OS `%TEMP%`** (`…\AppData\Local\Temp\fastembed_cache`).
Windows Storage Sense / Disk Cleanup wipes Temp → the next reindex **silently
re-downloaded ~87 MB** from HuggingFace. The reindex *logic* was never the
bottleneck (incremental by hash; unchanged tree = **0.18 s**).

**Fix**: pin the cache next to the engine — `server.py` now does
`os.environ.setdefault("FASTEMBED_CACHE_PATH", <repo>/recall-mcp/.fastembed_cache)`
(gitignored). Weights are a **core runtime asset**, so they live with the engine,
not in volatile Temp. The 87 MB was moved there once (no re-download). Engine commit
`e5a2531`.

**Process lesson (same session)**: a diagnostic `find /` over the whole drive ran
**>1 h** in the background unnoticed — `| head` does *not* stop `find` when there are
no matches (no write → no SIGPIPE). **Never `find /`**; scope searches to a known
path, and actually check background tasks before declaring "nothing is running".

## What it is

A small Python MCP server (`knowledge-recall-mcp`) that indexes this wiki's Markdown
and answers semantic + keyword queries. It is the **recall layer** — it *finds*
pages; the [[role-librarian]] still curates what gets written.

- **Recipe**: FTS5 (BM25) + FastEmbed `all-MiniLM-L6-v2` (384-dim, local, no API key)
  in sqlite-vec `vec0` (cosine), chunked ~2000/200, fused by Reciprocal Rank Fusion
  (K=60). Incremental re-index by content hash.
- **Why our own**: Hermes' recall is keyword-only (FTS5); the LLM WIKI `wiki_engine`
  had grown into a tangled multi-tenant product (auth/billing/web UI). We took only
  the proven recipe — local-first, lightweight, no third-party code to vet.

## How to use

- **Tools (MCP)**: `search_notes(query, mode=hybrid|fulltext|semantic, limit)`,
  `read_note(path)`, `recall_stats(limit)`, `reindex()`.
- **CLI**: `python server.py index | search "…" | read <path> | stats | serve`.
  - ⚠️ **Always pass the live-wiki env** (`WIKI_DIR=…/LLM Knowledge Library Wiki/Wiki`, `RECALL_EXTRA_DIRS=…/ExampleApp/.memory`). A **bare** `index`/`reindex` defaults to the engine's own content-free `Wiki/` and **pollutes the shared DB**; re-running with the correct env full-syncs it back.
- **Bootstrap a fresh clone**: `./bootstrap.ps1` (Windows) / `./bootstrap.sh` —
  venv + deps + index in one idempotent command (see [[role-operations]]).
- **Register** the MCP server (snippet in the repo README) and restart the client.

## Status & limits

Verified: indexes the wiki (56 pages at first build; grows with the wiki), hybrid
queries return `fts+sem`-fused results. `reindex` is **manual** (run after wiki writes,
or on a timer).

**Multilingual since 2026-07-04**: production model is now
`paraphrase-multilingual-MiniLM-L12-v2` (A/B on the 50-query bilingual eval set:
**48/50 hit@5, DE 26/27** vs. old all-MiniLM 42/50, DE 20/27; EN unchanged).
Configured via `RECALL_MODEL` + `RECALL_DB=recall-index-ml.sqlite` at **all three
call sites** — MCP registration (`~/.claude.json`), the wiki post-commit hook, and
the failure-recall hook (see [[failure-triggered-recall]]). ⚠️ These must stay in
sync: a mismatched incremental reindex silently mixes embedding models in one DB
(content-hash alone doesn't detect a model change). **Since 2026-07-04 this is
enforced in code** (engine commit `a0454af`): a model-aware **`INDEX_KEY`**
(`model|dim|chunk|schema`) is stored in the DB's meta table — `index` forces a
**full re-embed** on mismatch or a legacy keyless DB (verified: 159 chunks forced
once, then 0 on the next incremental run), and `search` **refuses semantic**
against a foreign-keyed index with a loud, actionable error (verified). Env
discipline is still good hygiene, but no longer the only protection. The old
English index (`recall-index.sqlite`) is kept as fallback.

Search results also now carry `summary`/`type`/`status`/`last_updated` from each
page's frontmatter (**summary-first recall** — the caller can often decide from
the summary without reading the page), and every retrieval is appended to
`recall-retrieval-log.jsonl` (append-only; a **review queue** for retros, never
automatic lifecycle decisions — per [[cascaded-agent-memory]] gotcha #1).

## Usage telemetry + ranking signals (since 2026-08-16, engine `bd4937e`)

Until this change the wiki could not answer whether it was earning its keep: a few
hundred indexed pages and no signal on which ones ever helped. The engine now
records its own usage in the index DB and uses two mild signals in ranking.

**What is recorded** — two tables next to the index:

- `events` — one row per `search`, per `hit` (a page surfaced by a search, with
  rank and score) and per `read`, timestamped and session-tagged;
- `page_stats` — per page: `hits`, `reads`, `first_hit`, `last_hit`, `last_read`.

**The usefulness signal is derived, never self-reported.** A page counts as useful
when an agent **opens** it within `RECALL_READ_WINDOW_S` (default 900 s) of a
search having surfaced it; a read of a page the search never returned is manual
navigation and deliberately does **not** count. Asking an agent to rate its own
recall would be a rule without a control — the design rationale and its limits are
[[derived-usage-signals-not-self-reports]]. Telemetry can be switched off with
`RECALL_TELEMETRY=0`.

**What `recall_stats` / `server.py stats` reports**: `searches` / `hits` / `reads`
and the **read rate**; **workhorses** (most-read pages); **surfaced but never
opened** — the diagnostic bucket, since the agent judges a hit by its *summary*, so
these have a summary problem rather than a content problem; **never surfaced at
all** (dead weight or unreachable vocabulary); **query co-occurrence** (pages that
keep surfacing for the same query are neighbours in practice — substrate for a
typed graph later); and **`telemetry_errors`**, so a broken meter cannot look like
a quiet one ([[silent-except-hides-dead-features]]).

**Two ranking nudges** (both multiplicative on the fused RRF score, both mild by
design — they break ties, they never overturn a clearly better match):

- **recency**: up to **+15 %**, exponential decay with a **180-day half-life**, read
  from the page's `**Last updated**` field (`RECALL_RECENCY_W`,
  `RECALL_RECENCY_HALFLIFE_D`);
- **status demotion**: **×0.6** (`RECALL_STALE_FACTOR`) for pages whose `Status` /
  `Type` field marks them `historical`, `superseded`, `tombstone`, `obsolete`,
  `deprecated` or `retired`.

⚠️ **This changes the meaning of a wiki convention.** The protocol's
["Historical (retained, no longer current)"](../../WIKI_PROTOCOL.md) marker was
until now a **human-readable** label that the ranking ignored; it now **bites**.
It is a **demotion, not a filter** — history is kept on purpose and a historical
page still surfaces when it is the best answer, just below current material. Two
practical consequences: (a) marking a page historical is now a retrieval decision,
not only an editorial one; (b) the demotion reads the **`Status`/`Type` fields
only** — an earlier version also scanned the page `Summary`, which demoted an
innocent page because its prose contained the word "deprecated" (one of the four
bugs this change's tests caught).

**Verified 2026-08-16** on the live index: one search recorded exactly +1 search /
+3 hits / +1 read; a read with no preceding hit correctly did not count; demotion
fired on 2 real pages with no false positives; 0 telemetry errors. Four bugs were
found by these tests and **none of them was visible on reading the code**.

### First measured usage — the 2026-08-16 backfill (engine `3aac59f`)

The counters did not have to wait for data: **1657 events** were reconstructed
from two artefacts that had been recording all along — the engine's own
append-only retrieval log (which pages a query *surfaced*) and the agent session
transcripts (`Read` calls on wiki files = which pages were *opened*). History now
reaches back to **2026-06-17**. Method, and the rules that keep it honest, in
[[backfill-a-new-metric-from-existing-history]]; 76 events with ambiguous or
unknown basenames were **skipped, not guessed**.

⚠️ **Backfilled and live numbers are reported separately and must stay that way.**
`recall_stats` carries `backfilled_events`, `live_hits`, `live_reads` and
`live_read_rate` next to the blended totals, because the definitions differ (the
live "useful" signal requires a read inside a window after a hit; a transcript
read is any read). Blended read rate **0.767** vs live **0.029** — quoting the
first alone would be a lying instrument.

Totals after the backfill: **958 hits / 735 reads**, **114 of 266** pages
surfaced at least once. Three findings that change how the engine and the wiki
are maintained:

- **`Wiki/log.md` dominates retrieval** — the **highest hit count of any page
  (127)** against only **49** opens, and it topped the results in two unrelated
  experiments (a candidate-dedup sweep, see
  [[mine-transcripts-for-recurring-complaints]], and an earlier ad-hoc query).
  The cause is structural: the changelog is long, append-only, and repeats every
  page's vocabulary, so it is an attractor for keyword scoring. **Open decision:
  take `log.md` out of the index, or give it a weighting bucket of its own.**
  Until then, treat a `log.md` top hit as noise rather than as an answer. (This
  is the promoted form of item 3 of
  [[2026-08-16-governance-model-and-machinery-open-questions]] — note that its
  pre-agreed trigger, "shows up under `surfaced_never_read`", never fired: the
  page *is* read. The discriminating figure was the hit/read **ratio**, not the
  bucket.)
- **`Wiki/index.md` is navigated to, not searched for** — **121 reads** against
  **2 hits**. It is an entry point agents open directly, so tuning its wording
  for retrieval would be effort spent on a path nobody takes; tune it for
  *reading*.
- **The wiki is not full of dead weight** — only **12 of 266** pages have never
  surfaced, and most of those were created the same day. That was the suspicion
  the telemetry was built to test, and the answer is no.

## Gotcha — HF_HUB_OFFLINE masquerades as "Could not load model from any source"

**Symptom**: fetching a **new** model fails with `Could not load model … from any
source` — which reads like a network problem or HuggingFace rate-limit.
**Root cause**: `server.py` pins `HF_HUB_OFFLINE=1` **by design** (so the cached
model is never silently re-downloaded); under that env a **first-time download of
a NEW model** must fail — but the error message doesn't say "offline mode", so it
looks transient. Diagnosis cost us a wrong "transient/network" explanation
(2026-07-04) before the pinned env var was spotted.

**Rule**: to fetch a new model **once**, load it in a process **without** the
offline pin; after the cache is populated (and the model passed
[[third-party-model-gate]]), the pin becomes exactly the re-download guard the
security audit wants. Verified 2026-07-04.

## Model registry (third-party-model-gate)

Per [[third-party-model-gate]]: every model running locally is listed here with
provenance, hashes, audit verdict, and eval result.

| | `all-MiniLM-L6-v2` | `paraphrase-multilingual-MiniLM-L12-v2` |
|---|---|---|
| Role | fallback (old index) | **production** |
| Source | hf:qdrant/all-MiniLM-L6-v2-onnx (fastembed default) | hf:qdrant/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q |
| Upstream | sentence-transformers | sentence-transformers |
| Revision | (pre-gate, unpinned) | `faf4aa4225822f3bc6376869cb1164e8e3feedd0` (cache refs/main) |
| Format | ONNX | ONNX protobuf, no PyOp/pickle/external-data (statically inspected) |
| sha256 (.onnx) | (pre-gate, not recorded) | `634d0f66c8...c376f` — full hashes in audit, backup verified |
| License | Apache-2.0 (known from source) | Apache-2.0 (known from source; no license file in cache) |
| Audit | grandfathered baseline (months in prod, pre-gate) | **SAFE-WITH-CONDITIONS**, security role, static review, 2026-07-04 |
| Eval | 42/50 hit@5 (DE 20/27) | **48/50 hit@5 (DE 26/27)** |

**Conditions in force**: (1) pinned snapshot backed up to
`<BACKUP_DIR>/models/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q-faf4aa42/`
(hashes re-verified on copy) — after any re-download, **re-verify sha256 against this
entry before first use** (fastembed resolves by name, not revision); (2) residual
risks: theoretical backdoored-embedding retrieval bias (low plausibility/impact —
hybrid BM25 leg + human review), license asserted from source not local file.

## Related pages

- [[agent-orchestration-options]]
- [[role-operations]]
- [[role-librarian]]
- [[karpathy-loop-and-agent-discipline]]
- [[third-party-model-gate]]
- [[failure-triggered-recall]] — failure-signature recall hook that queries this engine.
- [[cascaded-agent-memory]] — the memory-tier design this engine serves (Tier 2).
- [[windows-cp1252-piped-python-output]] — UTF-8 env rule for consumers of this engine's CLI on Windows.
- [[derived-usage-signals-not-self-reports]] — why the read signal is derived from behaviour instead of asked for, and how to read the hit/read shape.
- [[backfill-a-new-metric-from-existing-history]] — how six weeks of usage history were reconstructed on the metric's first day, and why blended and live numbers stay apart.
- [[mine-transcripts-for-recurring-complaints]] — the second use of the same transcript corpus; also where this engine's changelog dominance broke an automated dedup.
- [[silent-except-hides-dead-features]] — the lost-read bug this engine hit: a swallowed `database is locked` would have reported "0 reads" as a finding.
