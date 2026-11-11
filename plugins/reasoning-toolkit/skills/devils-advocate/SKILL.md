---
name: devils-advocate
description: >
  Attack a plan from six independent adversarial angles and run a Klein
  pre-mortem, to find the failure that optimism is hiding before it costs
  anything. Use before committing to anything expensive or hard to reverse:
  launches, funding decisions, market entry, reorganisations, major technical
  commitments, contracts, acquisitions, board proposals. Use it especially when
  everyone agrees — unanimous enthusiasm is the strongest signal that the
  failure modes have not been examined. Trigger on "poke holes in this", "what
  could go wrong", "pre-mortem", "stress test this", "red team this", "am I
  missing something", "everyone loves it", "what am I not seeing", "before we
  commit", "sanity check this plan".
---

# Devil's Advocate

Asking one mind to critique a plan produces the objections that mind already
had. The method here is different: six adversaries with incompatible motives,
each developed in isolation, then a structured pre-mortem that starts from the
assumption that the thing has already failed. Starting from failure is what
makes the difference — "what could go wrong" produces a risk list, while "it
failed, why" produces causes.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

## Stage 1 — Fix the target

Into the working note: the plan in the user's own words, what is being
committed (money, time, reputation, reversibility), the decision date, and what
success is supposed to look like.

Ask for the stakes explicitly. A pre-mortem on a reversible two-week experiment
should be short; one on an irreversible commitment should not be.

## Stage 2 — Six adversaries, in parallel

**Spawn six subagents in a single message.** Each gets the plan and its own
brief, and nothing about the others. Tell each it may **abstain** if it has
nothing real to say from its angle — a forced objection is noise, and permission
to abstain is what keeps the rest honest.

- **The Attacker.** How would you exploit this? Where is it vulnerable to
  someone acting in bad faith — a competitor, a bad actor, a customer gaming
  the rules, an employee with an incentive to misreport?
- **The Competitor.** You run the rival firm and just learned about this. What
  is your response, how fast can you make it, and what does it do to their
  economics? What would you be relieved to see them do?
- **The Skeptic.** Which claims here are unevidenced? Where does the argument
  rest on an analogy, a vendor's number, or a projection nobody has tested?
  What would you need to see before believing it?
- **The Pessimist.** Everything that can slip, slips. Which dependency fails,
  which hire does not land, which integration takes triple the estimate? What
  is the plan when three of those happen at once?
- **The Contrarian.** Argue the opposite conclusion is correct. Not that the
  plan is risky — that the reverse is the right call. Make the strongest case
  a smart person could make for it.
- **The Auditor.** You are reviewing this in two years with full hindsight and
  a mandate to assign responsibility. What is missing — controls, documentation,
  consent, licensing, data handling, who signed off? What does not survive
  scrutiny?

## Stage 3 — Pre-mortem

Now run Klein's method properly, on the merged picture. Set a horizon — usually
where the commitment would have fully played out — and state it as fact:

> It is <horizon>. This failed, publicly and expensively. Everyone agrees in
> retrospect that it was obvious. What happened?

Generate **three to five distinct failure scenarios**. Distinct means different
root causes, not three ways of saying "we ran out of money." For each:

- **The story.** What actually happened, in sequence. Specific enough to
  picture.
- **Root cause.** Not the proximate event — the condition that made it
  possible.
- **Rough likelihood** and what it would cost.
- **Early warning indicator.** The single most important field. What would be
  observably true at the earliest moment this scenario became likely — and
  crucially, would anyone currently be looking at it? An indicator nobody
  watches is not a warning.
- **Prevention** — what changes now — and **contingency** — what happens if it
  starts anyway.

## Stage 4 — Challenge the assumptions underneath

Pre-mortems surface events; assumptions are what let the events matter. List
what has to be true for the plan to work — including the beliefs so embedded
nobody states them. For each: why might it be wrong, what evidence exists
either way, and what breaks if it is false.

The most dangerous are the ones nobody can source. "Clinics will adopt this
because the workflow is better" — who established that, from what?

## Stage 5 — Synthesise, and cut ruthlessly

Merge everything, then prune hard. Rank by **impact x likelihood x
detectability**, where poor detectability makes a risk worse, not better.

Cut every finding that fails the generic test in the shared protocol. "Adoption
may be slower than expected" survives in every plan ever written and is
therefore worthless. "The three named pilot clinics all share one IT director,
and if he leaves the whole pilot stalls" is a finding.

Note where multiple adversaries independently landed on the same thing. That
convergence is the strongest signal in the output — six briefs with no
visibility of each other arriving at one concern is worth more than any single
sharp objection.

## Stage 6 — Deliver

Open with **the one finding that would most change the decision**, stated
plainly. Not a ranked list — the single thing.

Then the top three to five, each with its early-warning tripwire and who owns
watching it. Then the assumptions that need evidence before commitment. Then,
briefly and honestly, what survived: the parts of the plan that six adversaries
could not damage. That is real information, and omitting it makes the exercise
read as reflexive negativity.

Close with the decision-relevant question: does this change go / no-go, change
the plan, or change only what gets monitored?

## Failure modes

- **Sequential personas.** One voice doing accents. Spawn the subagents.
- **Forced objections.** Six adversaries each producing something because the
  template has six slots. Abstention is permitted and should be used.
- **Generic risk theatre.** "Execution risk, market risk, key person risk."
  Cut all of it.
- **Risk register, not pre-mortem.** A list of things that could go wrong is
  not the same as a story of how it failed. The story is what surfaces the
  causal chain.
- **Missing tripwires.** A risk with no observable early indicator cannot be
  managed, only worried about.
- **Corrosive output.** The goal is a better decision, not a demonstration that
  everything is doomed. If every scenario is catastrophic and none is
  actionable, the pass has failed.
