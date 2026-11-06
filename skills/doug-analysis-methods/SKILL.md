---
name: doug-analysis-methods
description: "Use for Doug's research, decisions, figures and reviews."
version: 1.1.0
author: Doug Keiller
metadata:
  hermes:
    tags: [doug, research, decisions, judgement, provenance, methods]
---

# Doug's analysis methods

This file holds the research methods and the Hermes-specific provenance rules. The judgement and provenance rules shared with Claude Code are in SOUL.md, which is generated from ~/.claude/CLAUDE.md. Load it for any research beyond a single lookup, any recommendation or decision, any figure Doug will act on, document reviews, and venture or product ideas.

## Methods
If an installed Hermes skill covers one of these, load it and say so in one line. If not, say so in one line and apply the method briefly by hand. When a method works well and will recur, offer to save it as a skill.
- Research beyond a single lookup: wide enumerated long-list first, stop. I set criteria and weights; you score and rank every candidate and show the scoring; I approve the cut; only then deep, cited verification on survivors. Never pick finalists by eye. Parallel subagents are fine for the verification stage. Once I approve a cut, run exactly the N I named, using the metric and source I named. If a substitution looks better (a different repo, a different metric), show it and ask before dispatching; never swap silently. Keep an incumbent baseline separate from the N. See `references/option-comparison-procedure.md`.
- Best-practice questions ("what do people do", "best practice for X"): search with both Exa and Perplexity, then report where they agree and where they differ, with a link to each source. Check the load-bearing claims against the vendor's primary docs (fetch the page or its `index.md` / `llms-full.txt` and grep it). Practitioner posts and issue threads describe failure modes that happened to someone; they are not base rates. Label them as dated reports and reproduce one before relying on it.
- Choosing between named options: weighted scoring plus a check that the answer survives different weights. Compare options only within the same layer. An agent that runs tools, a gateway or router that passes model calls through, and a model host are different products, so a score across layers answers no real question. Check each option against this machine (does the tool accept it, does the account allow it) before recommending it.
- Integration questions ("can X connect to Y"): separate "no native integration" from "connectable through a generic config path". Before answering no, read the tool's custom-provider or base-URL docs, because a closed feature request means only that the vendor declined to build a dedicated integration. Report both halves, with the config path as the answer if one exists.
- Irreversible commitments: pre-mortem from several adversarial angles.
- Several defensible approaches: explore them separately, score against a rubric fixed in advance, then merge.
- Any figure or derivation I will act on: show each step, each consuming the prior one.
- Anything landing on people who were not in the room: write each stakeholder's view independently, then note real conflicts.
- Eligibility, contract or policy rules: check whether the conclusion actually follows from the premises.
- Repeatable AI or unattended workflows (anything that runs without me watching, or that I will rely on): build a golden set before relying on it. A golden set is an answer key: real inputs with expected outputs written from the primary source before the run. Run it, report pass or fail per case, and say what it does not test. When a case fails, check the source text before changing the expected answer, and say which side was wrong. Explain the term to Doug in one plain sentence the first time it comes up.
- Post-mortems: separate decision quality from outcome.

## Facts and provenance
- Mark every unverified number inline, and every capability or membership claim made from recall (e.g. "X has a Claude Code integration"). Those claims are often used as filters, so an unmarked one silently keeps or drops candidates.
- Time-sensitive facts carry an as-of date. Memory and saved notes are dated snapshots; re-verify before I act on them. For the live setup (default model, presets, providers, keys), read the config or CLI output rather than memory, because a snapshot can describe a setup that has since changed.
- Cite a source only for something you opened in this session. Never write a commit SHA, file path, line number, or "confirmed in the source" into a note unless you read it in that session. A remembered or inferred detail presented as a citation looks checked and is not; say "recall" or "inference" in the sentence where it sits.
- Treat factual claims in another agent's or tool's report as recall until you check them against the live system (config, files, CLI output). That agent reads files, not your live state, so its claims about this machine are inferences. Check each claim by name and report which held and which did not, because a report can be right on judgement and wrong on facts.

## Related
- `doug-operating-rules`: files, cost, clients, credentials, output, memory, voice.
- `grounded-citations`, `shortlist-research`: tooling for the research method above.
- `references/option-comparison-procedure.md`: steps and pitfalls for comparing third-party options (catalog long-lists, star counts, subagent scoring).
- Web search: Exa or Perplexity only.
