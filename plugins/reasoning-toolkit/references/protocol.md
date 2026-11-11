# Shared protocol for the reasoning toolkit

Every skill in this toolkit follows the same three rules. Read this once per
session; it applies to all eight.

## Rule 1 — The working note is the stage gate

Each run writes a Markdown working note, and each stage is appended to that
note **before** the next stage begins. The file is not documentation produced
at the end; it is the mechanism that makes skipping a stage visible.

### Where it goes

Working notes belong in **the folder for the workstream the question is
about**, in a `reasoning-notes/` subfolder — a pre-mortem on a client deal
goes to that client's folder, a decision matrix for a venture to the venture's
folder.

Determine the workstream from the subject of the question, not from whichever
folder happens to be connected. Then:

- **Workstream is clear and its folder is connected** → write there.
- **Workstream is clear but its folder is not connected** → request access to
  that folder before starting, naming why.
- **Workstream is unclear, or the question spans several** → ask which folder,
  once. If working unattended, write to the session workspace, say so plainly
  at the top of the response, and do not guess a folder.
- **No folders connected at all** → session workspace, delivered as a file.

Never default a working note into a personal knowledge vault or archive folder.
Archives hold material deliberately kept; a working note is workspace output and
only earns a place in an archive if the user decides it has.

### Filename

`YYYY-MM-DD-<short-slug>-<tool>.md` — kebab-case, no colons, slashes, question
marks, quotes, or trailing spaces or dots. Many sync clients reject those.

Never overwrite an existing note. If the filename is taken, version it:
`...-v2.md`.

### Frontmatter and header

```markdown
---
date: YYYY-MM-DD
source: claude-session
tags: [<workstream>, <tool>]
status: draft
---

# <Tool name> — <one-line subject>
Question as posed: <the user's own words, verbatim, not paraphrased>
Status: in progress | complete
```

Set `status: verified` only where the findings have actually been checked
against sources. Flag unverified facts inline, and give any time-sensitive
figure an as-of date.

Never rewrite the "Question as posed" line once set. Several tools compare the
closing framing against it, and a tidied-up version destroys that comparison.

## Rule 2 — Independence is spawned, not simulated

When a tool calls for multiple perspectives, branches, or critics, spawn a
separate subagent for each one via the Agent tool, in a single message so they
run concurrently. Do not write several viewpoints in sequence in one context
and call them independent — a single context contaminates every viewpoint after
the first, which is the exact failure these tools exist to prevent.

Give each subagent only the frame it needs. Do not tell it what the other
subagents were asked, what the expected answer is, or what the user prefers.

If the Agent tool is unavailable, say so plainly in the working note and in the
response, then run the perspectives sequentially with an explicit instruction to
each not to reference the previous ones. Flag the result as lower-confidence.
Never silently downgrade.

## Rule 3 — Refuse the generic

Every one of these tools fails the same way: by producing plausible,
well-organised, generic output. "Execution risk." "Stakeholder alignment."
"Market conditions may change." These are shapes of answers, not answers.

Apply this test to every finding before it goes in the note: **could this
sentence appear unchanged in an analysis of a completely different decision?**
If yes, it is filler. Either make it specific to this situation — name the
actor, the number, the date, the mechanism — or cut it.

A short specific output beats a long generic one, every time.

## On stopping

If the user's question turns out to be underspecified in a way that makes the
tool meaningless (a decision matrix with one option, a post-mortem on something
that has not concluded), say so and stop. Do not manufacture inputs to keep the
machinery turning.
