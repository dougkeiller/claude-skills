---
date: 2026-08-26
source: claude-session
tags: [example, devils-advocate]
status: draft
---

# Devil's Advocate — moving from per-seat to usage-based pricing
Question as posed: "We're moving from per-seat to per-audit pricing. Poke holes in it before the board meeting."
Status: complete

> Worked example. Shows the working-note format and what non-generic output
> looks like. The plan below is a test fixture, not a real company.

## Stage 1 — The target

40-person B2B SaaS, compliance-tracking software for mid-market hospitals.
Moving from $450/seat/year (avg 60 seats) to $12 per compliance audit processed
(avg 3,400 audits/year). Rationale: usage matches value; model shows +18%
revenue on the existing base. All new customers from Q1, existing migrated at
renewal over 12 months, no grandfathering. Decision in 3 weeks.

**Stakes:** effectively irreversible once new logos have signed on the new
model. CEO and CRO aligned, board enthusiastic — no dissent recorded, which is
itself the reason to run this.

## Stage 2 — Six adversaries (spawned in parallel, no shared context)

**Attacker.** Compliance officers control the meter. They batch several checks
into one "audit," run marginal ones in Excel, defer the rest. Volume drops, the
model collapses — and the company has now priced customers for doing *less*
compliance, which becomes a discovery exhibit if a hospital under-audits and
someone is harmed. "Audit" is undefined, so every invoice is disputable.
Retries, duplicates and test runs inflate the meter and nobody is paid to fix it.

**Competitor.** No product change needed — a one-pager and a rep script inside
two weeks. "Predictable budget, unlimited audits." The 12-month no-grandfather
migration publishes the target list: every account has a known renewal date to
work backward from. Heavy users pay $40,800 against $27,000 today; offer a
fixed-price switch, free migration, 3-year lock. Light users get ignored — let
them keep the discount and the margin dilution. *Relieved to see:*
grandfathering, a cap, or a phased rollout.

**Skeptic.** The arithmetic does not close. $27,000 → $40,800 is +51%, not +18%.
The model is silently assuming roughly 22% volume decline or heavy discounting
and nobody has said which. The 3,400 average conceals skew — the median
customer's invoice may double while the mean shows +18%. Before believing it:
ten named renewal accounts shown their actual new invoice, reaction in writing.

**Pessimist.** Hospital finance issues POs for fixed annual amounts. A variable
line fails their budget process, so every renewal reopens as a 90-day
procurement approval — twelve months of those landing on about five AEs.
Cash flips from annual prepay to monthly arrears; roughly a quarter of
collections disappears during the migration year at 40 headcount. Metering must
be dispute-proof by Q1. Reversal is blocked because new logos have already
signed usage.

**Contrarian.** The reverse call: flat per-hospital or per-bed pricing, raised.
Per-audit billing turns every audit into variable spend the compliance director
must justify, so she rations. Volume drops, the data thins, the product stops
being system-of-record. Flat capture takes the same $13,800 spread with one PO,
no metering and billing-dispute stack, no ASC 606 variable-consideration rework
at 40 people — and it pushes audit volume *up*, deepening the moat that usage
pricing would tax.

**Auditor.** No named model owner, no documented assumptions, no
usage-suppression haircut; board minutes will record enthusiasm, not review.
No CFO or controller among the sponsors. ASC 606: per-audit fees are variable
consideration billed in arrears — ratable deferred revenue and the current ARR
definition collapse, and nobody has documented the recognition change or
restated prior-period ARR for diligence. The meter becomes the revenue system of
record with no count reconciliation, dispute-and-credit policy, immutable log,
or SOC 2 scope extension. No legal review of MSA repricing rights.
"No grandfathering" is a decision, not customer consent.

**Abstentions:** none.

## Stage 3 — Convergence

Five of six independently reached the same arithmetic: **$27,000 → $40,800 is
+51%, and the +18% figure implies an unstated ~22% volume decline.** No
subagent could see any other's work. That convergence is the strongest finding
here — stronger than any single objection.

Second convergence, three of six: **customers control the meter and will
ration.** Attacker, Skeptic and Contrarian each reached it from different
directions.

## Stage 5 — Ranked findings

| # | Finding | Impact x Likelihood x Detectability | Tripwire |
|---|---|---|---|
| 1 | The +18% and the unit economics disagree; the gap is an undocumented volume-decline assumption | High / High / **Poor — nobody is looking** | Model owner named and the haircut stated in writing, before the board meeting |
| 2 | Customers ration audits to control spend; the model's own assumption comes true and overshoots | High / High / Medium | Audits per customer per month, tracked from first migrated cohort; alarm at -10% |
| 3 | Fixed-budget POs cannot absorb a variable line; renewals reopen as 90-day procurements | High / Medium / Good | Days-to-close on the first five migrated renewals |
| 4 | Competitor weaponises the published renewal schedule with a fixed-price counter | Medium / High / Poor | Win/loss reason codes at renewal, from week one |
| 5 | ASC 606 variable consideration breaks the ARR definition mid-diligence | High / Medium / Poor until it is too late | Controller sign-off before the decision, not after |

## Stage 6 — What survived

The strategic logic is sound: usage pricing does align price with value here, and
the light-user segment genuinely is over-served by per-seat. No adversary
attacked the direction — five attacked the *arithmetic, the pacing and the
absence of a floor*.

**The one finding that would most change the decision:** the +18% and the +51%
cannot both be right, and until someone names the model owner and states the
volume assumption out loud, the board is approving a number nobody has
defended.

**Decision-relevant:** this does not read as no-go. It reads as *not in three
weeks, and not without a floor* — a minimum commitment, a cap on year-one
increase, and a defined "audit."
