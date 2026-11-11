# research-toolkit

One research plugin, Exa-first. A single entry point — say "research X", "what
are my options for Y", "monitor Z", or type `/research` — picks one of six modes,
enforces the human stops between the long-list, the scored cut and verification,
and writes a dated note to your PKM. Connector-class costs are not reported; the
only price stated is a scheduled monitor's recurring one.

## The six modes

| You want | Mode | Stops for you? |
| --- | --- | --- |
| A fact, one entity, a page read | Lookup | No |
| The landscape — who and what is out there | Sweep (Pass 1) | **Always** — you set the criteria and weights |
| Every candidate scored against them | Cut (decision-matrix) | **Always** — you approve the cut line |
| The truth about the survivors | Verify (Pass 2) | No |
| A structured list of a whole universe, with Particle / Financial Datasets / Polymarket when needed | Enumerate | No |
| A researched answer in one call — planned searches, grounded synthesis, per-field confidence | Deep | No |
| What is new, on a schedule | Watch | No |

## Components

- `skills/research/SKILL.md` — the router and the method. The only skill.
- `agents/searcher.md` — a Haiku subagent with the Exa search rules baked in.
  The fallback path for Sweep when the script cannot reach `api.exa.ai`.
- `references/exa-surface.md` — the Exa map by job, prices, filters, Connect
  providers, and what is unavailable (Websets, plan-gated).
- `references/data-index.md` — what Exa indexes beyond web pages (filings,
  transcripts, papers, patents, trials, approvals, case law, contracts, census,
  local businesses, podcasts, agent skills), mapped to this user's question
  types with the query shape each wants.
- `references/source-map.md` — which non-Exa source for which question:
  WebSearch, Elicit, PubMed, bioRxiv, alphaXiv, Readwise, Google Drive,
  Wolfram, CMS Coverage, NPI Registry, the browser, scheduled tasks.
- `references/query-patterns.md` — query writing and domain patterns, adapted
  from Exa's MIT-licensed `search` skill and corrected for the advanced tool.
- `references/output-template.md` — the dated note.
- `scripts/exa_extras.py` — stdlib-only CLI: `sweep` (file-based Pass 1),
  `deep` (Deep Search with additional directions, system prompt, text or
  object output schema checked against Exa's limits, highlights, grounding),
  `monitor-*` (Monitors), `webset-*` (gated by plan).
- `scripts/.exa_key` — **a live Exa API key in plaintext.**
- `.mcp.json` — declares the Exa connector as this plugin's search dependency.

## Before sharing this plugin with anyone

Delete `scripts/.exa_key`. The script falls back to the `EXA_API_KEY`
environment variable and then to `~/.exa_key`, so it keeps working for whoever
supplies their own.

## Relationship to Exa's own plugin

Keep Exa's `exa` plugin installed — it may be what supplies the MCP server, and
removing it is untested. This plugin never invokes its skills (`exa:search`,
`exa:exa-agent`): they were written for Exa's default two-tool install and tell
subagents to avoid the advanced search tool. The useful content from their
references is adapted, with credit, in `references/query-patterns.md`.

## Cloud sessions

`sweep`, `deep` and `monitor-*` call `api.exa.ai` directly, which a Cowork
cloud session reaches only if the organization allows that host (Organization
settings → Capabilities → Allow network egress). The MCP tools are unaffected.

## Rotating the key

Issue a new key at dashboard.exa.ai/api-keys, replace the one line in
`scripts/.exa_key`, repackage, reinstall.

## History

- 1.3.0 — Exa search best practices (exa.ai/docs/search/best-practices) and the
  data index (exa.ai/docs/search/data/*), both read 2026-10-07. `sweep` asks
  for capped highlights instead of page text, takes `--objective`, drops the
  deprecated `--include-text` / `--exclude-text` (terms go in the query), and
  runs each `--alt` as its own call — `additionalQueries` is Deep-only, so the
  old sweep had been silently ignoring alternates. `deep` gains `--objective`.
  Searcher agent and skill text aligned: highlights baseline, one content view
  per call, hard filters only when a violating result is unusable, recency
  (published-date) vs freshness (`maxAgeHours`) kept distinct. New
  `references/data-index.md`; source map gains Macrobond (Connect provider,
  free per call) and Exa-native rows for legal, procurement and census records.
  Live checks: `objective` accepted on `/search`; `includeText` still accepted
  but deprecated.
- 1.2.0 — Deep Search brought up to the full surface in exa.ai/docs/search/deep-search
  (read 2026-10-06): `deep` gains `--alt` (additionalQueries, max 10),
  `--system` (systemPrompt), `--text` / `--schema` (outputSchema, limits
  checked locally before the call), `--highlights`, `--category`,
  `--location`, `--moderation`, `--out`; renders synthesis, per-field
  grounding and confidence, and selected pages as Markdown. Skill and surface
  map rewritten for mode choice, query directions vs rephrasings, prompt vs
  schema, when to stay with ordinary search, and how to treat the synthesis.
  Live golden test: deep-lite, 4.9 s, synthesis matched the pricing page.
- 1.1.0 — aligned with the 2026-10 globals: no cost reporting for connector-class
  calls (monitor pricing stays); finalists are no longer picked by eye — a scored
  Cut step (criteria and weights from the user, every long-list row scored via
  decision-matrix, user approves the line) sits between Sweep and Verify; note
  template gains a Scored cut section and loses Cost; deferred-tool loading
  spelled out; `monitor-create` default webhook fixed (`example.com` is rejected
  by Exa — now the no-op URL the live monitor uses); `deep` accepts
  `YYYY-MM-DD` for `--since`/`--until` and gains `--exclude`; `sweep` output
  path guidance for cloud sessions. Prices re-checked against exa.ai/pricing
  2026-10-06, unchanged.
- 1.0.1 — minor fixes.
- 1.0.0 — one skill, six modes; searcher agent replaces the dependency on
  `exa:search`; `sweep` script; source map; query patterns; output template.
- 0.7.0 — exa-extras folded in; `exa-tools` skill; shared surface map.
- 0.6.x — override of `exa:search`'s tool ban; crawl-date correction.
- 0.5.0 — the two-pass method.
