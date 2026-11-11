# Reasoning Toolkit

Eight reasoning methods, available as skills. Claude picks the right one from
what you say — you do not have to name the tool.

## The eight

**Break a stuck loop**

| Skill | What it does |
|---|---|
| Structured Reflection | Asks questions instead of answering, until the problem gets re-framed. For when you're going in circles. |
| Chain of Thought | Forces each step to quote the prior step's output, so nothing gets silently bridged. |
| Graph of Thought | Branches into genuinely different approaches, scores against a rubric fixed in advance, merges the best elements. |
| Context Switcher | Every stakeholder's view, each developed by a separate agent that cannot see the others. |

**Pressure-test a decision**

| Skill | What it does |
|---|---|
| Decision Matrix | Weighted scoring plus real sensitivity analysis — would the answer change if the numbers were somewhat different? |
| Devil's Advocate | Six independent adversaries plus a Klein pre-mortem, hunting the failure optimism is hiding. |
| Formal Logic | Runs Z3. Returns a verdict and, when an argument fails, a concrete counterexample. |
| Hindsight | A post-mortem where a cold reader judges the decision without ever being told the outcome. |

## What makes these different from prompt templates

Three things do actual work rather than describing it:

**Independence is spawned, not simulated.** Where a method calls for multiple
perspectives — stakeholders, adversaries, approach branches — each one runs as a
separate subagent that cannot see the others. Writing six viewpoints in one pass
produces one viewpoint wearing six hats; this avoids that by construction.

**Two methods run real computation.** Formal Logic calls Z3 and returns an
actual satisfying assignment where the premises hold and the conclusion fails.
Decision Matrix runs drop-one analysis, weight-flip thresholds, and a
20,000-draw Monte Carlo over weights and scores. Neither is Claude's impression
of rigour; both are arithmetic.

**Every run leaves a working note.** Each stage is written to a dated Markdown
file before the next begins, which is also what makes skipping a stage visible.

## Working notes

Runs write to `reasoning-notes/YYYY-MM-DD-<subject>-<tool>.md` inside **the
folder for the workstream the question is about** — a pre-mortem on a client
deal lands in that client's folder, not in a general notes pile. If the
workstream is unclear or its folder is not connected, the skill asks rather
than guessing; with nobody there to ask, it writes to the session workspace and
says so.

Notes carry YAML frontmatter (`date`, `source: claude-session`, `tags`,
`status`) and Drive-safe kebab-case filenames. Existing notes are never
overwritten — a clash gets versioned to `-v2`.

Archive and personal-knowledge folders are excluded by default: a working note
is workspace output, and only earns a place in an archive if you decide it has.

## Requirements

Formal Logic needs `z3-solver`; Decision Matrix needs `numpy`. Both install on
first use if missing:

```bash
pip install z3-solver numpy --break-system-packages
```

The rest run anywhere. Methods that use subagents degrade gracefully if the
Agent tool is unavailable — they say so and flag the lower confidence rather
than pretending.

## Origin

Modelled on the eight tools at reasoning.services, rebuilt as local skills.
