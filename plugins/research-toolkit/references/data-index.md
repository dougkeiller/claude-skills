# What Exa indexes — and the query shape each source wants

Exa searches more than web pages. Its index includes structured and semi-private
sources that used to need a separate connector or a detour, all reached through
the same `/search` call. Read from exa.ai/docs/search/data/* on 2026-10-07; the
pages say these are "common data patterns" and that the broader web is also
searched, so treat the lists as what Exa *vouches* for, not the boundary.

Two rules from Exa's own guides that hold across every source: name the entity
and the traits that qualify it, and ask for the **source type** when it matters
("earnings call transcript", "professional profile", "court opinion",
"vendor pricing page"). The query describes the page; `objective` says what the
task needs from it.

## Mapped to the questions this user asks

| Question type (workstream) | Exa holds | Query shape | Category / tool | Still pair with |
| --- | --- | --- | --- | --- |
| Market map of vendors or startups (a venture's competitors, a PE portfolio, an EdTech market) | Company pages with description, stage, funding; job postings; pricing pages | "companies selling <product> to <customer> in <geo>" — describe what they do, not a name list | `company` for the entity pass; general index for operating signals | Personal-site pass for first-hand accounts |
| Who runs it, who buys it, who to talk to | Professional profiles by role, skill, location; people qualified by company traits | "professional profiles of <role> at <company traits>" — one query carries the relationship | `people` | Team pages, "joined" announcements, speaker lists |
| Operating signals on a company (hiring, pricing, launches) | Job postings, pricing and docs pages, trade press | "<signal> at <company traits>" e.g. "remote staff engineer roles at Series B fintech" | general | Monitors for the standing version |
| Funding and deal flow (PE or VC work) | Announced rounds, investor pages | "<round> rounds in <sector> announced <window>"; "investors who led seed rounds in <sector> in the last year" | general + published-date pair | `financial_datasets` via agent for listed names |
| Public-company facts (portfolio comps, listed competitors) | Quotes and price history; earnings-call transcripts with speaker attribution; SEC and international filings; analyst estimates | "<company> <quarter> earnings call transcript" gets the transcript, not coverage; "10-K risk factors that mention <topic>" | `financial report` keeps results to filings and reports | `financial_datasets` via agent for structured numbers |
| Economic and policy data (development finance, op-eds) | Published economic releases and government statistics; census and public statistical records | "most recent <release> and <figure>"; "census tract <measure> in <geo>" | general | `macrobond` via agent for a clean time series; Wolfram for a computation |
| Procurement and public-sector market (PPPs, infrastructure) | Government contracts and procurement records; statutes, regulations, agency guidance | "federal contracts awarded for <service> <window>"; "<agency> guidance on <topic>" | general | The agency's own portal via browser when the record is behind a form |
| Legal position (contracts, timeshare, policy) | US court opinions with full text, court, docket, citation; statutes | "<jurisdiction> appellate decisions on <legal question>" in plain language, not a citation | general | A lawyer; this is research, not advice |
| Clinical and health evidence (a health venture, a genomics idea, senior living) | Papers and preprints with full-text chunks; clinical trials, drug labels, interactions; FDA and other regulatory approvals | "phase 3 trials of <intervention> in <population>"; "FDA approvals for <device class>"; "papers on <method or finding>" | `publication` for papers; general for trials and approvals | Elicit and PubMed remain primary for systematic work; Exa is the fast first pass and the practitioner-blog complement |
| Patents and prior art | Granted US patents with claims, inventors, assignees | Describe the invention functionally, "the way a claim would" — never a product name | general | — |
| Local market (eldercare in one city, senior living, a venture's GTM) | Local business profiles with address, hours, amenities, reviews; venues; property records; zoning decisions and permits | "<category> in <neighbourhood> with <attribute>", asked like a local; "<record type> approved in <city>" | general, `userLocation` set | Browser for a directory that blocks crawlers |
| What a person actually said (vetting an expert, a founder) | Podcast and video transcripts; interviews | "podcast episodes where <role> discuss <topic>" — name the format | general | `particle` via agent for speaker-attributed, timestamped transcript windows |
| Practitioner reality vs vendor story | Engineering and practitioner blogs; first-hand accounts | "engineering blog posts about <doing X>" — name the source type | `personal site` | — |
| Reputation and adverse signals (due diligence) | Adverse media; regulatory complaints; sanctions lists and watchlists | "negative press and regulatory complaints about <entity class>" — describe the signal and the class, not "<name> news" | general + `news` | `baselayer` via agent for US business verification and officers |
| Agent tooling and open-source skills (impact-agents research) | GitHub repos; API and developer docs; package registries with version detail; agent-skills directories | "agent skills for <task>" — state the artifact type and the task; "breaking changes in <package> <version>" | `github` for repos; general for skills directories | Hugging Face connector for models and datasets |
| What has been reported this week | News from major, trade and niche outlets, searchable within minutes of publication | "news coverage of <topic> published this month" with the published-date pair as the hard bound | `news` | WebSearch as the second index |

## The three guides in detail

Read 2026-10-28 from exa.ai/docs/search/data/overview and its three linked
guides (`research.md`, `news.md`, `companies-people.md`). **The guides do not
list category values, filter parameters or restrictions** — only example
queries; they defer to the OpenAPI spec (exa.ai/docs/exa-spec.yaml). The
`research` guide shows `category: "publication"`; the other category names and
the 400 behaviour of `company`/`people` come from the MCP tool schema and the
earlier live checks in `exa-surface.md`, not from these pages.

**Research publications** — `category: "publication"` limits to papers.
Indexed: papers and preprints (full-text chunks where parsed), patents
(abstracts, claims, inventors, assignees), grants and funding announcements,
clinical trials, drug labels and interaction data, regulatory and health
approvals; records carry titles, abstracts, authors, venues, citations,
publisher and repository pages.
- Papers: describe the method or finding, not guessed title keywords —
  "papers on evaluation benchmarks for retrieval-augmented generation".
- Clinical evidence: name the phase, intervention and population — "phase 3
  trials of GLP-1 agonists in adolescent patients".
- Regulatory: name the regulator and the device or drug class.
- Prior art: describe the invention functionally, the way a claim would.
- Trials, labels and approvals are *not* papers: run those without
  `category: "publication"`, or the category filter excludes them. This is an
  inference from the guide's wording ("limits results to papers"), not a
  documented rule — check the first result set.
- Multi-source structured output: Exa Agent, not a longer search.

**News** — reporting from major, trade and niche outlets, searchable within
minutes of publication; also blog posts and listicles, podcast and video
transcripts, adverse media.
- Name topic, source type and publication window: "news coverage of the EU AI
  Act enforcement timeline published this month". Add the published-date pair
  only when the window is a hard requirement.
- Name the source type for practitioner analysis ("engineering blog posts about
  migrating from Postgres to ClickHouse"); name format and subject for
  discussions ("podcast episodes where …").
- Adverse media: describe the signal and the entity class, not "<name> news".
- Newer publications use the time window in the query or the published-date
  pair; `maxAgeHours` is for pages that change, not for recency.

**Companies and people** — company pages, professional profiles, job
postings, pricing pages, product docs, personal websites, public talks,
interviews and articles. Use cases: company, candidate and expert discovery;
account research; market maps and deal sourcing; leadership and hiring research.
- Companies: describe what they do ("companies selling AI voice agents to
  dental practices"); name operating signals ("remote staff engineer roles at
  Series B fintech companies"); name funding ("investors who led seed rounds in
  robotics in the last year").
- People: combine role, seniority, location, skills and source type
  ("professional profiles of senior ML engineers in Seattle with PyTorch
  experience"); qualify by company traits; ask explicitly for personal websites
  or public work.
- Combined: put the relationship in one query — "heads of security at Series B
  healthcare software companies that sell to hospitals".
- The `company` and `people` categories run on semantic-only indices that
  reject domain and date filters (see `exa-surface.md`); the free-text query
  carries the qualification instead.
- People results are named individuals. Say what a profile is and where it came
  from; do not infer anything the page does not say.

## Three habits the guides repeat

**Ask for the relationship in one query.** "Heads of security at Series B
healthcare software companies that sell to hospitals" returns company pages,
profiles and hiring pages together. Building a company list first and then
searching people is slower and loses the qualification.

**Name the primary record, not coverage of it.** "Tyson Foods Q4 FY2025 earnings
call transcript" returns the transcript; "Tyson earnings" returns articles
about it. The same holds for filings, court opinions, trial registrations and
approvals — say the record type.

**Describe the signal and the class for adverse or diligence searches.**
"<name> news" returns PR. "Negative press and regulatory complaints about
<entity class>" returns what a diligence pass needs, and then the name narrows
it.

## Where this changes the source map

Sources that used to be reached only through a domain connector now have an Exa
first pass: clinical trials and regulatory approvals (alongside Elicit and
PubMed), case law and government contracts (no connector existed), census and
economic releases (alongside Wolfram), podcast transcripts (alongside Particle),
local business profiles (alongside the browser). The connector still wins where
it is the system of record or returns structure Exa does not — Elicit for a
systematic review, NPI for a provider's identity, Macrobond for a time series —
and `source-map.md` says which. Run Exa first for breadth, the connector for
the record.
