# Parallel — the second search tier

Use Parallel when Exa comes back thin or off-target, and say in the note which
tier served the answer. Guidance from docs.parallel.ai/search/best-practices
(read 2026-11-10); re-read it if a call is rejected, because the API changes.

## How to ask

Parallel wants two things together, and they are different:

- `objective` — the research goal in natural language: what is being decided,
  what kind of source should rank first, how fresh it must be. Up to 5,000
  characters.
- `search_queries` — one to three **short keyword queries, 3-6 words each**,
  each a different angle. At least one is required; more than five are dropped.

**Never send the raw question as both the objective and the only query.**
Parallel's own guide names this as the most common mistake.

```json
{
  "objective": "Compare how mid-market CRM vendors price AI features, for a buyer choosing between them. Prefer vendors' own pricing pages and independent analyst reviews from the last 12 months.",
  "search_queries": ["CRM AI add-on pricing", "CRM copilot per-seat cost", "analyst review CRM AI features"]
}
```

## Other settings

- Reuse one `session_id` across the calls for one task; start a new one per task.
- Leave `mode` at its default unless latency matters.
- Source and freshness restrictions go in `advanced_settings`, and reduce
  coverage: use them only when a result outside them would be unusable, the
  same rule as Exa's hard filters.

## What carries over from the Exa rules

Everything in SKILL.md about framing, stopping, the source-mix check and
provenance applies unchanged. A Parallel excerpt is a summary-level read: a
figure that carries a decision is still read on its page.
