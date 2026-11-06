---
name: shortlist-research
description: Semi-automated cost-effective MECE research — take a big option space down to an adversarially-verified shortlist. Breadth on flat-rate Gemini Deep Research (run manually by the user), scoring on Fable, verification on Perplexity + one Opus skeptic pass, synthesis on Fable. Use when the user wants to research a large set of options (programs, vendors, schools, tools, places) down to a ranked, fact-checked shortlist without the cost of a full multi-agent workflow. Keeps the user in the loop for taxonomy design and the finalist cut.
metadata:
  author: built-for-doug
  version: "1.0"
---

# /shortlist-research — cost-effective MECE shortlisting

This skill runs Doug's standing research playbook (see memory `feedback_research_cost_effective_pipeline`). The design principle: **flat-rate/cheap models touch the whole funnel; premium models (Opus) touch only the finalists.** Two human-judgment steps are deliberate, not gaps — do not automate them away.

Run it as a **two-pass, human-in-the-loop** procedure. Pass 1 goes through discovery + scoring and STOPS for Doug's cut. Pass 2 verifies + synthesizes. If invoked when a working folder already exists, detect which phase is next from the files present and resume there.

## Working folder

Create/use `~/shortlist_research/<short-topic-slug>/` with:
- `brief.md` — question, profile, taxonomy grid, rubric, shortlist size (written in Phase 1)
- `discovery_prompts.md` — the per-cell Gemini prompts you generate for Doug
- `discovery/<cell-slug>.md` — one file per cell; **Doug pastes Gemini Deep Research output here**
- `scored_longlist.md` + `scored_longlist.json` — Phase 3 output
- `FINALISTS.md` — the final report (Phase 6)

---

## Phase 1 — Scope + taxonomy (interactive; ~free)

Work with Doug in the main session. Do NOT spawn agents here. Establish and write to `brief.md`:
1. **The decision question**, sharpened.
2. **Profile / constraints** — the "who is this for / what matters" context that every downstream agent needs.
3. **The MECE taxonomy grid** — the mutually-exclusive, collectively-exhaustive cells to sweep (e.g. `type × region × cost-band`). This grid IS the coverage guarantee. Propose one; get Doug's sign-off.
4. **The scoring rubric** — weighted criteria (state weights explicitly), scored 0–100.
5. **Shortlist size** — how many finalists to end on (default ~8), and the longlist cut size (default top ~24).

If any of these is underspecified, ask before proceeding — this phase determines quality.

## Phase 2 — Discovery (Gemini Deep Research, run by Doug; flat-rate)

**Option A — Gemini is manual (this skill's design).** Generate one **Gemini Deep Research prompt per cell**, self-contained (each restates the profile + exactly what to find + "return a structured list with name, what it is, cost, location, dates, eligibility, and source links"). Write them all to `discovery_prompts.md`, numbered by cell.

**Do NOT name example candidate options in discovery prompts** (no "e.g. Amherst, Swarthmore, …"). Naming anchors the model and biases the sweep toward those names — discovery's whole job is to surface the candidates. State the criteria only. Rare exception: when you're *deliberately* re-running to confirm coverage of a specific known-eligible set the prior sweep may have missed — and even then, prefer describing the category over naming instances.

Then STOP and tell Doug, explicitly:
> Run each prompt in the Gemini app's **Deep Research** mode (this is the flat-rate lever), and save each result as `~/shortlist_research/<slug>/discovery/<cell-slug>.md`. Tell me when done (or say which cells you finished).

Do not proceed until discovery files exist. This is a real pause — end the turn.

## Phase 3 — Extract + score → longlist (Workflow; Fable only)

When `discovery/*.md` files are present:
1. Read every `discovery/*.md` file yourself (main session does the file I/O — workflow scripts can't read files).
2. Invoke the bundled scoring workflow:
   `Workflow({ scriptPath: "/home/doug/.claude/skills/shortlist-research/workflow_score.js", args: { docs: [{cell, text}, ...], rubric, profile, topN } })`
   - `docs` = one entry per discovery file (`cell` = the filename/segment, `text` = its full contents).
   - `rubric`, `profile` from `brief.md`; `topN` = the longlist cut size (~24).
   - The workflow caps extraction at 8 Fable agents, dedupes by name, and returns `{ total_unique, longlist }`.
3. Write the ranked longlist to `scored_longlist.md` (a table) and `scored_longlist.json`.

## Phase 4 — Human cut (interactive)

Present the ~24 ranked candidates to Doug as a compact table (name, key facts, score, one-line rationale). Ask him to pick the finalists to verify (~10–15). **This is his call — do not pre-cut for him beyond surfacing the ranking.** Wait for his selection. End the turn if he needs time.

## Phase 5 — Verify + Phase 6 — Synthesize (Workflow; Perplexity + one Opus pass + Fable)

When Doug gives his finalist picks:
1. Invoke the bundled verify workflow:
   `Workflow({ scriptPath: "/home/doug/.claude/skills/shortlist-research/workflow_verify.js", args: { finalists: [{name, claims}, ...], profile, rubric } })`
   - `finalists` = his picks; `claims` = the key facts from the longlist to fact-check (leave blank to have the agent establish them).
   - The workflow: Perplexity-grounded fact-check per finalist (Fable + `general-purpose` agent so it can reach the Perplexity MCP) → **one batched Opus adversarial skeptic pass** over all finalists → Fable-written ranked report. Returns `{ report, finalists }`.
2. Write `report` to `FINALISTS.md`. Summarize the ranked result + each finalist's "confirm in writing" open questions for Doug in the chat.

---

## Cost-control rules (enforce these)

- **Never** run the full expensive multi-agent Workflow style over the whole funnel. Discovery is flat-rate Gemini; scoring/verify/synthesis are Fable; only the single batched skeptic pass is Opus.
- Keep extraction ≤ 8 agents (the script enforces this).
- Output schemas are capped (word/array limits) — keep them that way; verbose agents cost twice.
- Checkpoint every phase to files so a failure never re-runs an earlier phase. To rerun a workflow after an edit, prefer `Workflow({ scriptPath, resumeFromRunId })`.
- One Opus skeptic call covers all finalists together (shared context/caching) — do not split into per-finalist Opus calls unless Doug wants independent verdicts.

## Notes
- Gemini "Deep Research" is an app feature, not an API — that's why Phase 2 is manual. It's the flat-rate cost lever; keep it manual by default.
- Perplexity `perplexity_research` is web-grounded + cited — the right tool for finalist fact-checks.
- If Doug wants full hands-off discovery later, the alternative is browser-driving Gemini via Playwright MCP (fragile) or the metered Gemini/Vertex API (loses flat-rate).
