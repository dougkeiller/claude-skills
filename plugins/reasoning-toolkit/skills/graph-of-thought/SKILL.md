---
name: graph-of-thought
description: >
  Explore several genuinely different approaches in parallel, score them against
  a rubric fixed in advance, then merge the strongest elements into a composite
  path. Use when a problem has more than one defensible approach and the first
  idea is likely to be anchored on: architecture and build-vs-buy choices, GTM
  strategy, positioning, pricing structure, how to sequence a programme, any
  "there are a few ways we could do this" question. Also use when the team has
  converged suspiciously fast, or when the obvious approach has a known flaw and
  the alternatives have not been explored. Trigger on "what are our options",
  "explore some approaches", "is there a better way to do this", "we could
  either... or...", "brainstorm the alternatives", "compare a few strategies",
  "I only see one way to do this".
---

# Graph of Thought

Linear reasoning commits to the first plausible branch and spends the rest of
its effort defending it. This tool forces genuine branching, scores against a
rubric written before the branches are seen, and — the part that separates it
from a simple options list — merges across branches, because the best answer is
usually elements of two approaches rather than one approach whole.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

## Stage 1 — Rubric before branches

Write the scoring rubric into the working note **before** generating any
approach. Rubrics written afterwards are rationalisations of a preference you
already hold.

Three to five criteria, each with a weight and — this is the part that gets
skipped — a description of what a 1 and a 5 actually look like for this
problem. "Speed: 5 = live in under six weeks; 1 = more than two quarters."
Without anchors, scoring collapses into vibes.

Confirm the rubric with the user if the stakes justify it. Changing the rubric
after seeing the branches is allowed exactly once, must be recorded in the note
with a reason, and requires rescoring everything.

## Stage 2 — Branch, genuinely

Name three to five approaches that are **structurally different**, not three
flavours of the same idea. Test each against the others: if two branches would
be executed by the same team, on the same timeline, using the same tools, they
are one branch.

Reach deliberately for the branches nobody proposes:

- The **do-nothing** branch. What happens if this is left alone? It is
  surprisingly often the winner, and it anchors every other branch's real cost.
- The **inverted** branch. Solve the opposite problem, or solve it for a
  different party.
- The **buy/borrow** branch when everyone assumes building.
- The **narrow** branch. Solve it for one segment or one site completely,
  instead of everyone partially.
- The **constraint-free** branch. What would you do with twice the budget or no
  legacy system? Sometimes a cheap version of it is available.

## Stage 3 — Expand each branch independently

**Spawn one subagent per branch, all in a single message so they run
concurrently.** Each gets the problem, its own branch, and the rubric — and
nothing about the other branches or which one you favour. This independence is
the whole point: developed in one context, later branches get written as
strawmen for the first.

Brief each subagent to return: how the approach actually works, what has to be
true for it to succeed, its strongest single advantage, its worst realistic
failure, roughly what it costs in time and money, and a self-score against each
rubric criterion with reasoning.

Instruct each one to argue its branch honestly — advocate, but do not conceal.
A subagent that hides its branch's fatal flaw has wasted the exercise.

## Stage 4 — Score, and take the self-scores with salt

Every branch's advocate will score it generously. Rescore each branch yourself
against the anchors from Stage 1, in one pass **per criterion across all
branches** rather than per branch across all criteria — scoring a whole branch
at once produces halo effects where one strong dimension lifts the rest.

Record the table in the note, with your score and the advocate's score side by
side. A large gap is informative: it usually means the advocate was relying on
something that does not survive comparison.

If the top two are within roughly 10% of each other, say so. The rubric is not
precise enough to separate them, and pretending otherwise is false confidence.

## Stage 5 — Merge

This is the stage that makes it a graph rather than a list. For the leading
branch, ask of every other branch: what does it do better, and can that element
be transplanted?

Most merges fail, and the note should record why. A merged element must be
**separable** (it does not depend on the rest of its parent branch) and
**compatible** (it does not contradict the host branch's core assumption).
Grafting a build-it-ourselves data model onto a buy-the-platform branch usually
fails the compatibility test — say so rather than producing an incoherent hybrid.

Where a merge works, name it explicitly: "Branch B, plus the phased site
rollout from Branch D, which is separable because it only governs sequencing."

Rescore the merged path. If it does not beat the unmerged leader, discard it.

## Stage 6 — Deliver

Recommended path first, in one sentence. Then: what it borrowed and from where,
its score against the runner-up and whether that gap is meaningful, the single
assumption that would most change the answer if wrong, and what the runner-up
was better at — because that is what will be lost, and someone should be
watching it.

Keep the discarded branches in the note. When the recommendation is
re-litigated in six weeks, "we considered that and here is what it scored" is
the most valuable thing in the file.

## Failure modes

- **Fake branches.** Three variations of one idea. Apply the same-team test.
- **Sequential expansion.** Writing all branches in one context. Contaminated by
  construction — spawn the subagents.
- **Post-hoc rubric.** Writing criteria that describe the branch you liked.
- **Halo scoring.** Score by criterion across branches, not branch by branch.
- **Frankenstein merges.** Combining incompatible elements because both scored
  well. Apply the separability and compatibility tests.
