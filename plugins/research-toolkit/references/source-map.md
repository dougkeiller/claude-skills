# Source map — which source for which question

Exa is the default engine, and its index now holds many record types that used
to need a connector — filings, trials, approvals, case law, contracts, census
tables, local businesses, transcripts; `data-index.md` maps them to question
types. Everything else here is reached for when the question is *theirs*, and
always alongside Exa rather than instead of it. Check the tool list before
planning: connectors come and go, and a source that is not loaded in this
session is not a source.

| The question is about | Reach for | Why it beats a web search |
| --- | --- | --- |
| Anything on the open web | Exa advanced search — see `exa-surface.md` | Semantic index; category rotation; personal sites and first-hand accounts |
| A question one search cannot settle — a comparison or researched conclusion | Deep Search via the script (`deep`) | Plans and iterates its own searches, returns a grounded synthesis with per-field confidence; still verified on the page |
| The same, second opinion | `WebSearch` | A different index. Use alongside on any sweep where coverage matters; never instead |
| Clinical or life-science literature | Elicit (`search_papers`, `search_trials`, systematic reviews), PubMed (`search_articles`, full text) | Structured metadata, trial registries, peer-reviewed full text. Exa's `publication` category and its trial/approval coverage are the fast first pass; these are the system of record |
| Biology preprints | bioRxiv (`search_preprints` — by date and category only, no keyword search) | The preprint server itself; not peer-reviewed, say so |
| CS, maths, physics, stats, quant finance preprints | alphaXiv (`discover_papers`, `get_paper_content`, researcher lookup) | Full-text arXiv access; who works on what; papers by a named researcher |
| What the user has already read or saved | Readwise (`reader_search_documents`, `readwise_search_highlights`) | Their own library. Check it first on any topic they have worked before — it is the cheapest source and the only one with their annotations |
| The user's own files | Google Drive (`search_files`, `read_file_content`) | Prior deliverables, client material, notes not in Readwise |
| A computation, unit conversion, dated fact, or dataset lookup | Wolfram (`WolframAlpha`) | Computes rather than retrieves; right for "how much", "convert", "on what date" |
| A macroeconomic or financial time series (GDP, CPI, policy rates, fiscal) by country | `agent_run` with `dataSources: [{provider: "macrobond"}]` | Central-bank and statistical-office series with source, units, frequency and release calendar; no per-call provider charge. Exa's web index has the *releases*; Macrobond has the *series* |
| Case law, statutes, government contracts, census tables | Exa general index (see `data-index.md`) | Primary records with full text and metadata; no separate connector exists for these |
| US Medicare coverage — what Part B pays for | CMS Coverage (`search_national_coverage`, `search_local_coverage`) | The coverage database itself; NCDs and LCDs as written |
| A US healthcare provider's identity, specialty, location | NPI Registry (`npi_lookup`, `npi_search`) | The federal registry; validates before you trust a directory |
| A page that blocks crawlers, needs a login, or renders client-side | Claude in Chrome (preferred) or the built-in browser | Reads what the crawler cannot. Ask before acting on a site that needs the user's login |
| Podcast transcripts — what a person actually said | `agent_run` with `dataSources: [{provider: "particle"}]` | Speaker-attributed, timestamped; not on the open web |
| A US public company's prices, fundamentals, earnings, filings, ownership, or a stock screen | `agent_run` with `financial_datasets` | 27,000+ US tickers; ties a claim to reported numbers rather than coverage of them |
| Web traffic, competitors of a domain, B2B company/people data, US business verification, product prices | `agent_run` with `similarweb`, `fiber`, `baselayer` or `affiliate` | Partner databases; see `exa-surface.md` for what each holds, its billing and its caveats (Similarweb figures are modelled; Affiliate links are affiliate links; Fiber contact reveal is personal data) |
| An exhaustive list where a missed entrant is the costly error | `agent_run` with `effort: "ultra"` | Pre-approved; highest-effort Agent, up to 3 h; see the research skill |
| The crowd's implied odds on a dated, resolvable event | `agent_run` with `polymarket` | A market price; report it as one — see the research skill's rule |
| Anything recurring — a watchlist, a weekly digest | Exa Monitors via the script, or a Cowork scheduled task | Runs without a session open |

## Rules that apply across sources

- **Check the user's own library before the web** when the topic is one they
  have worked before. Readwise and Drive are free and carry their judgement.
- **Say which source a figure came from**, in line, every time. A number from a
  connector that summarises (Elicit reports, `WebFetch`) is not a number read
  from the page.
- **Domain sources do not replace Exa's personal-site pass.** A clinical
  question still benefits from a practitioner's blog; a CS question still
  benefits from the engineer who tried it in production.
- **Absence is a finding.** If a domain source returns nothing on a topic it
  should cover, report that rather than filling the gap from the web.
