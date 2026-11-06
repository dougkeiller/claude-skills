# Comparing third-party options (plugins, tools, vendors)

Use with the Research bullet in SKILL.md. The steps run in order; each pitfall states the mechanism so you can apply it to a case this file does not cover.

## Procedure

1. **Get the long-list from the machine-readable source, not the rendered page.** Documentation pages are often client-rendered, so a plain fetch returns only navigation. Look for the JSON feed the page reads from, and save it to a file in the scratch directory.
2. **Save every intermediate to a file.** Python variables do not reliably survive between separate code-execution calls, so a later call can fail with NameError on data an earlier call built. Write the list, then the filtered list, to JSON or CSV and re-read them.
3. **Tag the long-list with cheap rules** (category, keywords in the description, capability fields). Mark these tags as approximate in the output, because keyword matches miss and over-match.
4. **Pull the ranking metric the user named, from the source the user named.** For GitHub stars, read the repo the catalog links (`gh api repos/<owner>/<repo> --jq .stargazers_count`). If the linked repo is a small integration and the product repo is large, show both numbers and ask which one counts before dispatching.
5. **Run exactly N.** The baseline (the option already in use) is scored with the same rubric but sits outside the N. Do not add or drop candidates to make a list look balanced without saying so.
6. **Sanity-check popularity.** Stars, forks, age, contributor count and last push together tell you more than stars alone. Flag a repo whose star count looks out of line with those.
7. **Fix the rubric before research starts.** Criteria, a 1–5 anchor for each score, and weights go to the user for approval. Scoring against a rubric written afterwards lets the weights follow the answer.
8. **Dispatch research with one shared brief.** Each subagent gets the same brief: read-only (no installs, config changes or enabling anything), the permitted search engines, a source URL for every claim, UNVERIFIED for anything it could not check, and the rubric. Add the candidate's name, repo and catalog text as its own task. Ask for a JSON output schema so the results can be merged in code.
9. **Merge in code, then test the weights.** Compute weighted totals with a script. Rerun with two or three alternative weight sets and report whether the top pick changes. A pick that survives only one weight set is a finding to report.
10. **Report one pick.** Give the trade-offs, the assumptions it rests on, what would change the recommendation, and the list of unverified claims.

## Pitfalls

- **Silent scope change.** Substituting a different repo, metric or count makes the result answer a question the user did not ask. Show the substitution and ask first.
- **Recall used as a filter.** A claim like "has a Claude Code integration" from memory can drop a candidate that does have one. Verify it, or mark it as recall before it filters anything.
- **Star counts used as quality.** Stars measure attention and can be inflated or belong to a sibling product in the same repo. Use them as one input among several.
- **Subagent self-reports.** A child saying it checked something is a claim, not a check. Spot-check the top two or three claims against the source before the report goes out.
- **Overfitting the rubric.** Weights chosen after seeing scores will favour the leader. Fix them first (step 7) and only test them afterwards (step 9).
