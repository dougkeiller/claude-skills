# Query patterns

Adapted from the `search` skill in Exa's own MCP plugin (exa-labs/exa-mcp-server,
MIT License, © 2025 Exa Labs), rewritten for `web_search_advanced_exa` and the
sweep script. The pattern is theirs; the tool choice is ours.

## Writing queries

Describe the page you want, not the fact you want to know. Exa is an embedding
index: it returns pages semantically near your query. Boolean operators are just
words; quotes do not force phrases; one- or two-word queries scatter.

| Looking for | Weak | Strong |
| --- | --- | --- |
| Blog posts about X | "X" | "detailed blog post about X written by a practitioner who uses it daily" |
| A company doing Y | "Y company" | category `company` + "startup building Y for mid-market home-care agencies" |
| A person at a company | "person at Acme" | category `people` + "senior engineer at Acme working on scheduling" |

Vary phrasings by *angle*, not synonym. "Overrated" and "overhyped" land in the
same embedding region; a sceptic's angle, a builder's angle and a buyer's angle
do not. Each angle on an ordinary search is its own call: `additionalQueries`
works only on the Deep types, and Exa says not to spend it on rephrasings
(exa.ai/docs/search/deep-search, read 2026-10-28).

Exa's own order for fixing weak results (best-practices, 2026-10-28): clarify
the query — subject, source type, period — then read the response in layers
(title, URL, published date, highlight), then add only hard constraints, and
change the search type last.

## People — category `people`

LinkedIn-weighted. Vague queries ("researcher founder CEO") match thousands of
profiles; combine role, seniority, location, skills and source type —
"professional profiles of senior ML engineers in Seattle with PyTorch
experience". Qualify people by company traits in the same query rather than
building a company list first: "heads of security at Series B healthcare
software companies that sell to hospitals". Ask explicitly for personal
websites or public talks when you want their own words. For full coverage of
one organisation, search by department and seniority in parallel — engineering,
product and design, sales and marketing — then supplement outside LinkedIn:
the team page, "joined [company]" announcements, conference speaker lists.
Deduplicate by LinkedIn URL, falling back to name + current company.

## Companies — category `company`

Structured company data: description, stage, funding. Describe what the
companies *do* and for whom — "companies selling AI voice agents to dental
practices" — rather than "[category] companies". Three angles that together
cover a competitive set: what they do; operating signals ("remote staff
engineer roles at Series B fintech companies", pricing pages, job postings);
and funding on the general index with a date bound ("investors who led seed
rounds in robotics in the last year"). For a named company's funding and
investors, one general search on "[company] raised round investors" plus one
`company` search on the name. The `company` and `people` categories reject
domain and date filters with a 400, so a time window goes in the query there.

## Publications — category `publication`

Exa's paper index. Describe the method or finding, not guessed title keywords
("papers on evaluation benchmarks for retrieval-augmented generation"); by
"[topic] comprehensive survey review" to find the surveys first and read their
reference lists for the seminal work; by author name plus topic. Clinical
evidence: name phase, intervention and population. Regulatory: name the
regulator and the device or drug class. Prior art: describe the invention
functionally, the way a claim would. Trials, labels and approvals may fall
outside `publication` (it "limits results to papers"), so run those on the
general index. Bound recency with the published-date pair when the window is
a hard requirement; otherwise say the period in the query. For clinical or
life-science questions, Elicit and PubMed are the primary sources and this
pass is the supplement — see `source-map.md`.

## News — category `news`

Name the topic, the source type and the window: "news coverage of the EU AI
Act enforcement timeline published this month" on the `news` category, with
the published-date pair as the hard bound when the window matters. Name the
source type for practitioner analysis ("engineering blog posts about…") and
the format for discussion ("podcast episodes where…"). Adverse media:
describe the negative signal and the entity class, not "<name> news". For
reactions, run the sceptic's angle as its own call: "criticism and concerns
raised about [event] by [kind of critic]".

## Personal sites — category `personal site`

Exa's distinctive strength: blogs and first-hand accounts by people who did the
thing. "personal blog post by someone who [did X] describing what happened" —
this is where expected losers and honest failure modes surface, which a
long-list needs.

## Hidden relationships

Direct queries ("[X] clients") return articles about the subject, not
connections. Use indirect signals: the subject's own platforms (blog, podcast,
about page — fetch them); case studies and customer pages; testimonials on
personal blogs ("[subject] changed how we work"); duration markers ("worked
with [subject] for years", which people rarely fabricate); insider terminology
— find the subject's coined terms, then search for other people using them.

## Source quality — tag it, don't classify it

Before reading anything deeply, filter noise: no skin in the game (theorists
with nothing shipped), misaligned incentives (vendor blogs, affiliate pages,
sponsored content), circular credentials (validated only by peers in the same
bubble), positive-only advice (no trade-offs discussed), temporal decay (moved
from doing to advising — are they still practising?).

The distinction that matters most is practitioner versus commentator.
Practitioner signals: shipped products, case studies with specific numbers, "we
built X and here is what happened". Commentator signals: roundup posts, top-ten
lists, content that mainly links to others' work.

In the long-list, each row carries a short free-form quality note describing
what was observed — "shipped it, writes from direct experience" or "roundup,
no original work shown" — rather than a grade. Convergence among several
*independent high-signal* sources is evidence; three low-signal sources agreeing
is shared noise. Three sources all citing the same press release is one source.

Run credibility searches ("[name] results portfolio case study"; "[name]
criticism overrated") only when the task is expert-finding or best-of; for a
standard sweep, tag what the content already shows.

## Filtering rows — hard first, soft second

Hard filters are binary and mechanical: a date range, a geography, a numeric
threshold, membership of a category, a named exclusion. Apply them first and
drop rows that fail; no judgement needed. Soft filters need judgement —
"genuinely shipping" versus "evaluating", "first-hand" versus "roundup" — and
usually a read of the page. Apply them only to rows that survived the hard
filters, and record a one-line reason for each keep or drop so the reasoning is
visible. Ambiguous dates ("early 2025") are flagged, not silently resolved. The
request sets the balance: "find every" keeps borderline rows and flags them;
"the best" drops them. Default to keeping with a flag and letting the user
decide at the stop.
