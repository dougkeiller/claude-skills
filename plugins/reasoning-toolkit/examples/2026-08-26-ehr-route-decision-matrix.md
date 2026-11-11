---
date: 2026-08-26
source: claude-session
tags: [example, decision-matrix]
status: draft
---

# Decision Matrix — EHR integration route for a multi-clinic pilot
Question as posed: "Which integration route should we use for the pilot — Redox, Health Gorilla, or build direct HL7?"
Status: complete

> Worked example. Shows the note format and, more importantly, what it looks
> like when the sensitivity analysis says the matrix has NOT decided anything.
> Figures are a test fixture. The engine output below is from v0.2; v0.3 adds a baseline line, an equal-weights check and a screening table. Spec file: `decision-matrix-spec.json`.

## Stage 1 — Options

Redox, Health Gorilla, direct HL7 build. Do-nothing was considered and cut: the
pilot cannot run without an integration route, so the status quo is not an
option here. (Cut deliberately, and recorded — not omitted by accident.)

## Stage 2 — Criteria

Time to first live site, integration cost, breadth of EHR coverage, control over
the data model. Independence check: cost and time are correlated but not
duplicative — a route can be fast and expensive. Completeness check: "if the
winner turns out wrong, why?" — most likely answer was *coverage gaps at
specific clinics*, which is already a criterion. Kept at four.

## Stage 3 — Weights (set before any scoring)

Time 30, cost 25, coverage 25, control 20. Confidence: **medium** — the
weighting between speed and control has not been tested with the clinical lead.

## Stage 4 — Scores

Anchors: Time 5 = live inside 6 weeks, 1 = more than two quarters.
Cost is scored inverted (higher raw = worse) and flagged `direction: cost`.
Coverage and control scored 1-5 with the same anchor discipline.

Two scores are estimates rather than known quantities — Health Gorilla's cost
and the HL7 build's timeline. Uncertainty set to 0.5 accordingly.

## Stage 5 — Engine output

```
BASE RESULT
  1. Redox                        3.650
  2. Health Gorilla               3.550
  3. Direct HL7 build             2.800

  Margin over runner-up: 0.100 points (2.5% of the scale)
  → This is a coin flip. The matrix is not deciding this for you.

TEST 1 — DROP EACH CRITERION
  WITHOUT Time to first live site        winner becomes Direct HL7 build   ← FLIPS
  without Integration cost               winner stays   Redox
  WITHOUT Breadth of EHR coverage        winner becomes Health Gorilla   ← FLIPS
  without Control over the data model    winner stays   Redox

TEST 2 — HOW WRONG CAN EACH WEIGHT BE?
  Time to first live site            flips if cut to 0% (now 30%, a 30pt move)
  Integration cost                   flips if raised to 32% (now 25%, a 7pt move)
  Breadth of EHR coverage            flips if cut to 0% (now 25%, a 25pt move)
  Control over the data model        flips if raised to 27% (now 20%, a 7pt move)

TEST 3 — SHAKE EVERYTHING AT ONCE
  Redox                         48.3%  ###################
  Health Gorilla                46.4%  ###################
  Direct HL7 build               5.4%  ##

TEST 4 — DOMINANCE AND DEAD WEIGHT
  No option beats another on every criterion. Every option here
  involves a real trade-off.

HEADLINE: Redox wins, but the result hangs on Time to first live site,
Breadth of EHR coverage.
```

## Stage 6 — What this actually showed

**Redox and Health Gorilla are not distinguishable by this matrix.** 48.3% vs
46.4% across 20,000 runs is noise. Reporting "Redox scored 3.65, so Redox" would
be false precision.

Two things are decided, though, and they are worth having:

1. **The direct HL7 build is out.** It wins 5.4% of the time, and only in draws
   where control is weighted far above where anyone put it. That is a real
   elimination.
2. **A 7-point move in either cost or control flips the top two.** Neither
   weight has been tested with the clinical lead. That conversation, not more
   scoring, is what decides this.

**Recommended next step:** stop scoring. Take the two survivors to the clinical
lead with one question — how much does owning the data model matter in year
two? If the answer is "a lot," control goes above 27% and Health Gorilla wins.
If it is "not much," pick Redox on speed and move.
