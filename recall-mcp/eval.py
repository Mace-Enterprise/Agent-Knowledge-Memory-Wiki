#!/usr/bin/env python3
"""recall-eval — does the recall engine surface the RIGHT pages (no nonsense)?

Run with the recall venv's python (needs the built index). It calls the engine's own
do_search and checks, per query, whether an expected page is in the top-K results.

Usage:  python eval.py [queryset.json]   (default: eval-queries.example.json beside this file)
queryset.json: [{"q": "...", "expect": ["slug", ...]}, ...]
  - expect = page basename(s) WITHOUT .md
  - a query HITS if ANY expected slug appears in the top-K results
Env: RECALL_EVAL_K (default 5). Exit code = number of misses (0 = all good).
"""
import os, sys, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("recall_server", os.path.join(HERE, "server.py"))
srv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srv)

K = int(os.environ.get("RECALL_EVAL_K", "5"))
qf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "eval-queries.example.json")
queries = json.load(open(qf, encoding="utf-8"))

def slug(path):
    return os.path.splitext(os.path.basename(path))[0]

misses = []
for item in queries:
    q, expect = item["q"], set(item["expect"])
    got = [slug(r["path"]) for r in srv.do_search(q, limit=K)]
    hit = bool(expect & set(got))
    if not hit:
        misses.append((q, sorted(expect), got))
    print(f"{'HIT ' if hit else 'MISS'} @{K}  {q[:55]:<55}  -> {got}")

n = len(queries)
print(f"\nrecall-eval: {n - len(misses)}/{n} hit@{K}  (miss-rate {len(misses)/n:.0%})  set={os.path.basename(qf)}")
for q, exp, got in misses:
    print(f"  MISS: '{q}'  expected one of {exp}, got {got}")
sys.exit(len(misses))
