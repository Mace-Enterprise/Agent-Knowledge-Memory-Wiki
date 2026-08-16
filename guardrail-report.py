#!/usr/bin/env python3
"""Which guardrails actually bite? Report, do not guess.

Joins three things:
  1. the guardrails that exist          (Wiki/guardrails/*.md)
  2. the events they produced           (guardrail-events.jsonl)
  3. what each one declares about itself (**Enforcement**: hook|audit|advisory)

The interesting output is not the counts but the GAPS:
  - a guardrail with an enforcement point but zero events  -> the control never ran
  - a guardrail that only ever reports "checked"           -> it has never caught anything;
    either the failure does not occur, or the check is looking in the wrong place
  - a guardrail declared advisory                          -> honest: it cannot block, and
    is measured through complaints instead of through events
  - a guardrail with no declaration at all                 -> unmeasured, and that is the
    finding: 0 of 23 declared one when this report was first written.

    python guardrail-report.py [--wiki DIR] [--log FILE]
"""
import io, json, os, re, sys, glob, collections

def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

# Default: the sibling Wiki/ in this repo. Never a real machine path — the pre-push
# gate refused this file once for exactly that, which is the gate working.
WIKI = arg("--wiki", os.environ.get(
    "WIKI_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "Wiki")))
LOG = arg("--log", os.environ.get(
    "GUARDRAIL_LOG",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "recall-mcp", "guardrail-events.jsonl")))

# --- 1) declared guardrails -------------------------------------------------------------
declared = {}
for f in sorted(glob.glob(os.path.join(WIKI, "guardrails", "*.md"))):
    slug = os.path.splitext(os.path.basename(f))[0]
    head = io.open(f, encoding="utf-8", errors="replace").read()[:3000]
    m = re.search(r"^\*\*Enforcement\*\*:\s*(.+)$", head, re.M)
    j = re.search(r"^\*\*Justification\*\*:\s*(.+)$", head, re.M)
    declared[slug] = (m.group(1).strip()[:40] if m else None,
                      j.group(1).strip()[:40] if j else "—")

# --- 2) events --------------------------------------------------------------------------
events = collections.defaultdict(collections.Counter)
last = {}
total = 0
if os.path.exists(LOG):
    for line in io.open(LOG, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        g, e = d.get("guardrail", "?"), d.get("event", "?")
        events[g][e] += 1
        last[g] = max(last.get(g, ""), d.get("ts", ""))
        total += 1

print(f"Guardrails: {len(declared)}   Ereignisse: {total}   Log: {LOG}")
undeclared = [g for g, (e, _j) in declared.items() if not e]
print(f"ohne Enforcement-Angabe: {len(undeclared)} von {len(declared)}\n")

rows = []
for slug, (enf, just) in sorted(declared.items()):
    c = events.get(slug, collections.Counter())
    rows.append((slug, enf or "—", c["checked"], c["blocked"], c["violated"],
                 c["bypassed"], (last.get(slug) or "")[:10], just))

print(f"{'guardrail':52} {'enforcement':14} {'lief':>5} {'blockte':>7} {'verletzt':>8} {'zuletzt':>11}")
for slug, enf, ch, bl, vi, by, ts, _j in rows:
    if not (ch or bl or vi or by):
        continue
    print(f"{slug[:52]:52} {enf[:14]:14} {ch:5} {bl:7} {vi:8} {ts:>11}")

silent = [(s, e, j) for s, e, ch, bl, vi, by, _, j in rows if not (ch or bl or vi or by)]
print(f"\n=== ohne jedes Ereignis: {len(silent)} von {len(declared)} ===")
for slug, enf, _j in silent[:40]:
    note = "advisory — per Beschwerde-Auswertung messbar" if enf.lower().startswith("advis") \
        else ("KONTROLLE LIEF NIE" if enf != "—" else "nicht instrumentiert, nicht deklariert")
    print(f"  {slug[:56]:56} {note}")

never_caught = [s for s, e, ch, bl, vi, by, _, _j in rows if ch and not bl and not vi]
if never_caught:
    print(f"\n=== lief, hat aber nie etwas gefangen: {len(never_caught)} ===")
    print("    (entweder tritt der Fehler nicht auf, oder die Pruefung sucht an der falschen Stelle)")
    for s in never_caught[:15]:
        print(f"  {s}")


# --- evaluation: is each rule earning its keep? -----------------------------------------
# Data for a decision, not a decision. Retiring a rule is the owner's call; what this can
# do is stop the ratchet where rules only ever accumulate.
print("\n=== Auswertung: verdient die Regel ihren Platz? ===")
buckets = {"erzwungen, hat schon gefangen": [], "erzwungen, nie gefangen": [],
           "advisory, Beschwerden bekannt": [], "advisory, kein Signal": [],
           "deklariert, Kontrolle lief nie": []}
for slug, enf, ch, bl, vi, by, ts, just in rows:
    advisory = enf.lower().startswith("advis")
    if not advisory and (bl or vi):
        buckets["erzwungen, hat schon gefangen"].append((slug, just, f"{bl} blockiert"))
    elif not advisory and ch:
        buckets["erzwungen, nie gefangen"].append((slug, just, f"{ch}x gelaufen"))
    elif not advisory:
        buckets["deklariert, Kontrolle lief nie"].append((slug, just, "kein Ereignis"))
    elif vi:
        buckets["advisory, Beschwerden bekannt"].append((slug, just, f"{vi} Verstoesse"))
    else:
        buckets["advisory, kein Signal"].append((slug, just, "keine Daten"))

HINT = {
    "erzwungen, hat schon gefangen": "behalten - belegt wirksam",
    "erzwungen, nie gefangen":       "beobachten - verhindert vielleicht nichts, oder prueft an der falschen Stelle",
    "deklariert, Kontrolle lief nie": "REPARIEREN - die Regel behauptet eine Kontrolle, die nicht laeuft",
    "advisory, Beschwerden bekannt": "Kandidat fuer echte Durchsetzung",
    "advisory, kein Signal":         "unbewertbar - kein Kanal. Erst messen, dann urteilen",
}
for name, items in buckets.items():
    if not items:
        continue
    print(f"\n  {name}  ({len(items)})  -> {HINT[name]}")
    for slug, just, note in items[:12]:
        print(f"     {slug[:50]:50} {note:16} {just[:34]}")
