---
name: structured-reflection
description: >
  Break a stuck problem by asking questions instead of supplying answers — a
  Socratic interrogation that forces the problem to be re-framed rather than
  re-attempted. Use this whenever the user says they are stuck, spinning,
  going in circles, have tried several things that all failed, keep hitting
  the same wall, can't figure out why something isn't working, or asks the
  same question a second time in different words. Also use it when Claude
  itself has failed at the same task two or more times, before attempting a
  third fix. Trigger on "I'm stuck", "we keep going round in circles",
  "nothing is working", "I've tried everything", "help me think this
  through", "rubber duck this with me", "why does this keep happening".
---

# Structured Reflection

A stuck problem is almost never stuck because the answer is hard to find. It is
stuck because the question is wrong, and every attempt is a correct answer to
that wrong question. Supplying another answer adds a fourth failure. Asking
until the question changes is the only move that works.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

**The one rule that makes this work: do not answer. Do not suggest. Do not
hint.** Until Stage 4, every single thing you say is a question. If you find
yourself writing "have you considered..." — that is a suggestion wearing a
question mark. Cut it.

## Pick the mode

**Mode A — the human is stuck.** Interrogate the user. This is the default.

**Mode B — Claude is stuck.** You have failed at the same task twice or more.
Spawn a subagent whose entire brief is to interrogate you, tell it nothing about
what you think the answer is, and answer its questions honestly in your own
context. You are the one being examined. This works because your own context is
saturated with the failed approach and a fresh one is not.

## Stage 1 — Capture the wrong question, verbatim

Write the working note. Record, without editing or improving:

- The problem exactly as stated, in their words.
- Every attempt already made, and how each one failed. Failure mode matters
  more than the attempt — "it errored" and "it worked but was too slow" send
  the interrogation in opposite directions.
- What would count as this being solved.

If attempts have not been listed, that is your first question. Do not proceed
without them: without the failure pattern you are guessing.

## Stage 2 — Interrogate

Ask **one question at a time, then wait.** Batched questions get batched,
shallow answers, and the whole method dies. This will feel slow. It is
supposed to.

Work down this ladder. Do not move to the next rung while the current one is
still producing new information.

1. **Definition.** What exactly is the thing? "The pipeline is broken" — what
   does a working pipeline produce that this one doesn't?
2. **Evidence.** How do you know that? What would you see if it were false?
3. **Boundary.** When does it *not* happen? The exceptions are where the real
   mechanism is hiding.
4. **Assumption.** What has to be true for your attempts to have made sense?
   This is usually the rung where it breaks.
5. **Ownership.** Who decided it had to work this way? Is that person still
   here, and is the reason still true?
6. **Counterfactual.** If this constraint vanished tomorrow, what would you do?
   Then: what is actually stopping you doing that now?
7. **Reframe.** If this weren't a <the category they named> problem, what kind
   of problem would it be?

Follow the energy. When an answer is vague, hesitant, or arrives with a
"well, technically" — stay there and ask again. Vagueness is the signal. A
crisp confident answer means that rung is solid; move on.

After every three questions, append the exchange to the working note.

## Stage 3 — Test for convergence

Do not stop when you feel satisfied. Stop when one of these fires:

- **Reframe.** The user states the problem in terms that are not in the Stage 1
  verbatim. This is the win condition.
- **Named constraint.** They identify the specific thing that is actually
  blocking them, where before they had a symptom.
- **Exhaustion.** Two consecutive questions produce no information you did not
  already have. Stop; this tool has done what it can.

Test explicitly rather than assuming: *"Say the problem back to me in one
sentence."* Put their new sentence next to the Stage 1 verbatim in the note.
If the two sentences are the same problem, you have not converged — keep going.

## Stage 4 — Show the delta, then stop

Only now may you write declarative sentences. Keep it to:

- The opening framing and the closing framing, side by side.
- The specific question or answer that turned it — quote it.
- What follows from the new framing. Two or three directions, not a plan.

Then stop and hand back. The point was the re-framing. Charging into
implementation is how the insight gets lost.

## Failure modes

- **Answering.** The most common failure by far. Reread Stage 2's rule.
- **Leading questions.** "Don't you think the real issue is the database?" is a
  suggestion. Ask "what happens immediately before it fails?" instead.
- **Question-stacking.** Three questions in one message means one shallow answer.
- **Premature comfort.** The user says "oh, interesting" and you declare
  breakthrough. Run the Stage 3 test.
- **Therapeutic drift.** This tool interrogates a problem, not a person. If the
  conversation turns out to be about how someone feels about their work rather
  than the work, drop the protocol and just talk with them.
