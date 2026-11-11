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
test with actual arithmetic: weight perturbation, drop-one analysis, and a
Monte Carlo over both weights and scores.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

## Stage 1 — Options

Get the real option set into the working note. Two checks:

- **Is anything missing?** Ask for the option nobody has written down — usually
  do nothing, delay, or a narrower version of the winner. Do-nothing belongs in
  almost every matrix; without it you cannot tell whether the winner beats the
  status quo or merely beats the other things on the list.
- **Is anything already dead?** An option nobody would accept regardless of
  score is padding, and it distorts nothing except the user's sense that the
  process was thorough. Cut it and say why.

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

## Stage 3 — Weights, before the scores are visible

Set and record weights **before** scoring any option. This is the single most
important sequencing rule here. Weights chosen after seeing the scores are not
priorities; they are a justification for a decision already made.

Use whole numbers summing to 100. Force real differentiation — if everything
lands between 15 and 20, nothing is being prioritised and the matrix will
produce a near-tie by construction. Ask what the user would give up if forced.

Also capture how firm the weights are — high, medium, or low confidence. That
drives how hard the Monte Carlo shakes them.

## Stage 4 — Score by criterion, not by option

Use a 1-5 scale. Score **one criterion across every option, then the next
criterion** — never one option across all criteria. Scoring an option as a
whole produces halo effects: a favoured option quietly scores well on
everything.

Anchor the ends before scoring: what does a 5 mean here, and a 1? Record the
anchors in the note.

Where a score is a guess rather than a known quantity, say so in the note. That
feeds the uncertainty parameter, and a matrix built on four guesses and two
facts should not be presented as arithmetic.

## Stage 5 — Run the engine

Write the spec as JSON and run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/sensitivity.py spec.json
```

Spec format:

```json
{
  "decision": "Which EHR integration route for the pilot",
  "scale": [1, 5],
  "options": ["Redox", "Health Gorilla", "Direct HL7 build"],
  "criteria": [
    {"name": "Time to first live site", "weight": 30, "direction": "benefit"},
    {"name": "Integration cost", "weight": 25, "direction": "cost"}
  ],
  "scores": {
    "Redox": {"Time to first live site": 5, "Integration cost": 4},
    "Health Gorilla": {"Time to first live site": 4, "Integration cost": 3},
    "Direct HL7 build": {"Time to first live site": 1, "Integration cost": 2}
  },
  "score_uncertainty": 0.5,
  "weight_confidence": "medium"
}
```

`direction` is `benefit` (higher is better) or `cost` (higher is worse).
`weight_confidence` is `high`, `medium`, or `low`.

The engine returns four tests: drop-each-criterion, the weight at which each
criterion flips the winner, a 20,000-run Monte Carlo win probability, and
dominance plus dead-weight detection. Paste its full output into the note. It
requires the numbers to be written down, which is itself part of the discipline
— you cannot run it on a vague impression.

## Stage 6 — Report what the sensitivity actually showed

Lead with robustness, not with the winner. "Redox wins, but only in 48% of runs
— this matrix is not deciding it for you" is a far more useful sentence than
"Redox scores 3.65."

Then cover: which criteria the result hangs on, how far a weight would have to
move to flip it and whether that move is plausible, any dominated or
dead-weight items, and — if the top two are within a few percent — say plainly
that the matrix has not separated them and name what should decide instead.

**A near-tie is a real finding, not a failure.** It usually means either the
options are genuinely equivalent (pick on speed or reversibility and move on)
or the criterion that actually matters is missing from the matrix. Ask which.

## Failure modes

- **Weights after scores.** The cardinal sin. Sequence it properly.
- **Scoring by option.** Produces halos. Score by criterion across options.
- **Flat weights.** Everything at 15-20% means nothing was prioritised.
- **Missing do-nothing.** Leaves you unable to tell whether the winner is good
  or merely least bad.
- **Reporting the number, hiding the fragility.** The sensitivity output is the
  deliverable; the score is the input.
- **Rerunning until it agrees with you.** Adjusting weights until the preferred
  option wins is fine only if the new weights are honestly what you believe —
  and the note should record that they changed, and why.
