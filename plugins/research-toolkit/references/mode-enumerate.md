# Enumerate — Exa Agent

Moved out of SKILL.md so it loads only when this mode runs. `$S` is the script path set in SKILL.md.

`agent_run` builds lists; it never establishes a fact. It returns a synthesis,
and Verify requires sources read directly. Before running, write down the
objective, what qualifies, the segments, the target count, the fields, and the
exclusions. `effort: low` is the default; raise it only when a run comes back
thin, and say which tier ran. Prices are in `exa-surface.md` for reference;
do not quote them to the user — with one exception, below.

**Agent Ultra** (`effort: "ultra"`) is the highest tier: metered rather than
fixed, typically about 30 minutes and up to 3 hours, default cap USD 20 (range
1–100). **The user has pre-approved it (2026-10-28): use it whenever judgement
says the extra completeness will change the answer — do not ask first.** Reach
for it when:

- the request is "every", "all", "the whole market" and the user will choose
  from the list, so a missed entrant is the costly error;
- a `high` or `xhigh` run came back thin, or segments are visibly missing;
- the qualifying criteria are hard to verify and each candidate needs checking;
- deep multi-source research where coverage is the point, not speed.

Not for a fact, a single entity, Verify (which reads pages directly), or
anything the user wants in minutes. Announce it in one line — that Ultra is
running, why, and the cap. Cap by judgement: the USD 20 default for a typical
exhaustive list, up to USD 100 for a large or multi-segment universe; add
`budget.maxDurationSeconds` (300–10800, Ultra only) when the user needs it
back sooner. Bound arrays with `maxItems`. It returns what it has near a
limit, so check `stopReason`: `schema_satisfied` is a finished run;
`budget_reached`, `time_limit_reached`, `iteration_limit_reached`,
`token_limit_reached` and `stopped` are partial, and the note must say so.
Resume the same `runId` over MCP rather than launching a duplicate. Details in
`exa-surface.md`.

- Pass a shallow `outputSchema` — top-level object, one bounded array, a source
  field per row, no citation or confidence fields (grounding comes back
  separately with per-field confidence).
- `input.exclusion` stops it re-returning what the long-list already has;
  `input.data` enriches rows the user holds.
- Keep the `runId`; resume with it rather than starting a duplicate. Extend a
  finished run with `previousRunId` rather than restating its context.
- `systemPrompt` steers behaviour, `outputSchema` steers shape. Don't conflate.
- For any verification-flavoured field, make it nullable and leave it out of
  `required` so the agent returns null instead of inventing a value, and use a
  `present | absent | cannot_verify` style enum — an unreachable page is not
  evidence of absence.

**Connect providers** (`dataSources`, up to five per run; nothing to install)
reach what the web index cannot. Name the provider-specific data in both the
query and the schema, or the agent falls back to web search.

- `particle` — 100,000+ podcast shows, transcribed and speaker-attributed. The
  only practical way to get what a person actually said in their own words, at
  length. Hear a practitioner before engaging them.
- `financial_datasets` — prices, fundamentals, earnings, SEC filings,
  ownership and screening for 27,000+ US tickers, plus ticker news. Ties a
  claim to reported numbers rather than coverage of them.
- `polymarket` — market-implied odds on dated, resolvable events. Read-only and
  free beyond the run. **Report it as a price, not a forecast**: "the market
  prices this at X", never a fact about the world, never the sole basis of a
  recommendation. Liquidity and spread say how much weight it deserves; a thin
  market is an opinion.

Providers compose — Polymarket plus Particle explains a move with the
commentary behind it. Four more are situational, with the rules that matter
here (full detail and prices in `exa-surface.md`):

- `similarweb` — traffic, rankings, competitors. **Modelled estimates**; say so
  wherever a figure is quoted. Billed per credit, scaling with rows × months, so
  keep both small.
- `fiber` — B2B company and people data and contact reveal. Billed per credit.
  Revealing emails or phone numbers is personal data about named people: ask
  first, and never carry it into a client deliverable without asking.
- `affiliate` — product catalogue and price comparison. The links are
  affiliate links; say so.
- `baselayer` (US business verification and officers), `jinko` (flights and
  hotels), `macrobond` (macro series; see the source map).

Billing on Fiber, Similarweb, Baselayer and Affiliate is on top of the run;
attach a provider only when the question needs it, and name its data in the
query and the schema or the agent will not call it.

**Coverage language.** Say "best-effort discovery" unless the universe was
bounded, the segments covered, the count checked, duplicates resolved and the
evidence inspected. Avoid "all", "complete", "exhaustive" without that.

