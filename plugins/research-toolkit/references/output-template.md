# Output — the dated working note

Every research run that goes past a Lookup ends in a Markdown note in the user's
PKM folder: `YYYY-MM-DD-<topic>.md`, flat in the vault root, frontmatter tags
rather than folders. Never overwrite an existing note — version it (`-v2`).
Exec-brief register: conclusions first, prose over bullet walls, minimal
jargon, MECE. Bullets only where structure genuinely helps.

```markdown
---
date: YYYY-MM-DD
source: claude-cowork-session
tags: [research, <workstream>, <topic>]
status: <long-list | scored | verified | watchlist>
---

# <Question, as one line>

**Conclusion.** Two to four sentences. What the evidence supports, how strongly,
and what it turns on. If the run stopped at the long-list or the scored cut,
say so here: the conclusion is that these N candidates map the space, and
nothing has been verified.

## Scored cut           <!-- after the first stop -->

The criteria and weights as the user set them, then the full scoring table —
every long-list row, one column per criterion, the weighted total, unknowns
marked unknown — the ranking, the sensitivity result, and the approved cut
line. If Verify later moved a ranking, say which and why.

## Finalists            <!-- Pass 2 only -->

One section per finalist the user picked. Each consequential figure quoted as
written, with its URL beside it and how it was read (page text via fetch /
summarised by a tool / recalled). Where sources disagree, both figures, and
which is trusted and why. Anything unverified marked unverified, in the prose,
never left sitting in a table looking checked.

## Long-list            <!-- appendix; keep rejected options visible -->

1. **Name** — one line on what it is; one line on why it might qualify; source
   link; quality note.
2. ...

Excluded: <what was left out and on what grounds>.

## What could not be verified, and why

## What would change the conclusion

## Sources consulted

Which surfaces ran (Exa categories, Deep Search, agent run with providers,
domain connectors, browser) and what each contributed. Absence of evidence
from a source that should have had it, stated as a finding. No cost section:
connector-class calls are not reported. A scheduled monitor's recurring price
is noted once, in the watchlist note that created it.
```

Two rules about the note that are easy to lose:

- **The long-list and the scoring table stay in the note after Pass 2.**
  Rejected options and the weights that rejected them are part of the answer;
  a reader who sees only the winner cannot judge the choice.
- **A watchlist run writes a short note too**: what is new since the last run,
  one line per item with URL, or "nothing new since <date>" — which is a real
  result, not an empty section.
