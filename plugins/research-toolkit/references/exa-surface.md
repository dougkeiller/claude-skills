# The Exa surface, by job

One map for the whole of Exa. The line between "MCP tool" and "REST endpoint" is
an accident of what the connector happens to expose — it is not a distinction
that means anything while you are researching, so it does not organise this file.
Jobs do.

Prices below were read from https://exa.ai/pricing on 2026-09-02 and re-checked
unchanged on 2026-10-06, and re-checked against exa.ai/docs/admin/pricing on
2026-10-28 (raw page text): `lite` is $4/1k, `auto` $7/1k, `instant`/`fast` are
legacy at their old prices. They are reference, not reporting: the user's standing
rule is that connector-class calls are not costed in conversation. State a
price only for a scheduled monitor or a Websets upgrade.

| Job | Reach for | Price |
| --- | --- | --- |
| Discover candidates | `web_search_advanced_exa` | $7/1k requests, +$0.001 per result past 10 |
| Read a page | `web_fetch_exa` | $1/1k pages per content type |
| Enumerate a universe | `agent_run` + `outputSchema` | $0.012–$1.00 fixed by effort; `auto` metered to a $5 cap; `ultra` metered to a $20 cap |
| Exhaustive list or deep multi-source research where completeness beats cost and time | `agent_run` with `effort: "ultra"` | Metered, default cap $20, up to $100; typically ~30 min, up to 3 h |
| Research a question in one call, with a grounded synthesis | `deep` via the script | $12/1k (`deep-lite`, `deep`); `deep-reasoning` $15/1k but now labelled legacy |
| Watch for what is new | `monitor-*` via the script | $15/1k requests; assume each run bills |
| Reach past the open web | `dataSources` on `agent_run` | provider rates on top of the run |

## Discover — `web_search_advanced_exa`

The workhorse; use it for nearly every search. `web_search_exa` is a fallback
only — `query` and `numResults`, nothing else, and no content cap, which is how
a sweep blows the context window. Ask for **highlights** rather than text (Exa's
recommended default: relevance-sized excerpts, and its evals put 500 characters
of highlights level with 8,000 of text); request one content view per call.
Pass `objective` — the task the search serves — on anything beyond a quick
lookup; it steers ranking and is where a source *preference* belongs. Only the
script sends it: the MCP `web_search_advanced_exa` tool has no `objective`
field (schema checked 2026-10-28), so on an MCP call the preference goes in the
query wording instead. Rotate
`category` (`company`, `people`, `personal site`, `publication`, `news`,
`financial report`, `pdf`, `github`); each index holds different entities.
`company` and `people` run on semantic-only indices that reject
`excludeDomains` and date ranges with a 400. `includeText` / `excludeText` are
deprecated (terms go in the query); `additionalQueries` is accepted only by
the deep types, so an ordinary sweep runs each phrasing as its own call.
Domain filters accept hostnames, hostname + path prefix, and `*.wildcards`.

Width is nearly free: one 50-result sweep costs about $0.05 and covers more
ground than five ten-result searches at $0.035.

**Search `type`** (Exa best-practices and the MCP tool schema, read 2026-10-28).
`auto` is the default and supports every parameter. `lite` is the low-cost,
low-latency type: it serves **cached content only**, rejects
`contents.maxAgeHours` with any value (including `-1`), and supports only
`query`, `numResults`, `category`, the domain and published-date filters,
`userLocation`, `moderation`, `textMaxCharacters` and the highlights
parameters. Use it for real-time paths where cached content is acceptable,
never where freshness matters. `fast` and `instant` are legacy: use `lite`
instead, or `auto` when a parameter `lite` lacks is needed. Change the type
last — a different type cannot repair an underspecified query.

**Rules from Exa's best-practices page** (read 2026-10-28), beyond those above:

- Change one thing at a time, in this order: clarify the query (subject, source
  type, period — "describe the pages you want, not a bag of keywords"); read
  the response in layers (title, URL, `publishedDate`, highlights); add hard
  constraints only where a violating result is unusable; change the type last.
- Preferred sources go in the query phrasing or `systemPrompt`; approved-only
  sources go in `includeDomains`, never `site:` in the query. A `site:` or
  quoted phrase that matches nothing is dropped, and the response says so with
  a `RESTRICTIONS_RELAXED` notice.
- `notices` describe how results were produced: pass them to the model with the
  results. `warnings` describe request problems (`IGNORED_FIELD` for a field
  with no effect): log them, never pass them to a model. Handle unknown codes by
  their `message`.
- Small structured output: `outputSchema` on a standard search, not Deep by
  default. Multi-item research output: `deep` with `outputSchema`, or Agent.
  More context from a few pages: search with highlights, then Contents.
- `contents.snapshotAsOf` replaces `contents.crawledBeforeDate`;
  `livecrawl: "always"` is `contents.maxAgeHours: 0` (never send both).
  `includeUrls`/`excludeUrls` are `includeDomains`/`excludeDomains`; top-level
  `text`/`highlights`/`summary` nest under `contents`; `useAutoprompt`,
  `numSentences`, `highlightsPerUrl` and `tokensNum` are gone.
- Highlights, text and summary are each billed separately: request only what
  the task needs. `summary` is one extra model call per result.
- `userIdentifier` (1–64 characters, letters, digits, `_`, `-`) attributes a
  request to an end user for telemetry only. It accepts an opaque ID, never an
  email, phone number, username or name. Relevant only when building a product
  on Exa, not for this user's own research.
- `stream: true` returns server-sent events only when `outputSchema` is set.

The `sweep` subcommand of the bundled script runs this whole pass as one
command — category rotation, `additionalQueries`, Exa-written summaries,
deduplication by URL — and writes `longlist.md` and `longlist.json` plus a cost
tally, so raw results never enter the context window. Measured 2026-09-02: three
categories × 15 results, 44 unique rows, $0.081, matching the list-price model
exactly ($0.007 base + $0.001 per result past ten + $0.001 per summary). When
egress to `api.exa.ai` is closed, the `searcher` agent does the same job through
the MCP tool.

Use `startPublishedDate` / `endPublishedDate` for *recency of publication*.
`startCrawlDate` and `endCrawlDate` are marked "Deprecated and has no effect;
ignored by the API" in Exa's OpenAPI spec — a window built on them silently
does not filter. For *freshness of a page that changes* use
`contents.maxAgeHours` (0 = live fetch), never a published-date filter; and do
not send `livecrawl` alongside it.

## Read — `web_fetch_exa`

Raw markdown of a page. Batch every URL into one call with a generous
`maxCharacters`. Prefer it to `WebFetch`, which returns a small model's summary
rather than the page: a four-row price table came back as "$1-3 per million
tokens" with the $15 row silently dropped.

## Enumerate — `agent_run`

Builds lists, never establishes facts — it returns a synthesis, and verification
needs sources read directly. Shallow `outputSchema` (depth 2, ~10 properties),
one source field per row, no citation or confidence fields — grounding comes back
separately, with per-field confidence. `input.exclusion` stops it re-returning
what you already have; `input.data` enriches rows you hold. Keep the `runId`;
resume with it rather than starting a duplicate, and pass a finished run as
`previousRunId` to extend it (the follow-up gets its own new ID).

**Effort ladder** (exa.ai/docs/agent/quickstart and /agent/agent-ultra, read
2026-10-28). The MCP tool's `effort` accepts `minimal | low | medium | high |
xhigh | ultra | auto`; the tool defaults to `low`, the REST API to `auto`.

| Effort | Price | Use |
| --- | --- | --- |
| `minimal` | $0.012 / request | trivial enrichment |
| `low` | $0.025 / request | default list-building |
| `medium` | $0.10 / request | a thin `low` run |
| `high` | $0.50 / request | |
| `xhigh` | $1.00 / request | |
| `auto` | metered, default cap $5 | unknown difficulty |
| `ultra` | metered, default cap $20 | see below |

Other agent pricing: 1 ACU = $0.10; $0.005 per search call; $0.02 per email
enrichment; $0.07 per phone enrichment. Fixed efforts reject a `budget`.

**Agent Ultra** — `effort: "ultra"`. The highest-effort mode: it "runs longer
and spends more compute than any other effort" for the most complete result.
There is no separate model ID; it is an effort value on the same
`POST /agent/runs` (REST), `agent_run` (MCP), `exa.agent.runs.create(...,
effort="ultra")` (SDKs) or `reasoning.effort: "ultra"` on the Responses API
(with `stream: true` or `background: true`).

- *Use for:* large list-building, deep multi-source research, criteria that are
  hard to verify, where completeness matters more than latency or cost.
  *Not for:* anything needing a predictable price or a quick answer — use a
  fixed effort.
- *Budget:* `budget.maxCostDollars` $1–$100 (default $20; also works with
  `auto`, default $5); `budget.maxDurationSeconds` 300–10,800 (Ultra only, no
  default). Near either limit the agent stops starting new work and returns what
  it has. Metered at standard Agent rates; early finishes cost less.
- *Latency:* typically ~30 minutes, up to 3 hours. SDK polling helpers time out
  after one hour by default, so pass a longer timeout or stream events. Over MCP,
  `agent_run` returns a run ID while the run is still going: resume with `runId`
  rather than starting a duplicate.
- *Stopping:* `POST /agent/runs/{run_id}/stop` ends the run and keeps partial
  results (`stopReason: "stopped"`; billed to the stop).
- *Stop reasons that still return results:* `schema_satisfied`,
  `budget_reached`, `time_limit_reached`, `iteration_limit_reached`,
  `token_limit_reached`, `stopped`. Not completed: `error`, `cancelled`. The
  quickstart page lists none of these, so treat the Ultra page as the source and
  expect it to move.
- *Statuses:* `queued`, `running`, `completed`, `failed`, `cancelled`. A
  completed run carries `output.text`, `output.structured`, `output.grounding`
  (authoritative over streamed source previews), `costDollars` and
  `usage.agentComputeUnits`.

**Standing approval (user, 2026-10-28):** Ultra is pre-approved whenever
judgement says the extra completeness is worth it. Do not ask first. Say in one
line that Ultra is running, why, and the cap chosen. Pick the cap by judgement:
$20 (default) for a typical exhaustive list; up to $100 when the universe is
large or multi-segment and a thin result would mislead. Bound arrays with
`maxItems` so contact-enrichment cost stays predictable.

**Verification schemas** (quickstart, 2026-10-28): make fields that may not be
verifiable nullable and leave them out of `required`, so the agent returns
`null` rather than inventing a value. Separate a failed inspection from
negative evidence with an enum such as `present | absent | cannot_verify` — an
unreachable site is not evidence that a page does not exist.

## Reason in one call — Deep Search

`type: deep-lite | deep | deep-reasoning` on the ordinary `/search` request
(docs: exa.ai/docs/search/deep-search; spec: exa.ai/docs/reference/search —
both read 2026-10-06). Exa plans the search from `query`, expands it, runs
several searches, inspects the evidence, issues targeted follow-ups where it is
incomplete or contradictory, then selects pages and synthesises.

| Type | Base price | Latency (Exa's figures) | Use |
| --- | --- | --- | --- |
| `deep-lite` | $12/1k | ~4 s | lightweight expansion and synthesis |
| `deep` | $12/1k | 4–15 s | iterative research, several structured items |
| `deep-reasoning` | $15/1k | 12–40 s | **Legacy** per exa.ai/docs/search/deep-search (read 2026-10-28), which recommends `deep` for research workflows. Earlier reads (2026-10-06) described it as the type for conflicting evidence; the later page wins. Use `deep` first; reach for this only if `deep` returns thin on conflicting evidence, and say so. For long list-building Exa points to Agent instead |

Extra results past 10 and page summaries bill as on an ordinary search.

The parameters that make it more than a slower search:

- `additionalQueries` — up to 10, *Deep types only*. Each should be a different
  search direction; minor rephrasings add volume, not coverage.
- `systemPrompt` — behaviour: source preferences, novelty, deduplication. Not
  the shape of the output.
- `outputSchema` — shape, and the trigger for synthesis. Root `text` (prose)
  or `object`. Limits, enforced with a 400 before the search runs: at most 10
  properties counted across every level (array `items` properties count), at
  most 2 levels of nested objects below the root, every array declares
  `items`. Need more fields → several focused Deep calls, or Agent. The spec
  says `outputSchema` works on *every* search type (adds ~2 s), but only Deep
  types do the iterative research before synthesising.
- `contents.highlights: true` — the evidence snippets Deep actually used.
- `numResults` — bounds pages returned, not searches performed.
- `stream: true` — SSE, only with `outputSchema`; the script does not use it.
- All standard filters (`includeDomains`, `excludeDomains`, published-date
  pair, `category`, `userLocation`, `moderation`) sit on the same request and
  were accepted alongside `type: deep-lite` in a live call on 2026-10-06.

When Deep beats an ordinary search (Exa, 2026-10-28): difficult searches,
synthesis across many results, or structured output with three or more fields
one search cannot fill; Deep is the default when `outputSchema` is used. Stay
with `auto` (or `lite`) when you only need ranked pages, the query targets a
specific source, your own code does the reasoning, or the path is interactive,
autocomplete or voice.

The response has `results` (selected pages) and, with a schema, `output.content`
plus `output.grounding`: one entry per field with `citations` and a `confidence`
of `low | medium | high`. The synthesis is a draft to verify, not a source;
grounding tells you where to look.

The script's `deep` subcommand carries all of this (`--alt`, `--system`,
`--text`/`--schema` with a local limits check, `--highlights`, filters, `--out`)
and renders synthesis, grounding and selected pages as Markdown. Measured
2026-10-06: `deep-lite`, two directions, text schema, five pages, 4.9 s.

## Watch — Monitors

Recurring searches with semantic deduplication across runs, so each run surfaces
only what is new. A run that returns nothing is a real answer: "nothing new since
the last run", never an empty section.

Three constraints the API imposes: a webhook URL is mandatory even though runs
are readable over the API (Exa rejects `example.com`, localhost, `.local` and
private IPs, so the placeholder must be a real public host); `trigger` is
optional, so a monitor can be manual-only and cost nothing until triggered;
minimum interval is one hour, anchored to creation time. Whether Exa disables a
monitor whose deliveries keep failing is **unverified** — if a scheduled monitor
goes quiet, check that first.

## Reach past the open web — Connect providers

Attached per run via `dataSources: [{ "provider": "<id>" }]` on `agent_run`
(`data_sources` in the Python SDK), up to five (Exa raises the limit on request
via sales@exa.ai; the MCP tool enforces `maxItems: 5`). Attaching makes a
provider *available*; it does not force a call. Nothing to install. The agent
calls a provider's tools only when it is attached, and chooses per step between
the provider and web search; a schema field that asks for a provider-specific
metric ("monthly visits", "total funding") triggers the matching tool. Put the
metric in the query *and* the schema, and name the source in the field
`description` ("from Similarweb"). Connect charges add to the standard run
price. Zero Data Retention teams can attach only ZDR-eligible providers; any
other returns a 400 naming it. This account is not known to be ZDR.

| Provider | Pricing (read 2026-10-28, exa.ai/docs/agent/connect/overview) | ZDR |
| --- | --- | --- |
| `fiber` | $0.02 per credit | yes |
| `similarweb` | $0.30 per credit | no |
| `baselayer` | $0.10–$4.00 per order; follow-up reads of a prior search free | yes |
| `polymarket` | free | no |
| `macrobond` | free | yes |
| `affiliate` | $0.015 per call | no |
| `particle` | $0.015 per call | no |
| `financial_datasets` | $0.01 per call | no |
| `jinko` | $0.005 per call | yes |

Fiber and Similarweb bill the credits the provider reports; a call with no
match or no data is free. Similarweb runs 1–15 credits a call, so $0.30–$4.50.
Baselayer by operation: KYB business search $1.00; UCC lien search $2.00 per
state; litigation/bankruptcy docket $1.00 per category; watchlist screening
$0.10–$0.25 per list; industry classification or website analysis $0.35 each;
international business search $4.00; follow-up reads of a prior business search
free. Other providers (Exa's example names `harmonic`) exist on request through
Exa's team.

**`particle` — podcast transcripts.** 100,000+ shows, transcribed, diarized and
speaker-attributed within minutes of airing, returned as timestamped transcript
windows. The only practical way to get what a specific person actually said in
their own words, at length, unedited by a marketing page. Use it to hear a
practitioner before engaging them; also for expert commentary, quotable
soundbites, and tracking how a narrative is moving.

**`financial_datasets` — US public-company data.** Prices, fundamentals,
earnings, SEC filings, ownership and stock screening for 27,000+ US tickers,
plus ticker news (Connect overview, read 2026-10-28; earlier notes called it
"ticker news" only). Ties a claim about a listed company to its filings and
reported numbers rather than to coverage of them.

**`macrobond` — macroeconomic and financial time series** from central banks
and statistical offices worldwide: series search, observations (up to 2,000),
frequency- and currency-aligned comparisons, and release calendars. No per-call
provider charge (docs, read 2026-10-07). The right source for a GDP, CPI,
policy-rate or fiscal series behind an infrastructure or policy argument;
series are named by Macrobond entity (`usgdp`), not URL, so quote the entity
and the source metadata the agent returns.

**`polymarket` — prediction-market data.** Market-implied odds, price history,
order-book depth and position holders. Read-only and free; you pay only for the
agent run. Use it for the crowd's implied probability of a *dated, resolvable*
event and how it has moved. Liquidity and spread say how much weight the number
deserves — a thin market is an opinion, not a signal.

Providers compose: Polymarket plus Particle explains a move in the odds with the
commentary behind it; Polymarket plus Financial Datasets ties implied odds to the
underlying numbers.

The remaining five are situational. Name the provider-specific data in both the
query and the schema, or the agent falls back to web search.

- **`similarweb` — modelled web traffic.** Traffic and rank, similar sites,
  traffic sources, top referrers/countries/pages/keywords, keyword overview,
  audience demographics and overlap, technologies, top sites by category. Cost
  scales with rows × months (about one credit per metric × row × month; e.g.
  traffic sources 10 credits, demographics 8, technologies 10), so keep result
  counts and months small. The figures are **modelled estimates**, not
  measurements: say so wherever one is quoted, and treat a competitor ranking
  as a lead to check.
- **`fiber` — B2B company and people data.** 40M+ companies, 850M+ people, 30M+
  jobs: company, people and LinkedIn profile search; LinkedIn signals (job
  changes, promotions, headcount, fundraising); posts from LinkedIn, X,
  Instagram, TikTok, Reddit, YouTube; work/personal email and phone reveal.
  Search costs 2 credits + 1 per result; company lookup ~2 per candidate;
  person lookup 2; contact reveal 2 (work email) to 5 (phone). A lookup's
  `numResults` sets how many candidates you pay for. **Contact reveal returns
  personal data about named individuals**: do not run it without the user's
  say-so on the specific purpose, and never into a client deliverable without
  asking.
- **`baselayer` — US business verification.** Registration, officers, risk
  signals. Rate varies by operation.
- **`affiliate` — product catalogue search** across merchants and affiliate
  networks: live pricing, brands, direct merchant links (product search and
  price comparison). The links are **affiliate links**: say so, and do not hand
  them over as neutral recommendations. The docs state no limits.
- **`jinko` — flight and hotel search.**

Documented pairings: Polymarket + Particle (the commentary behind a move in the
odds) and Polymarket + Financial Datasets; Particle + Financial Datasets
(cross-check a podcast claim against reporting); Particle + Fiber (context on
people discussed); Fiber + Similarweb (competitors into company records);
Fiber + Baselayer (officers and registration).

## Not available — Websets

`GET /websets/v0/websets` returns 401: "Your team does not have access to the
API. Upgrade to a Pro plan to get access." Subscription-priced — Starter
$49/month, Pro $449/month (websets.exa.ai/billing, read 2026-09-02). Do not build
a Websets flow without re-checking the plan, and never present the upgrade as a
small step. `agent_run` covers much of the same list-building ground at $0.025.
