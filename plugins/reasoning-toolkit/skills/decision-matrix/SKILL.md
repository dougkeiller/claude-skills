---
name: decision-matrix
description: >
  Score options against weighted criteria and then actually test whether the
  answer survives different priorities, using real sensitivity analysis rather
  than an assertion that the result is robust. Use whenever choosing between
  named alternatives: vendor and platform selection, build vs buy, hiring
  between finalists, which market or segment to enter, which initiative to fund,
  choosing between offers or sites or partners. Also use when someone has
  already built a scoring spreadsheet and wants to know whether to trust it, or
  when a decision keeps getting re-litigated. Trigger on "which should we pick",
  "compare these options", "weighted scoring", "decision matrix", "help me
  choose between", "score these vendors", "we keep going back and forth on
  this", "does this decision hold up".
---

# Decision Matrix

A weighted scoring matrix produces a number, and the number produces false
confidence. The useful question is never "which option scores highest" — it is
"how much would have to be wrong for the answer to change." This skill runs that
test with actual arithmetic: weight perturbation, drop-one analysis, an
equal-weights check, and a Monte Carlo over both weights and scores.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

## Stage 1 — Options

Get the real option set into the working note. Five checks:

- **Is the baseline there?** Do nothing, or the status quo, is an option in
  every matrix and the engine will not run without one. Without it you cannot
  tell whether the winner is good or merely the least bad. Name it in the spec
  as `"baseline"`. Only when there genuinely is no status quo, set it to `null`
  and say why in the note.
- **Is anything else missing?** Ask for the option nobody has written down —
  usually delay, or a narrower version of the favourite.
- **Must-haves first.** Ask what any acceptable option must do or must not do.
  An option that fails a must-have is out before scoring, and the note says
  which one and why. A weighted sum lets a strong score on one criterion offset
  a fatal weakness on another; screening is how that is prevented.
- **Is anything already dead?** An option nobody would accept regardless of
  score is padding. Cut it and say why.
- **Exclusive, or can they be combined?** Ask directly: is this a choice of
  one, or could several of these be used together? If they can be combined,
  group them by the job each does and record the groups in the spec
  (`"groups"`). The answer is then one pick per group, and ranking them all
  against each other as rivals is the wrong question.

## Stage 2 — Criteria, before any scoring

Three to seven. Fewer misses real considerations; more dilutes weight until
nothing distinguishes anything.

Test the set:

- **Independence.** Overlapping criteria double-count. "Cost" and "Budget fit"
  are one criterion; scoring both gives cost twice its stated weight.
- **Discrimination.** A criterion where every option scores the same cannot
  affect the outcome. The engine flags these, but catching them here is better.
- **Completeness.** Ask directly: if the winner turned out to be wrong, what
  would the reason most likely be? If that reason is not a criterion, add it.
- **Direction.** For each, is a higher raw score better or worse? Cost-type
  criteria get inverted by the engine; declare which they are.

## Stage 3 — Anchor each scale, before weights

Use a 1-5 scale. For every criterion, write down what a 1 and a 5 mean **for
this decision** — the worst and the best level plausibly on offer, not the
worst and best imaginable. Record the anchors in the note.

This comes before weighting because a weight has no meaning without the range
it applies to. "Cost matters a lot" is true when options run from 10k to 500k
and false when they run from 40k to 45k.

## Stage 4 — Weights, before any option is scored

Set and record weights **before** scoring any option. Weights chosen after
seeing the scores are not priorities; they are a justification for a decision
already made.

Ask about each criterion in terms of its range, not its importance in the
abstract: *"how much does it matter to move from the 1 to the 5 on this
criterion, compared with doing the same on the others?"* One question per
criterion is enough; do not run a longer elicitation exercise unless asked.

Use whole numbers summing to 100. Force real differentiation — if everything
lands between 15 and 20, nothing is being prioritised and the matrix will
produce a near-tie by construction. Ask what the user would give up if forced.

Also capture how firm the weights are — high, medium, or low confidence. That
drives how hard the Monte Carlo shakes them.

## Stage 5 — Score by criterion, not by option

Score **one criterion across every option, then the next criterion** — never
one option across all criteria. Scoring an option as a whole produces halo
effects: a favoured option quietly scores well on everything. Score against the
Stage 3 anchors.

Where a score is a guess rather than a known quantity, say so in the note. That
feeds the uncertainty parameter, and a matrix built on four guesses and two
facts should not be presented as arithmetic. Uncertain scores often move the
result more than uncertain weights do.

## Stage 6 — Run the engine

Write the spec as JSON and run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/sensitivity.py spec.json
```

The engine needs numpy. If `python3` does not have it, the script says so; run
it as `uv run --with numpy python ${CLAUDE_PLUGIN_ROOT}/scripts/sensitivity.py spec.json`.

Spec format:

```json
{
  "decision": "Which EHR integration route for the pilot",
  "scale": [1, 5],
  "options": ["Redox", "Health Gorilla", "Direct HL7 build", "Stay on manual entry"],
  "criteria": [
    {"name": "Time to first live site", "weight": 30, "direction": "benefit"},
    {"name": "Integration cost", "weight": 25, "direction": "cost"}
  ],
  "scores": {
    "Redox": {"Time to first live site": 5, "Integration cost": 4},
    "Health Gorilla": {"Time to first live site": 4, "Integration cost": 3},
    "Direct HL7 build": {"Time to first live site": 1, "Integration cost": 2},
    "Stay on manual entry": {"Time to first live site": 5, "Integration cost": 1}
  },
  "score_uncertainty": 0.5,
  "weight_confidence": "medium",
  "baseline": "Stay on manual entry"
}
```

`direction` is `benefit` (higher is better) or `cost` (higher is worse).
`weight_confidence` is `high`, `medium`, or `low`. `baseline` is required.

Two optional fields:

- `"top_k": 5` — **screening mode**, for cutting a long-list rather than picking
  a winner. The engine reports how often each option lands in the top k and how
  often it beats the baseline. It turns on by itself at ten or more options.
- `"groups": {"Option A": "job one", "Option B": "job two"}` — for options that
  can be combined (Stage 1). The engine ranks within each group.

The engine returns: the base ranking against the baseline, an equal-weights
check, drop-each-criterion, the weight at which each criterion flips the
winner, a 20,000-run Monte Carlo win probability, the screening table, and
dominance plus dead-weight detection. Paste its full output into the note.

## Stage 7 — Report what the sensitivity actually showed

Lead with robustness, not with the winner. "Redox wins, but only in 48% of runs
— this matrix is not deciding it for you" is a far more useful sentence than
"Redox scores 3.65."

Then cover: whether the winner beats the baseline and how reliably; whether it
survives equal weights; which criteria the result hangs on; how far a weight
would have to move to flip it and whether that move is plausible; any dominated
or dead-weight items; and — if the top two are within a few percent — say
plainly that the matrix has not separated them and name what should decide
instead.

**When screening a long-list**, the deliverable is the cut, not a winner. Report
which options reliably make the top k, which sit on the edge, and which do not
beat the baseline. Put the cut where reliability drops, and say that options on
the edge are a judgement call for the user.

**When options are combinable**, report the pick in each group and whether it
beats the baseline. Do not present the overall ranking as the answer.

**A near-tie is a real finding, not a failure.** It usually means either the
options are genuinely equivalent (pick on speed or reversibility and move on)
or the criterion that actually matters is missing from the matrix. Ask which.

## Failure modes

- **Weights after scores.** The cardinal sin. Sequence it properly.
- **Weights without ranges.** "Importance" in the abstract. Anchor first.
- **Scoring by option.** Produces halos. Score by criterion across options.
- **Flat weights.** Everything at 15-20% means nothing was prioritised.
- **Missing do-nothing.** Leaves you unable to tell whether the winner is good
  or merely least bad. The engine refuses to run without a baseline.
- **Ranking things that are not rivals.** Options that can be combined need
  groups, not a league table.
- **Letting a high total hide a fatal flaw.** Screen on must-haves first.
- **Reporting the number, hiding the fragility.** The sensitivity output is the
  deliverable; the score is the input.
- **Rerunning until it agrees with you.** Adjusting weights until the preferred
  option wins is fine only if the new weights are honestly what you believe —
  and the note should record that they changed, and why.
