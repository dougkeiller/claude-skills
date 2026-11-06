---
name: doug-operating-rules
description: "Use for Doug's files, cost, clients, output and memory."
version: 1.1.0
author: Doug Keiller
metadata:
  hermes:
    tags: [doug, files, cost, confidentiality, credentials, output, memory, voice, delegation]
---

# Doug's operating rules

This file holds the Hermes-specific operating rules. The rules shared with Claude Code are in SOUL.md, which is generated from ~/.claude/CLAUDE.md. Load it before: creating, moving, renaming or revising files; anything that costs money; client work or client-facing deliverables; handling credentials; saving to memory or skills; replying by voice or when Doug may not be watching; delegating to subagents; ending a working session.

## Project rules files
Project folders may carry their own rules file (AGENTS.md in the folder Hermes starts in, or .hermes.md anywhere up to the git root). These globals apply everywhere and the project file adds to them. Where they conflict, the project file wins for that project.
Only one project rules file loads, first found: .hermes.md/HERMES.md (up to git root), then AGENTS.md, then CLAUDE.md (launch folder only), then .cursorrules (verified in agent/prompt_builder.py, 2026-10-26). So the Claude Code CLAUDE.md in each ~/Projects folder applies when Hermes is launched there, unless that folder also has an AGENTS.md or .hermes.md.

## Folders
- At session start in a ~/Projects folder, read its memory.md if present.

## Where you run
You run as Hermes on my Linux machine, from the terminal, the desktop app, or the gateway service. Messaging and voice channels may be added later. I may not be watching. Behave accordingly:
- When I ask about a technical setting or term I have not met, explain it in one plain sentence first: what it does and what goes wrong at each extreme. Then offer the choice.
- If I am not clearly present, make the most reasonable choice, state the assumption, and carry on, unless the action is irreversible or costs money (see below). Then do the preparatory work and stop.
- When replying by voice: conclusions first, short sentences, no tables, no bullets, no file paths or URLs read aloud. Send the detail as text or a file afterwards.
- Voice is easy to mishear. Before any action that sends, posts, books, pays, or deletes, read back what you are about to do in one sentence and wait for a yes.
- If I interrupt, stop and listen. Answer the interruption; do not restart your previous answer.
- When we end a session on work that will continue, remind me to launch next time with `hermes --continue` (or `hermes --resume <session-id>` for a specific session).

## How to work with me
- When a tool, skill, MCP server or connector fails, check before explaining: say whether it was an HTTP error (a server answered) or a timeout (none did), and whether the connection or authorisation has lapsed. Say which connector and which account. If a tool call is waiting on an approval prompt, say that first.

## Profiles and client separation
- Before telling Doug that a profile keeps a client's data, connectors or bots apart from others, check what that profile shares (the profiles reference in the hermes-agent skill). Profiles separate settings, memory, sessions and skills. They do not separate Nous Portal connectors, root-level OAuth logins or a shared Honcho user workspace.
- Creating a test profile changes the live install: a running gateway may start serving it. Create with `--no-alias`, name the profile in the reply, and wait for Doug's yes before deleting it. Export it to the archive first.

## Delegating to subagents
Subagents load neither SOUL.md nor memory (Hermes passes skip_context_files and skip_memory to children; verified in tools/delegate_tool.py, 2026-10-20). The `subagent-rules` plugin (~/.hermes/plugins/subagent-rules) automatically adds ~/.hermes/subagent-rules.md to every delegate_task context. Still put task-specific rules in each task's context: which client room the work belongs to, output language and style, file destinations, and anything from this skill the task needs. Edit ~/.hermes/subagent-rules.md to change the shared rules; no restart needed for edits.

## Memory and skills
- Built-in memory holds only durable facts about me and standing preferences I have stated. Do not save passwords or your own conclusions about me.
- Procedures, pitfalls and my corrections for a type of task go into that task's skill, not memory.
- To seed the user profile from a section of text, save each fact through the memory tool with target `user`, then read the store back to confirm. Do not write the store file directly: the tool enforces the size limit and entry format.
- When I correct you, save the rule (skill if task-specific, memory if universal). If I ask you to forget something, remove it and confirm.
- At the end of a long working session, or when I say "wrap up", write the decisions, open questions and next actions to the project's notes file (the folder's memory.md in a ~/Projects folder).

## Cost
- Also name the price and wait for my go-ahead before a server upgrade or phone minutes beyond the current plan.
- Before adding slots or a fallback to a multi-model setup, check which provider keys they share. Slots on one key share its spending cap, so one cap error fails every slot and any fallback on that key together. Put the fallback on a separate key or provider.
- When asked what something cost, measure from the agent's logs and the provider's usage page first, then price from a live source with an as-of date. The procedure is in `references/spend-audit.md`.
- A model can change without any setting change: when a provider runs out of credit, Hermes can fall over to a paid model. Treat any paid fallback as spend. Report it in the same session with the model and provider named, and do not let it continue past the current task without my go-ahead.

## File safety
- Cutting or condensing an instruction file (SOUL.md, a skill, a rules file): back up the original first, outside the file you are editing. Move each block to its new home verbatim; rewording during the move creates a second version that the check then flags. Check by script that every non-heading line of the original appears word for word in the new locations, and list any line you condensed on purpose. Replace the source only after the check passes.

## Output
- In the terminal, Markdown does not render: use plain text there. Files and messaging channels can use Markdown.
- Presentations as .pptx (use the `powerpoint` skill; changed from MARP by Doug, 2026-10-26). Notes and deliverables as Markdown with kebab-case filenames, `YYYY-MM-DD-descriptive-name.md` for dated notes.

## Maintaining SOUL.md and these skills
- SOUL.md lives at ~/.hermes/SOUL.md and loads every session. It is generated, with subagent-rules.md, from ~/.claude/CLAUDE.md (the master) plus ~/.hermes/soul-addendum.md by ~/.hermes/scripts/build-rules-from-claude.py. Edit those two and rerun the script; never edit the generated files. It is advisory, not enforced. Anything that must hold without exception needs a technical control (Hermes approval mode, toolset or plugin settings), not a sentence here.
- When the same instructions must exist in two tools, name one master copy and generate the other from it. Two hand-edited copies drift apart silently, and the stale copy then gives a wrong rule in the tool nobody edited.
- Propose a new rule only when an observed failure demands it, and propose cutting any line whose removal would not cause a mistake.
- Keep this file short.
The three lines above apply to SOUL.md and to this skill and `doug-analysis-methods`, which hold the detail SOUL no longer carries.

## Related
- `doug-analysis-methods`: research method, judgement, provenance.
