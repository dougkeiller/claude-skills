---
name: context-switcher
description: >
  Generate every stakeholder's view of a decision in parallel, each developed
  independently so no viewpoint is contaminated by the others, then map where
  they genuinely conflict versus merely differ in emphasis. Use before anything
  that lands on people who were not in the room: reorganisations, pricing and
  packaging changes, policy and process changes, partnership and vendor
  decisions, product changes that shift who wins and who loses, board or
  investor communications, public positioning. Also use when a proposal has
  sailed through with everyone nodding, or when a rollout keeps stalling for
  reasons nobody can name. Trigger on "how will this land", "who might push
  back", "what will X think", "stakeholder view", "get buy-in", "sell this
  internally", "am I missing a perspective", "everyone seems on board".
---

# Context Switcher

Writing several perspectives in one pass produces one perspective wearing
several hats. The second view is drafted with the first still in view, the third
is reconciled with both, and by the fourth you are writing a consensus that no
actual person holds. The value here comes entirely from independence, which
means separate subagents, each of which cannot see the others.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

## Stage 1 — Enumerate, past the obvious ones

Write the decision into the note in the user's own words, then list the
stakeholders. The obvious three or four will already be in mind; the value is
in the ones that are not. Work through this list explicitly and record who you
ruled out and why:

- Who **loses** something — status, budget, headcount, autonomy, a workaround
  they rely on? Losers are systematically under-represented in planning.
- Who has to **execute** it, as opposed to approve it?
- Who has to **explain or defend** it to someone else?
- Who **inherits** it in two years, long after the deciders have moved on?
- Who is **downstream** — the customer's customer, the patient, the clinician
  at the desk, the analyst who consumes the output?
- Who **audits, regulates, or reviews** it?
- Who **was not asked** but will have an opinion the moment it ships?
- Which **competitor or adversary** benefits?

Five to eight is the working range. Fewer misses the point; more dilutes it.

For each, record who they are, what they are measured on, and what they stand to
gain or lose. That third item is what drives their view — not their job title.

## Stage 2 — Spawn them in parallel

**One subagent per stakeholder, all launched in a single message.** Each brief
contains: the decision, that stakeholder's role and incentives, and what they
would plausibly know at the time they hear about it — which is often much less
than the decision-maker knows.

Never include: the other stakeholders' briefs, the outcome you expect, which
stakeholders you consider important, or what the user hopes people will
conclude.

Ask each subagent for:

- Their first reaction, unfiltered.
- What they think this is really about — which is often not the stated rationale.
- What it costs them specifically.
- The strongest objection they can make that a reasonable person would accept.
- What they would need to see to support it.
- What they would do about it — support, comply quietly, resist openly, work
  around it, leave.

That last item matters most and is usually omitted. Quiet non-compliance is the
most common real response to a decision, and it never shows up in a stakeholder
map built by consensus.

## Stage 3 — Map the conflicts

Collect the views into the note verbatim first, then analyse. Sort every
disagreement into one of three bins, because they need completely different
responses:

**Real trade-off.** Two stakeholders want incompatible things and both are
right within their own frame. This cannot be communicated away. It has to be
decided, and someone has to be told they lost. Name who.

**Information gap.** They disagree because they know different things. Solvable
by showing the same facts — genuinely solvable, not "we need better comms" as a
euphemism for pushing through.

**Framing gap.** They agree on the facts and weigh them differently because
they are measured on different outcomes. Sometimes solvable by changing what
they are measured on; often not solvable at all, only managed.

Then look for what nobody said. If no stakeholder mentioned the thing that
worries you, either the concern is unfounded or you have missed a stakeholder.

## Stage 4 — Deliver

Lead with the sharpest thing found, not with a roster. Usually that is either
the strongest objection nobody in the room had voiced, or a real trade-off that
had been mistaken for a communication problem.

Then: the conflict map by bin, who genuinely loses and whether that is
acceptable, what would change each significant opponent's mind, and the one
stakeholder whose view most surprised you.

Where a real trade-off has been identified, do not soften it into a
both-and. The value delivered here is knowing which fight you are picking.

## Failure modes

- **Sequential drafting.** The failure this tool exists to prevent. Spawn them.
- **Cardboard stakeholders.** "Engineering will worry about tech debt." Real
  people have specific, self-interested, occasionally unreasonable views. A
  perspective nobody could disagree with was not worth generating.
- **Only the powerful.** Executives and customers get modelled; the person who
  has to run the new process at 7am does not.
- **Synthesising into consensus.** Averaging the views destroys the output. The
  disagreements are the finding.
- **Comms-washing.** Labelling a real trade-off an information gap because that
  version has a solution.
