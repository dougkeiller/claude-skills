# claude-skills

Claude Code skills written for Doug Keiller.

- `skills/shortlist-research` — semi-automated, cost-effective research from a big option space to an adversarially verified shortlist.
- `skills/daily-project-sync` — scheduled task that aligns ~/Projects folders with Todoist and Cowork projects (additive creates only).

- `skills/doug-analysis-methods` — research methods, judgement and provenance rules (Hermes version).
- `skills/doug-operating-rules` — file, cost, confidentiality, output and memory rules (Hermes version).

## Plugins

- `plugins/research-toolkit` (v1.3.0): one research entry point with six modes (Lookup, Sweep, Verify, Enumerate, Deep, Watch) on Exa, with human stops between the long-list, the scored cut and verification. Needs your own Exa key in `EXA_API_KEY`; monitors need `EXA_MONITOR_WEBHOOK`.
- `plugins/reasoning-toolkit` (v0.2.0): eight decision skills (decision-matrix with real sensitivity analysis, devils-advocate pre-mortem, graph-of-thought, chain-of-thought, context-switcher, formal-logic, hindsight, structured-reflection).

These are public copies of the installed plugins. Client and personal examples are replaced with generic ones; credentials and backups are excluded.

Install by copying a folder into `~/.claude/skills/` (daily-project-sync lives in `~/.claude/scheduled-tasks/`).
