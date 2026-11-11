---
name: hindsight
description: >
  Run a post-mortem that separates decision quality from outcome quality, using
  a cold reader who is shown only what was knowable at the time and never learns
  how it turned out. Use after anything has concluded and is being reviewed: a
  failed launch or deal, a project that overran, a hire that did not work, a
  bet that paid off, an incident, a quarter that missed or beat. Use it
  especially when a review has already settled on a lesson — settled lessons are
  usually hindsight bias wearing a conclusion. Trigger on "post-mortem",
  "retrospective", "lessons learned", "what went wrong", "should we have seen
  this coming", "we should have known", "reviewing what happened", "why did
  this fail", "debrief", "how did we get this so wrong".
---

# Hindsight

Once you know how something turned out, you cannot un-know it, and every
judgement about the decision is contaminated. The outcome feels foreseeable, the
warning signs feel obvious, and the review concludes that someone should have
seen it. Most post-mortems produce this and call it a lesson.

The fix is structural, not a matter of trying harder to be fair: reconstruct the
information state at decision time, then have someone judge the decision who has
never been told the outcome.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

## Stage 1 — Reconstruct the decision, not the outcome

Into the note: what was decided, by whom, when, and what the alternatives were.
Just the decision. The outcome comes later and stays out of this section.

Then build the three-column split — the heart of the method:

| Knew at the time | Could have known | Could not have known |
|---|---|---|

- **Knew** — actually in front of the deciders. Documents, numbers, opinions
  voiced.
- **Could have known** — existed and was reachable with reasonable effort but
  was not sought. This column is where process failures live, and it is the
  only column that yields real lessons.
- **Could not have known** — unknowable then, at any effort. Be strict and
  generous at once: things that only became knowable *because* of what happened
  belong here, however obvious they now feel.

Two questions that reliably improve this stage: **who dissented at the time,
and was their objection audible?** A dissent recorded in a document nobody read
is different from one raised in the room and overruled. And: **what was the
decision competing with for attention?** Decisions made in a crisis or during a
fundraise get judged later as though they had a quiet week's consideration.

## Stage 2 — The cold reader

**Spawn a subagent and give it only the "knew at the time" column, the
alternatives available, and the constraints.** Never the outcome. Never a hint
of what you are hoping it will say.

Ask it: which option would you choose, and why? What is the strongest case
against your choice? What would you want to know before deciding, and could you
get it? What is the biggest risk in your choice, and how would you watch for it?

This is the one mechanism that makes hindsight bias structurally impossible for
this step, and it is the reason to use this skill rather than simply intending
to be fair. Record its answer verbatim before continuing.

If subagents are unavailable, say so and flag the reduced confidence — a
self-administered blind review by someone who knows the outcome is not blind.

## Stage 3 — Reveal, then classify

Now state what actually happened, and place it in the grid:

|                    | Good outcome | Bad outcome |
|--------------------|--------------|-------------|
| **Good decision**  | Earned       | Bad luck    |
| **Bad decision**   | Lucky        | Deserved    |

Decide "good decision" using the cold reader's judgement, not your own — this
is what the cold reader was for. Where the cold reader chose the same option
that was actually chosen, the decision was reasonable on the information
available, whatever followed.

**Bad luck** and **lucky** are the two cells that post-mortems systematically
refuse to use, and they are the most important. A good decision with a bad
outcome should be *reinforced*, not corrected — punishing it teaches the
organisation to avoid sound risks. A bad decision with a good outcome is the
most dangerous cell of all, because success ratifies a broken process. If the
outcome was good, run this anyway; that cell is exactly what a celebration
hides.

## Stage 4 — Extract the process lesson

One rule governs this stage: **fix the process, not the answer.**

- Banned: "next time we should choose X." That is the answer, available only
  because you know the outcome. It generalises to nothing.
- Required: "our process did not surface Y, which was in the *could have known*
  column, and here is the change that would surface it next time."

Every lesson must trace to the middle column. If it traces to *could not have
known*, the lesson is about resilience and reversibility — how to fail more
cheaply — not about foresight. If it traces to *knew at the time*, the failure
was in weighting or courage, not information, and the fix is different again.

Then test each lesson: **would it have helped in any other decision, or only
this one?** A lesson that applies only to the exact situation that just occurred
is hindsight bias in the shape of an action item.

## Stage 5 — Deliver

Lead with the classification — "good decision, bad outcome" — because it sets
whether this is a correction or a reinforcement, and everyone in the room is
waiting to know which.

Then: what the cold reader concluded and how that compares to what was done;
the two or three lessons with their column traced; and explicitly, what should
*not* change. Naming what was done well and should be repeated is half the
value, and post-mortems almost always omit it.

## Banned language

Strike these on sight, in your own output and in the material under review.
Each is hindsight bias with a vocabulary:

- "Obviously", "clearly", "of course" — applied to anything about the decision.
- "Should have known", "red flags everywhere", "all the signs were there".
- "Inevitable", "doomed from the start", "always going to happen".

When someone uses one, ask the question underneath it: *what specifically was
visible then, and to whom?* That question is usually the most productive
moment in the whole review.

## Failure modes

- **Contaminated cold reader.** Any leak of the outcome voids the exercise.
- **Skipping the reveal order.** Judging the decision after stating the outcome
  is the ordinary post-mortem this tool exists to replace.
- **Refusing the luck cells.** Every outcome gets attributed to decision
  quality, which is how organisations learn superstitions.
- **Answer-shaped lessons.** "Pick the other vendor next time."
- **Blame.** The three-column split is a bias correction, not a defence brief.
  If the review turns into establishing who is at fault, the lessons stop
  arriving, because nobody will tell you what was in the middle column.
