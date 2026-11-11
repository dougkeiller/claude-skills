#!/usr/bin/env python3
"""
exa_extras.py — the Exa surfaces that have no MCP tool, driven from one script:
  sweep      file-based Pass 1: category-rotated /search (highlights + Exa-written
             summaries, each alternate phrasing its own call, optional objective),
             deduplicated by URL, written to longlist.md + .json
  deep       Deep Search (type=deep-lite|deep|deep-reasoning on /search) with
             additionalQueries, systemPrompt, outputSchema (text or object, limits
             checked locally), highlights, and a grounded synthesis printed with
             Exa's per-field confidence
  monitor-*  Monitors: create / list / get / run / runs / delete
  webset-*   Websets (gated: requires a Pro plan on the account)

Stdlib only. Key resolution: EXA_API_KEY, else .exa_key beside this script,
else ~/.exa_key. All four families were exercised against the live API on
2026-09-02; sweep measured 3 categories x 15 results -> 44 rows at $0.081.

  ./exa_extras.py sweep "description of the ideal page for the question" \
      --categories general,company,people,"personal site" --num 25 \
      --alt "second phrasing" --alt "third phrasing" \
      --objective "long-list of X for a buyer's comparison; vendor sites and first-hand reviews first" \
      --exclude-domains g2.com capterra.com --since 2025-01-01 --out research/longlist
  ./exa_extras.py deep "research question" --type deep --highlights \
      --alt "a different angle" --alt "another" \
      --system "Prefer primary sources; exclude duplicates" \
      --text "a grounded comparison organised by option"      # or --schema file.json
      --out research/deep-<topic>
  ./exa_extras.py monitor-create "what to watch" --name my-topic --period 1d --num 15
  ./exa_extras.py monitor-list
  ./exa_extras.py monitor-run mon_abc123        # trigger now, poll, print the output
  ./exa_extras.py monitor-delete mon_abc123
  ./exa_extras.py webset-create "query" --count 25 --criteria "..." --enrich "CEO name"
  ./exa_extras.py webset-status ws_abc123 --wait
  ./exa_extras.py webset-items  ws_abc123 --limit 50 --csv out.csv
"""
import argparse, csv, json, os, sys, time, urllib.error, urllib.request

BASE = "https://api.exa.ai"


def api_key():
    """EXA_API_KEY, else .exa_key beside this script (the plugin copy), else ~/.exa_key."""
    k = os.environ.get("EXA_API_KEY")
    if k:
        return k.strip()
    for p in (os.path.join(os.path.dirname(os.path.abspath(__file__)), ".exa_key"),
              os.path.expanduser("~/.exa_key")):
        try:
            with open(p) as f:
                k = f.read().strip()
            if k:
                return k
        except OSError:
            pass
    sys.exit("No Exa API key: set EXA_API_KEY, or put one in .exa_key beside this script.")


def call(method, path, body=None):
    key = api_key()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:1000]
        sys.exit(f"HTTP {e.code} on {method} {path}\n{detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {BASE} — {e.reason}\n"
                 "If this is a Cowork cloud session, egress to api.exa.ai is "
                 "probably still blocked by the organization network policy.")


def iso_start(d):
    """Accept YYYY-MM-DD or a full ISO 8601 timestamp; return the ISO form Exa wants."""
    return d if "T" in d else d + "T00:00:00.000Z"


def iso_end(d):
    return d if "T" in d else d + "T23:59:59.000Z"


def cost(resp):
    c = resp.get("costDollars")
    if c:
        print(f"[cost] ${c.get('total')}  {json.dumps({k: v for k, v in c.items() if k != 'total'})}",
              file=sys.stderr)


# --- Deep Search -----------------------------------------------------------
# Same /search endpoint, type=deep-lite|deep|deep-reasoning. Exa plans the
# search, runs several, inspects, refines, then selects and (with outputSchema)
# synthesises a grounded answer with per-field citations and confidence.
# Surface per https://exa.ai/docs/search/deep-search and the /search OpenAPI
# spec, read 2026-10-06:
#   additionalQueries  up to 10, deep types only — distinct directions, not rephrasings
#   systemPrompt       how to research and present (source preference, dedup, novelty)
#   outputSchema       root "text" (a prose synthesis) or "object"; <=10 properties
#                      counted at every level, <=2 levels of nested objects, every
#                      array needs items; validated server-side -> 400
#   contents           text / highlights as on any search; numResults bounds what is
#                      RETURNED, not how many searches Deep runs
#   stream             SSE, only meaningful with outputSchema — not used by this CLI
# All standard filters (domains, published dates, category, userLocation,
# moderation) are on the same request object and were accepted by the API.

def _schema_check(schema):
    """Mirror Exa's outputSchema limits so a bad schema fails here, not with a 400
    after the search has been planned. Returns a list of problems."""
    probs = []
    if schema.get("type") == "text":
        return probs
    if schema.get("type") != "object":
        return ['root "type" must be "text" or "object"']
    count = 0

    def walk(node, obj_depth):
        nonlocal count
        t = node.get("type")
        if t == "object":
            if obj_depth > 2:
                probs.append("more than 2 levels of nested objects below the root")
            for name, sub in (node.get("properties") or {}).items():
                count += 1
                walk(sub, obj_depth + 1 if sub.get("type") == "object" else obj_depth)
        elif t == "array":
            if "items" not in node:
                probs.append("an array field has no items")
            else:
                items = node["items"]
                walk(items, obj_depth + 1 if items.get("type") == "object" else obj_depth)

    walk(schema, 0)
    if count > 10:
        probs.append(f"{count} properties in total; the limit is 10 across all levels")
    return probs


def _load_schema(a):
    if a.text:
        return {"type": "text", "description": a.text}
    if a.schema:
        s = a.schema
        if os.path.exists(s):
            with open(s) as f:
                s = f.read()
        try:
            schema = json.loads(s)
        except json.JSONDecodeError as e:
            sys.exit(f"--schema is not valid JSON: {e}")
        probs = _schema_check(schema)
        if probs:
            sys.exit("outputSchema would be rejected by Exa:\n  - " + "\n  - ".join(probs))
        return schema
    return None


def deep(a):
    if a.alt and len(a.alt) > 10:
        sys.exit("--alt: Exa accepts at most 10 additional queries")
    contents = {}
    if a.chars > 0:
        contents["text"] = {"maxCharacters": a.chars}
    if a.highlights:
        contents["highlights"] = True
    body = {"query": a.query, "type": a.type, "numResults": a.num}
    if contents:
        body["contents"] = contents
    if a.alt:
        body["additionalQueries"] = a.alt
    if a.objective:
        body["objective"] = a.objective
    if a.system:
        body["systemPrompt"] = a.system
    schema = _load_schema(a)
    if schema:
        body["outputSchema"] = schema
    if a.category:
        body["category"] = a.category
    if a.include:
        body["includeDomains"] = a.include
    if a.exclude:
        body["excludeDomains"] = a.exclude
    if a.since:
        body["startPublishedDate"] = iso_start(a.since)
    if a.until:
        body["endPublishedDate"] = iso_end(a.until)
    if a.location:
        body["userLocation"] = a.location
    if a.moderation:
        body["moderation"] = True

    t0 = time.time()
    r = call("POST", "/search", body)
    secs = time.time() - t0
    cost(r)
    print(f"[deep] type={a.type}  {secs:.1f}s  {len(r.get('results', []))} results returned", file=sys.stderr)

    lines = [f"# Deep Search — {a.query}", "",
             f"{time.strftime('%Y-%m-%d')} · type `{a.type}` · {len(r.get('results', []))} selected pages"
             + (f" · {len(a.alt)} additional directions" if a.alt else ""), ""]
    out = r.get("output") or {}
    if out:
        content = out.get("content")
        lines += ["## Synthesis (Exa-generated; verify every consequential figure against its page)", ""]
        if isinstance(content, str):
            lines += [content, ""]
        else:
            lines += ["```json", json.dumps(content, indent=2), "```", ""]
        grounding = out.get("grounding") or []
        if grounding:
            lines += ["## Grounding — per field, Exa's own confidence", ""]
            lows = 0
            for g in grounding:
                conf = g.get("confidence", "?")
                if conf == "low":
                    lows += 1
                cites = "; ".join(f"[{c.get('title') or c.get('url')}]({c.get('url')})"
                                  for c in g.get("citations", []))
                lines.append(f"- `{g.get('field')}` — **{conf}** — {cites or '(no citation)'}")
            lines.append("")
            if lows:
                lines += [f"_{lows} field(s) at low confidence: treat as unverified._", ""]
    lines += ["## Selected pages", ""]
    for i, res in enumerate(r.get("results", []), 1):
        date = (res.get("publishedDate") or "")[:10]
        lines.append(f"{i}. **{res.get('title') or '(untitled)'}**  \n   {res.get('url')}"
                     + (f"  \n   _{date}_" if date else ""))
        for h in (res.get("highlights") or [])[:3]:
            lines.append(f"   > {h.strip().replace(chr(10), ' ')[:300]}")
        txt = (res.get("text") or "").strip().replace("\n", " ")
        if txt and not res.get("highlights"):
            lines.append(f"   {txt[:300]}")
        lines.append("")
    md = "\n".join(lines)

    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out + ".md", "w") as f:
            f.write(md)
        with open(a.out + ".json", "w") as f:
            json.dump({"request": body, "response": r}, f, indent=1)
        print(f"→ {a.out}.md / {a.out}.json")
    else:
        print(md)
    if a.json:
        print(json.dumps(r, indent=2))


def webset_create(a):
    search = {"query": a.query, "count": a.count}
    if a.criteria:
        search["criteria"] = [{"description": c} for c in a.criteria]
    if a.entity:
        search["entity"] = {"type": a.entity}
    body = {"search": search}
    if a.enrich:
        ens = []
        for e in a.enrich:
            desc, _, fmt = e.partition(":")
            ens.append({"description": desc, "format": fmt or "text"})
        body["enrichments"] = ens
    r = call("POST", "/websets/v0/websets/", body)
    print(json.dumps(r, indent=2))
    wid = r.get("id")
    if wid:
        print(f"\nwebset id: {wid}\npoll: {sys.argv[0]} webset-status {wid}", file=sys.stderr)


def webset_status(a):
    r = call("GET", f"/websets/v0/websets/{a.id}")
    print(json.dumps({k: r.get(k) for k in ("id", "status", "searches", "enrichments")}, indent=2))
    if a.wait:
        while r.get("status") not in ("idle", "paused", "failed", None):
            time.sleep(a.interval)
            r = call("GET", f"/websets/v0/websets/{a.id}")
            print(f"  status: {r.get('status')}", file=sys.stderr)
        print(f"final status: {r.get('status')}")


def webset_items(a):
    r = call("GET", f"/websets/v0/websets/{a.id}/items?limit={a.limit}")
    items = r.get("data", [])
    print(f"{len(items)} items", file=sys.stderr)
    if a.csv:
        rows = []
        for it in items:
            row = {"id": it.get("id"), "url": (it.get("properties") or {}).get("url", "")}
            for en in it.get("enrichments", []) or []:
                row[en.get("description", "enrichment")] = en.get("result")
            rows.append(row)
        keys = sorted({k for r_ in rows for k in r_})
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {a.csv}")
    else:
        print(json.dumps(items, indent=2))



# --- Monitors -------------------------------------------------------------
# Scheduled recurring searches. $15/1k requests (exa.ai/pricing, read
# 2026-09-02); which calls bill is not documented — assume each RUN does.
# A webhook URL is required by the API even when you never consume it: results
# are readable with monitor-runs / monitor-run. Exa rejects example.com,
# localhost, .local and private IPs, so the default is a no-op path on a real
# public host (the one the live monitor created 2026-09-02 uses). `trigger` is
# optional — omit --period for a manual-only monitor.

def monitor_create(a):
    body = {
        "search": {"query": a.query, "numResults": a.num},
        "webhook": {"url": a.webhook},
    }
    if a.name:
        body["name"] = a.name
    if a.period:
        body["trigger"] = {"type": "interval", "period": a.period}
    if a.describe:
        body["outputSchema"] = {"type": "text", "description": a.describe}
    r = call("POST", "/monitors", body)
    secret = r.pop("webhookSecret", None)
    print(json.dumps(r, indent=2))
    if secret:
        print("\nwebhookSecret returned once and not stored by this script; "
              "irrelevant unless you consume the webhook.", file=sys.stderr)
    if a.period:
        print(f"scheduled every {a.period}", file=sys.stderr)
    else:
        print("manual-only (no schedule) — run it with monitor-run", file=sys.stderr)


def monitor_list(a):
    q = f"?limit={a.limit}" + (f"&status={a.status}" if a.status else "")
    r = call("GET", "/monitors" + q)
    data = r.get("data", [])
    if not data:
        print("no monitors")
        return
    for m in data:
        trig = (m.get("trigger") or {}).get("period", "manual")
        print(f"{m.get('id')}  {m.get('status','?'):8}  every {trig:6}  "
              f"{m.get('name') or (m.get('search') or {}).get('query','')[:60]}")


def monitor_get(a):
    print(json.dumps(call("GET", f"/monitors/{a.id}"), indent=2))


def monitor_delete(a):
    r = call("DELETE", f"/monitors/{a.id}")
    print(f"deleted {r.get('id', a.id)}")


def monitor_runs(a):
    r = call("GET", f"/monitors/{a.id}/runs?limit={a.limit}")
    for run in r.get("data", []):
        print(f"{run.get('id')}  {run.get('status')}  {run.get('createdAt','')}")


def monitor_run(a):
    """Trigger a run now, poll until it finishes, print the output."""
    call("POST", f"/monitors/{a.id}/trigger")
    print("triggered", file=sys.stderr)
    latest = None
    for _ in range(a.tries):
        time.sleep(a.interval)
        runs = call("GET", f"/monitors/{a.id}/runs?limit=1").get("data", [])
        if not runs:
            continue
        latest = runs[0]
        print(f"  {latest.get('status')}", file=sys.stderr)
        if latest.get("status") in ("completed", "failed", "canceled"):
            break
    if not latest:
        sys.exit("no run appeared")
    if latest.get("status") != "completed":
        sys.exit(f"run ended {latest.get('status')}")
    run = call("GET", f"/monitors/{a.id}/runs/{latest['id']}")
    out = run.get("output") or {}
    if isinstance(out, dict) and out.get("results"):
        for res in out["results"]:
            print(f"- {res.get('title') or '(untitled)'}\n  {res.get('url')}")
    else:
        print(json.dumps(out, indent=2) if out else "(no new results this run)")



# --- Sweep: a file-based Pass 1 --------------------------------------------
# Category-rotated advanced searches against /search, deduplicated by URL,
# with Exa writing the one-line annotation per row (summary, $0.001/page).
# Raw results never enter the model's context: read the .md it writes.

SEMANTIC_ONLY = {"company", "people"}   # reject excludeDomains and published-date filters with a 400
SUMMARY_Q = "What is this, and who is it for, in one sentence."


def sweep(a):
    cats = [c.strip() for c in a.categories.split(",") if c.strip()]
    if not cats:
        cats = ["general"]
    # additionalQueries is accepted only by the deep types (spec, 2026-10-07), so
    # on `auto` each alternate phrasing is its own call. Dedup by URL below.
    queries = [a.query] + (a.alt or [])
    seen, rows, total, calls = {}, [], 0.0, []
    for cat, q in ((c, q) for c in cats for q in queries):
        # Highlights, not text: Exa sizes excerpts to relevance (its own evals put
        # 500 chars of highlights level with 8,000 of text). Capped here because a
        # long-list wants one line per row; Deep leaves them uncapped.
        contents = {"highlights": {"maxCharacters": a.chars},
                    "summary": {"query": a.summary_query or SUMMARY_Q}}
        if a.full_text:
            contents = {"text": {"maxCharacters": a.chars}, "summary": contents["summary"]}
        body = {"query": q, "type": "auto", "numResults": a.num, "contents": contents}
        if cat != "general":
            body["category"] = cat
        if a.objective:
            body["objective"] = a.objective
        if cat not in SEMANTIC_ONLY:
            if a.exclude_domains:
                body["excludeDomains"] = a.exclude_domains
            if a.include_domains:
                body["includeDomains"] = a.include_domains
            if a.since:
                body["startPublishedDate"] = iso_start(a.since)
            if a.until:
                body["endPublishedDate"] = iso_end(a.until)
        if a.location:
            body["userLocation"] = a.location
        r = call("POST", "/search", body)
        c = (r.get("costDollars") or {}).get("total") or 0.0
        total += c
        res = r.get("results", [])
        calls.append({"category": cat, "query": q, "results": len(res), "cost": c})
        print(f"  {cat:14} {len(res):3} results  {q[:50]}", file=sys.stderr)
        for x in res:
            url = x.get("url")
            if not url:
                continue
            if url in seen:
                if cat not in seen[url]["also_in"] and cat != seen[url]["category"]:
                    seen[url]["also_in"].append(cat)
                continue
            snippet = " ".join(h.strip() for h in (x.get("highlights") or [])) or (x.get("text") or "")
            row = {
                "n": len(rows) + 1,
                "title": (x.get("title") or "").strip() or "(untitled)",
                "url": url,
                "summary": (x.get("summary") or "").strip(),
                "snippet": snippet.strip().replace("\n", " ")[: a.chars],
                "published": (x.get("publishedDate") or "")[:10],
                "author": (x.get("author") or "").strip(),
                "category": cat,
                "also_in": [],
            }
            seen[url] = row
            rows.append(row)

    out = a.out
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    meta = {"query": a.query, "alt": a.alt or [], "objective": a.objective or "",
            "categories": cats, "num": a.num,
            "date": time.strftime("%Y-%m-%d"), "calls": calls,
            "unique": len(rows), "cost_total": round(total, 4)}
    with open(out + ".json", "w") as f:
        json.dump({"meta": meta, "rows": rows}, f, indent=1)
    with open(out + ".md", "w") as f:
        f.write(f"# Long-list — {a.query}\n\n")
        f.write(f"{meta['date']} · {len(rows)} unique results across "
                f"{', '.join(cats)} · {len(queries)} phrasing(s) · {len(calls)} calls\n\n")
        f.write("Rows are Exa similarity, not validation. Annotations are Exa-written "
                "summaries of each page, not verified facts.\n\n")
        for r_ in rows:
            tag = r_["category"] + ("" if not r_["also_in"] else " +" + ",".join(r_["also_in"]))
            date = f" · {r_['published']}" if r_["published"] else ""
            f.write(f"{r_['n']}. **{r_['title']}** — {r_['summary'] or r_['snippet'][:200]}  \n")
            f.write(f"   {r_['url']}  \n   _{tag}{date}_\n\n")
    print(f"[cost] ${total:.3f} across {len(calls)} calls", file=sys.stderr)
    print(f"\n{len(rows)} unique results → {out}.md / {out}.json")


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)

d = sub.add_parser("deep", help="Deep Search on /search: planned, iterative, optionally synthesised with grounding")
d.add_argument("query", help="what to research, as a question or a description of the ideal evidence")
d.add_argument("--type", default="deep", choices=["deep-lite", "deep", "deep-reasoning"],
               help="deep (default) for research; deep-lite when latency matters; deep-reasoning for conflicting evidence")
d.add_argument("--alt", action="append",
               help="additionalQueries (max 10): each a meaningfully different direction, not a rephrasing")
d.add_argument("--objective", help="the larger task this search serves: what should rank first, what to exclude, which facts to pull")
d.add_argument("--system", help="systemPrompt: HOW to research and present — source preferences, dedup, novelty")
d.add_argument("--schema", help='outputSchema as JSON or a path to a .json file (root type "object"; <=10 properties, <=2 nested levels)')
d.add_argument("--text", help='outputSchema of type "text": a one-line description of the prose synthesis wanted')
d.add_argument("--highlights", action="store_true", help="return highlights (evidence snippets) per page")
d.add_argument("--num", type=int, default=10, help="pages returned in results; does not limit Deep's internal searches")
d.add_argument("--chars", type=int, default=600, help="text per page; 0 to omit text")
d.add_argument("--category", help="company | publication | news | personal site | financial report | people")
d.add_argument("--include", nargs="*", help="includeDomains")
d.add_argument("--exclude", nargs="*", help="excludeDomains")
d.add_argument("--since", help="YYYY-MM-DD (or full ISO 8601)")
d.add_argument("--until", help="YYYY-MM-DD (or full ISO 8601)")
d.add_argument("--location", help="ISO country code, e.g. US")
d.add_argument("--moderation", action="store_true")
d.add_argument("--out", help="path prefix; writes .md and .json instead of printing")
d.add_argument("--json", action="store_true", help="also dump the raw response")
d.set_defaults(func=deep)

c = sub.add_parser("webset-create")
c.add_argument("query")
c.add_argument("--count", type=int, default=10)
c.add_argument("--criteria", action="append")
c.add_argument("--enrich", action="append", help='"description" or "description:number|text|date|boolean"')
c.add_argument("--entity", help="company | person | article | research_paper")
c.set_defaults(func=webset_create)

s = sub.add_parser("webset-status")
s.add_argument("id")
s.add_argument("--wait", action="store_true")
s.add_argument("--interval", type=int, default=10)
s.set_defaults(func=webset_status)

i = sub.add_parser("webset-items")
i.add_argument("id")
i.add_argument("--limit", type=int, default=25)
i.add_argument("--csv")
i.set_defaults(func=webset_items)

mc = sub.add_parser("monitor-create")
mc.add_argument("query")
mc.add_argument("--name")
mc.add_argument("--num", type=int, default=10)
mc.add_argument("--period", help='e.g. 1h, 6h, 1d, 7d — min 1h; omit for manual-only')
mc.add_argument("--describe", help="how the run output should be written")
mc.add_argument("--webhook", default=os.environ.get("EXA_MONITOR_WEBHOOK", ""),
                help="required by the API and never consumed; must be a real public host "
                     "(Exa rejects example.com, localhost, .local and private IPs)")
mc.set_defaults(func=monitor_create)

ml = sub.add_parser("monitor-list")
ml.add_argument("--limit", type=int, default=50)
ml.add_argument("--status", choices=["active", "paused", "disabled"])
ml.set_defaults(func=monitor_list)

mg = sub.add_parser("monitor-get"); mg.add_argument("id"); mg.set_defaults(func=monitor_get)
md = sub.add_parser("monitor-delete"); md.add_argument("id"); md.set_defaults(func=monitor_delete)

mr = sub.add_parser("monitor-runs")
mr.add_argument("id"); mr.add_argument("--limit", type=int, default=10)
mr.set_defaults(func=monitor_runs)

mx = sub.add_parser("monitor-run")
mx.add_argument("id")
mx.add_argument("--interval", type=int, default=5)
mx.add_argument("--tries", type=int, default=36)
mx.set_defaults(func=monitor_run)

sw = sub.add_parser("sweep", help="file-based Pass 1: category-rotated searches -> longlist.md")
sw.add_argument("query", help="describe the ideal page, not keywords")
sw.add_argument("--categories", default="general,company,people,personal site",
                help="comma-separated; 'general' = no category filter")
sw.add_argument("--num", type=int, default=25, help="results per category (1-100)")
sw.add_argument("--alt", action="append",
                help="alternate phrasings, each run as its own call per category (a different angle, not a synonym)")
sw.add_argument("--objective", help="the goal this sweep serves: what should rank first, what to exclude, what to pull — "
                                    "Exa uses it to rank; put source preferences here, not in a domain filter")
sw.add_argument("--chars", type=int, default=400, help="cap on highlight (or text) characters per row")
sw.add_argument("--full-text", action="store_true", help="request page text instead of highlights (rarely needed)")
sw.add_argument("--summary-query", help="what the one-line annotation should answer")
sw.add_argument("--exclude-domains", nargs="*", help="hard filter: only when a result from there would be unusable")
sw.add_argument("--include-domains", nargs="*", help="hard filter: only when results must come from approved sources")
sw.add_argument("--since", help="YYYY-MM-DD; general-index categories only")
sw.add_argument("--until", help="YYYY-MM-DD; general-index categories only")
sw.add_argument("--location", help="ISO country code, e.g. US")
sw.add_argument("--out", default="research/longlist", help="path prefix; writes .md and .json")
sw.set_defaults(func=sweep)

a = p.parse_args()
a.func(a)
