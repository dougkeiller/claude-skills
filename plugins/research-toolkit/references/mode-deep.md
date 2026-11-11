# Deep — Deep Search

Moved out of SKILL.md so it loads only when this mode runs. `$S` is the script path set in SKILL.md.

Same endpoint as an ordinary search, but Exa plans the search, runs several,
inspects the evidence, refines where it is thin or contradictory, then selects
pages and — if asked — synthesises a grounded answer with a citation and a
confidence per field. Use it when one retrieval pass cannot settle the
question; stay with an ordinary search when the query already names a specific
source or narrow topic, or when the job is to find pages for this skill to
read. Run it without a price preamble.

**Mode.** `deep` by default — Exa's recommended type for research workflows.
`deep-lite` when latency matters and the question is simple (about 4 s).
`deep-reasoning` is now labelled **legacy** on Exa's Deep Search page (read
2026-10-28); try `deep` first and use it only if `deep` comes back thin on
genuinely conflicting evidence (12–40 s). For long-running list-building or
multi-hop enrichment Exa itself points to `agent_run` instead, which is
Enumerate (and Agent Ultra when completeness is the point). Deep is the
default whenever an `outputSchema` of three or more fields is needed; for a
small structured answer, an ordinary search with `outputSchema` is enough.

**Shape the request in four separate parts, and keep them separate:**

- `query` — *what* to research, as a question or a description of the ideal
  evidence.
- `--alt` (`additionalQueries`, up to 10, Deep-only) — meaningfully different
  *directions*: a sceptic's angle, a builder's angle, a competitor's name, a
  regulator's term, a different sub-problem. Never rephrasings; Deep expands
  the main query itself.
- `--objective` — the task the search serves (what should rank first, what to
  exclude, what to pull); works on every search type.
- `--system` (`systemPrompt`) — *how* to research and present: source
  preferences ("prefer the vendor's own pricing page and regulator filings"),
  deduplication, novelty, what to exclude.
- `--text "…"` or `--schema file.json` (`outputSchema`) — the *shape* of the
  answer, and the thing that turns on synthesis. `--text` gives a grounded
  prose synthesis; `--schema` gives structured fields. Object schemas are
  capped at 10 properties counted at every level, 2 levels of nested objects,
  and every array needs `items` — the script checks this before spending the
  call. Do not add citation or confidence fields; Exa returns them.

`--highlights` returns the evidence snippets Deep used; prefer it to full text
on a Deep call. `--num` bounds the pages *returned*, not the searches Deep
runs. All ordinary filters apply (`--include`, `--exclude`, `--since`,
`--until`, `--category`, `--location`). Write to `--out` so the raw response
stays out of context.

```bash
python3 "$S" deep "How do the leading X vendors handle Y, and where do they differ?" \
  --type deep --highlights --chars 0 --num 10 \
  --alt "customer complaints about Y in X tools" --alt "X vendor pricing page Y feature" \
  --objective "comparison for a buyer choosing between X vendors; pull how each handles Y and its price" \
  --system "Prefer vendors' own documentation and first-hand practitioner accounts; drop roundups and duplicates" \
  --text "A grounded comparison organised by vendor, each claim tied to its source" \
  --since YYYY-MM-DD --out <session output dir>/<topic>-deep
```

**Reading the result.** The synthesis is Exa-generated: a strong *draft* of
the answer, not a verified one. Every consequential figure still gets read on
its page before it carries a decision (Verify's rules), and the note says it
came "via Deep synthesis, confirmed on the page" or "via Deep synthesis,
unconfirmed". Exa's confidence is per field: treat `low` as unverified
outright, and treat `high` as a reason to go and look, not a substitute. When
Deep returns fewer pages than asked, or the grounding cites one source for
several fields, say so — that is the shape of the evidence.

