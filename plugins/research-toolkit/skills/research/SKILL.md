---
name: research
description: The single entry point for research. Invoke for ANY request to research, investigate, survey, compare, shortlist, or find options — "research this", "deep dive on", "find everything about", "who are the players", "what are my options", "what is out there" — and for standing watchlists ("monitor this", "track announcements about", "what's new since last time"), Deep Search, and structured list-building with Exa Agent (including Agent Ultra for exhaustive runs) and its Connect data providers (Particle podcast transcripts, Financial Datasets, Polymarket, Similarweb, Fiber, Affiliate.com, Macrobond, Baselayer, Jinko). Also invoke before any recommendation that turns on costs, deadlines, eligibility or financials. Picks one of six modes, enforces the human stops between the long-list, the scored cut and verification, and writes the dated note. Exa is the engine; other connectors are pulled in by the source map. Never invoke the vendor skills exa:search or exa:exa-agent — this skill owns dispatch.
---

# Research

<!-- Prices are written "USD 0.012" not with a dollar sign followed by a digit: the skill loader treats that pattern as a positional-argument placeholder and substitutes words from the invocation. -->

One skill, six modes. Exa does the searching; this skill decides the shape,
keeps the human in the loop where it matters, and writes the note. The method
is wide before deep, and finalists are never picked by eye: long-list → the
user sets criteria and weights → every candidate is scored and the scoring
shown → the user approves the cut → verification on the survivors only.
Detail lives in the references — read the one the mode needs rather than
reconstructing it:

- `${CLAUDE_PLUGIN_ROOT}/references/exa-surface.md` — the Exa map by job, prices, filters, Connect providers, what is unavailable
- `${CLAUDE_PLUGIN_ROOT}/references/data-index.md` — what Exa indexes beyond web pages, mapped to the user's question types, with the query shape each wants
- `${CLAUDE_PLUGIN_ROOT}/references/source-map.md` — which non-Exa source for which question
- `${CLAUDE_PLUGIN_ROOT}/references/query-patterns.md` — how to phrase queries; people, companies, papers, news, relationships, source quality
- `${CLAUDE_PLUGIN_ROOT}/references/output-template.md` — the dated note

The script: `S="${CLAUDE_PLUGIN_ROOT}/scripts/exa_extras.py"`. It carries its
own credential — never ask for an API key, never print it.

## Before anything

1. **Dates.** If the request involves time, compute the exact bounds from
   today's date in the environment and write them down. Never reuse a date from
   an example.
2. **Tools.** The method needs `web_search_advanced_exa` and `web_fetch_exa`.
   The Exa tools are usually *deferred*: they appear by name only and must be
   loaded before the first call, in one go. Their prefix depends on the host:
   `mcp__Exa__` in Cowork (this plugin's own server), but in the Claude Code
   desktop app the plugin's server has an empty URL and the working tools come
   from the claude.ai Exa connector under a UUID prefix (seen 2026-10-28:
   `mcp__ae62a597-c1b5-4fd7-a90b-ef15232199e7__`). Find them by name rather
   than assuming a prefix — `ToolSearch` with `web_search_advanced_exa` —
   then `select:` all three (`web_search_advanced_exa`, `web_fetch_exa`,
   `agent_run`) under the prefix that came back. Say so if they are absent. Note which domain
   connectors from the source map are actually loaded (many are deferred too).
3. **Egress.** `deep`, `sweep` and `monitor-*` call `api.exa.ai` directly.
   Cowork cloud sessions on this account have reached it (checked 2026-10-06),
   but the setting is the organisation's and can change: a connection error
   rather than an HTTP status means it is closed — say so and use the MCP path
   instead of retrying.
4. **The user's own library first** when the topic is one they have worked
   before: Readwise, then Drive. Free, and it carries their judgement.

## Pick the mode

| Signal in the request | Mode |
| --- | --- |
| A fact, one named entity, "what does this page say" | **Lookup** |
| A landscape — options, players, "find me all", "what's out there", a comparison not yet scoped | **Sweep** |
| "Verify these", "go deep on", named finalists from an earlier long-list | **Verify** |
| "Build me a list of every…", enrichment of rows the user holds, anything needing Particle, Financial Datasets or Polymarket | **Enumerate** |
| A question one retrieval pass cannot settle — a comparison, a researched conclusion, several structured items each with its own requirements, conflicting evidence to weigh | **Deep** |
| "Monitor", "watch", "track", "what's new since", "set up a standing search" | **Watch** |

Tell the user which mode you picked, in one line. Do not estimate or report
what searches, fetches, sweeps, Deep Search or agent runs cost — the user's
standing rule is that connector-class calls are cheap and the figure is noise.
The two exceptions, where money recurs or a plan upgrade is implied, are a
scheduled monitor (Watch) and Websets; state those prices before acting. An
Agent Ultra run is pre-approved: announce its cap in one line, don't ask. When
a request could be a Lookup or a Sweep, prefer Sweep if the answer would be a
*choice* — a confident answer about the wrong three options is the failure
this skill exists to prevent. Ask only when the reading is genuinely open.

## How to ask Exa — every mode

Exa's own guidance (exa.ai/docs/search/best-practices, read 2026-10-07),
reduced to what matters for ad hoc research:

- **Start small: a natural-language query plus highlights.** Describe the
  page wanted — subject, source type, period — not a bag of keywords. Ask for
  highlights rather than page text; Exa sizes them to relevance and they carry
  the evidence at a fraction of the tokens. One content view per call.
- **Give the objective.** `objective` is the task the search serves: what
  should rank first, what to exclude, which facts to pull. Pass it on every
  script sweep and Deep call; it is how a source *preference* reaches Exa. The
  MCP search tool has no `objective` field, so on MCP calls (and in the
  searcher agent) the preference goes into the query wording.
- **Hard filters only when a violating result is unusable.** Domain and date
  filters are for "must come from" and "must be after"; a preference for a kind
  of source belongs in the query or the objective, never in an allowlist.
  `includeText` / `excludeText` are deprecated — put the terms in the query.
- **Read the response in layers before changing the request**: title and URL
  for the kind of source, published date for recency, highlight for the
  evidence. Then change one thing at a time; a different search type cannot
  repair an underspecified query.
- **Recency vs freshness are different controls.** Newer *publications*: a
  time window in the query or the published-date pair. A page that *changes*
  (prices, staffing): `maxAgeHours`. Not the other way round.
- **Search `type`: `auto` by default; `lite` only for cached, low-latency
  paths.** `lite` rejects `maxAgeHours` and most advanced parameters, so never
  use it for volatile facts. `fast` and `instant` are legacy. Change the type
  last.
- **Pass `notices` on, keep `warnings` out.** A `RESTRICTIONS_RELAXED` notice
  means a quoted phrase or `site:` operator was dropped because nothing matched:
  the results are looser than the query said. `warnings` are request bugs to
  fix, not material for analysis.
- **Name the primary record and the source type**: papers by method or finding,
  trials by phase + intervention + population, regulators by body + product
  class, prior art described the way a claim would be, adverse media by signal +
  entity class, people by role + company traits in one query.
- **Know what the index holds.** Exa indexes more than web pages — filings and
  earnings transcripts, papers, patents, clinical trials, court opinions,
  government contracts, census tables, local business profiles, podcast
  transcripts. `references/data-index.md` maps the user's question types to
  these and gives the query shape each one wants. Check it when planning a
  sweep; a source that Exa indexes natively needs no detour.

## Lookup

One or two `web_search_advanced_exa` calls with highlights, or a
`web_fetch_exa` of the page. Answer directly with the source. State how the
figure was read. No note unless the user asks.

## Sweep — Pass 1, wide

Goal: an enumerated long-list that maps the space. Breadth, not depth. Verify
nothing; fetch nothing; one line per candidate.

Restate the question in one line and state the inclusion criteria. If they are
ambiguous, take the reading that keeps the net widest and say so.

**Run the sweep script first.** One command does the category rotation, the
alternate phrasings, the Exa-written annotations and the deduplication, and
writes the long-list to a file so raw results never enter this context:

```bash
python3 "$S" sweep "description of the ideal page for this question" \
  --categories "general,company,people,personal site" --num 25 \
  --objective "long-list of <X> for <purpose>; rank <source kind> first, exclude <kind>, pull <fact>" \
  --alt "a sceptic's angle" --alt "a buyer's angle" \
  --since YYYY-MM-DD --out <session output dir>/<topic>-longlist
```

Point `--out` at a path that survives the session (in Cowork cloud,
`/mnt/user-data/outputs/`); a relative `research/` path lands in the
container and is lost when it is reclaimed.

Each `--alt` is its own call per category (Exa's `additionalQueries` works
only on Deep types), so make each one a different *angle*, not a synonym. The
script asks for capped highlights plus an Exa summary per row. Choose
categories for the question: `company` for firms, `people` for individual
practitioners who often have no company site, `personal site` for first-hand
accounts and expected losers, `publication`, `news`, `financial report` when
the subject is theirs — and consult `data-index.md` for what else the index
holds natively. `company` and `people` reject domain and date filters (the
script strips them; on the MCP tool they fail with a 400). Add
`--exclude-domains` only for sites whose results would be unusable (listicle
farms), not for sites you merely rank lower — that preference goes in the
objective. Read the `.md` it writes, not the JSON.

**If the script cannot run** (egress closed), spawn one `searcher` agent per
category in a single message, each with the question, the criteria, the
category, two or three phrasings, and the exclusions. They return rows and
`sources_reviewed`; compile from those. Never run bulk searches in this
context yourself.

**Widen beyond Exa.** Run `WebSearch` on the same question as a second index.
Add domain sources from the source map when the subject is theirs. Report
absence from a source that should have had coverage.

**Compile.** Deduplicate by URL, then by entity. Check coverage: missing
segments, geographies, entity types; obvious names absent. A follow-up on one
gap is a single searcher or one more script call, not a new sweep. Aim for
genuine coverage including expected losers — a long-list of plausible winners
is a shortlist wearing a disguise.

**Deliver** a numbered list: name, one line on what it is, one line on why it
might qualify, source link, quality note. The quality note is an observation,
not a grade — "vendor's own site", "app-store listing", "personal blog,
first-hand", "press release", "roundup, links to others" — written from the
URL and the Exa summary for script rows, and taken from the searcher's
`quality` field for agent rows. Say when it rests on the summary alone. Then
what was excluded and on what grounds.

**Stop here — first stop.** Do not ask the user to pick entries by eye. Ask
for the criteria that matter and their weights; propose a starting set drawn
from the question (fit to the stated need, evidence of real use, cost or
pricing model, maturity, geography, anything the request named) only as a
draft for them to edit. If nobody is there to answer, write the long-list
note with the draft criteria in it and end the turn.

## Cut — scoring the long-list

Score **every** candidate on the long-list against the user's criteria and
weights, through `reasoning-toolkit:decision-matrix` — it also runs the
sensitivity test that shows which rankings depend on one weight. Scoring uses
only what Pass 1 produced (the Exa summary, the snippet, the URL, the quality
note); it is a ranking of the evidence so far, not a verification. Where a
row cannot be scored on a criterion, score it unknown and say so rather than
guessing low. Show the full table, the ranking, and the sensitivity result.
Propose a cut line and the reason for it.

**Stop here — second stop.** The user approves the cut or moves it. Only the
rows that survive go to Verify. Never start Verify unattended; if nobody is
there, write the note with the scored table and end the turn.

## Verify — Pass 2, deep

Only the finalists that survived the approved cut. Nothing else.

- **Pin to the primary source.** `includeDomains: ["theirsite.com"]` stops an
  aggregator outranking the thing it summarises. This is the one place a domain
  allowlist is right: in Verify the finalist's own site is a *requirement*, not
  a preference. Entries can carry a path prefix (`theirsite.com/pricing`).
- **Pull the page that holds the number.** `subpages: 3` with
  `subpageTarget: ["pricing", "fees", "about"]` crawls a result's own subpages —
  the fastest route from a homepage to a fee schedule.
- **Force freshness on anything volatile.** `maxAgeHours: 0` always
  live-crawls; prices, deadlines, availability and staffing get 0. A cached
  page is how you confidently quote last year's number. Raise
  `livecrawlTimeout` for slow sites.
- **Bound recency with the published-date pair only.** `startPublishedDate` /
  `endPublishedDate`. The crawl-date parameters are deprecated and ignored by
  the API; a window built on them silently does not filter.
- **Read the raw text.** Batch every finalist URL into one `web_fetch_exa` call
  with a generous `maxCharacters`. Quote each consequential figure as written,
  with the URL beside it. Never paraphrase a number. `WebFetch` returns a small
  model's summary, not the page — a four-row price table once came back as a
  range with the USD 15 row silently dropped.
- **Pages that block crawlers or need a login**: Claude in Chrome, with the
  user's say-so on any site that uses their account.
- **Geo-sensitive facts** take `userLocation`.

Where sources disagree, show both and say which is trusted and why. Never
average, never pick silently. Mark anything unverified as unverified, in the
prose. After Verify, re-run the scoring on the verified facts if any figure
moved a finalist's position — the Cut was scored on summaries, and a verified
number can overturn it. Say which rankings changed and why.

## Enumerate — Exa Agent

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

## Deep — Deep Search

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

## Watch — Monitors

**Before creating a scheduled monitor, state the recurring cost and wait for
a go-ahead** — this is the one place in the toolkit where money recurs without
a session open: about USD 0.015 a run, roughly USD 0.45 a month at daily
(list price read 2026-10-06; assume each run bills). Omit `--period` for a
manual-only monitor that costs nothing until triggered. The script's default
webhook is a no-op URL on the user's own domain; Exa rejects `example.com`,
localhost and private hosts.

```bash
python3 "$S" monitor-create "what to watch for, described richly" \
  --name <slug> --num 15 --period 1d --describe "one line per new development, naming who and what"
python3 "$S" monitor-list
python3 "$S" monitor-run <id>       # trigger now, poll, print what is new
python3 "$S" monitor-delete <id>
```

Each run deduplicates against previous runs, so it surfaces only what is new;
a run that returns nothing is a real answer — "nothing new since <date>",
never an empty section. The API requires a
webhook URL even though runs are readable over the API; the script's placeholder
is a public host where deliveries fail harmlessly. Whether Exa disables a
monitor whose deliveries keep failing is unverified — if a scheduled monitor
goes quiet, check that first. For a digest that runs without a session open,
a Cowork scheduled task can call `monitor-run` and write the note.

## Output

Anything past a Lookup ends in a dated Markdown note in the user's PKM, per
`output-template.md`: conclusion first, finalists, the scored cut, the
long-list kept as an appendix, what could not be verified, what would change
the conclusion, and which sources ran. Never overwrite an existing note —
version it.

## Provenance

For every figure that carries a decision, say how it was read: page text via
fetch, a tool that summarised, or recalled. Quote it as written, with the URL
beside it and an as-of date for anything that moves. An unchecked figure never
sits in a table looking checked. The script still prints `costDollars` to
stderr for debugging; it is not relayed to the user.

## Guardrails

- Research framed as research stays research. Do not upgrade a scoping question
  into a committed recommendation, and do not fill unanswered questions with
  invented premises.
- Report the shape of the evidence. Three sources citing one press release are
  one source. Convergence matters only among independent, high-signal sources.
- Absence of evidence is a finding worth stating, not a gap to paper over.
- After two failed attempts at the same approach, stop and say what was learned.
- Do not invoke `exa:search` or `exa:exa-agent`. They were written for Exa's
  default two-tool install and instruct subagents to avoid the advanced tool;
  this skill and its `searcher` agent replace them.
