---
name: formal-logic
description: >
  Check whether an argument's conclusion actually follows from its premises,
  using a real solver that returns a verdict plus a concrete counterexample
  rather than an opinion. Use on any argument whose validity carries
  consequences: eligibility and qualification rules, contract and policy logic,
  compliance determinations, "if X then we must Y" reasoning, scheduling and
  ordering constraints, board or investment cases, anything where a conclusion
  is being presented as forced by the facts. Also use when two people apply the
  same rules and reach different answers, or when a conclusion feels wrong but
  the argument sounds airtight. Trigger on "does this follow", "is this
  argument valid", "check the logic", "prove this", "these rules seem to
  contradict", "does the policy actually say that", "am I entitled to", "is
  this reasoning sound", "find the flaw in this argument".
---

# Formal Logic

Arguments that sound airtight often are not, and the gap is usually invisible in
prose. This skill translates the argument into logic, runs Z3, and returns
either a proof of validity or a **witness** — an explicit assignment where every
premise is true and the conclusion is still false. A witness ends the argument
in a way that "I don't find that convincing" never does.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

**Scope, stated up front and repeated to the user:** this tests whether the
conclusion follows *from the stated premises*. It says nothing about whether
the premises are true. A valid argument from false premises proves nothing, and
the most common real-world failure is a true conclusion drawn from premises
that do not support it.

## Stage 1 — Extract the argument

Write the argument into the note as given, then separate it:

- **Premises** — what is being asserted as given.
- **Conclusion** — the single claim said to follow.
- **Hidden premises** — steps the argument uses but never states. Nearly every
  real argument has these, and they are usually where the flaw lives. Surface
  them explicitly and confirm with the user, because adding a hidden premise
  can turn an invalid argument valid, and that is itself the finding: "this
  works only if you also accept X."

If there is no clear conclusion, or the "argument" is a set of considerations
rather than a derivation, say so and stop. Not everything is an entailment.

## Stage 2 — Build the dictionary

Declare a variable for every distinct claim or quantity, each with a
plain-English label. The engine refuses to run without labels, deliberately:
the translation is the part a human must check, and an unlabelled variable
cannot be checked.

Types: `bool` for true/false claims, `int` or `real` for quantities, thresholds,
counts, and timing.

Watch for the two translation errors that quietly change the argument:

- **Splitting what should be one variable**, or merging what should be two. If
  "the pilot succeeds" means something different in the premise and the
  conclusion, that equivocation is the actual flaw — and formalising it exposes
  it, because you will be forced to choose one meaning.
- **Turning "if" into "if and only if".** Policies say "eligible if you meet
  A"; people reason as though failing A proves ineligibility. If the source
  really is biconditional, use `==` and say so.

For ordering and timing, integers work well: `t_approval < t_start` for "approval
must precede start."

## Stage 3 — Run the engine

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/entail.py spec.json
```

```json
{
  "claim": "One-line English statement of what is being tested",
  "vars": {"pilot_works": "bool", "scale": "bool", "cost_k": "int"},
  "labels": {"pilot_works": "The pilot hits its retention target",
             "scale": "We roll out to all sites",
             "cost_k": "Integration cost, $k"},
  "premises": [
    {"id": "P1", "text": "If the pilot hits retention, we roll out",
     "expr": "Implies(pilot_works, scale)"},
    {"id": "P2", "text": "The pilot hit retention", "expr": "pilot_works"}
  ],
  "conclusion": {"text": "We roll out to all sites", "expr": "scale"}
}
```

Expressions are Z3 Python: `And`, `Or`, `Not`, `Implies`, `Xor`, `If`,
`Distinct`, and `== != < <= > >= + - *`.

The engine reports four things: whether the premises are even consistent with
each other, whether they entail the conclusion, a witness if they do not,
whether they entail the *opposite*, and — when valid — which premises are
load-bearing versus decorative.

Paste the full output into the note.

## Stage 4 — Interpret honestly

**Premises inconsistent.** Stop here. Contradictory premises entail everything,
so the entailment result would be meaningless. The finding is the contradiction,
and the engine names the smallest contradicting set. This is common in policy
and contract work and is usually the most valuable thing the tool finds.

**Not entailed.** Walk the user through the witness in plain English: here is a
world where everything you asserted holds and your conclusion is still false.
Then say what premise would have to be added to close it — and whether that
premise is one they would actually endorse. Often they will, and the real
finding is that the argument depends on something unstated.

**Entailed.** Say clearly that this is validity, not truth, and turn attention
to the premises. If the engine flagged a premise as decorative, mention it —
it usually means someone included a fact that felt supportive but does no work.

**Entails the opposite.** Rare and worth flagging loudly.

## Stage 5 — Deliver

Verdict first, in one sentence. Then the witness in English if there is one.
Then the dictionary, so the translation can be checked — always include this,
because a verdict on a mis-formalisation is worse than no verdict.

Finally, and required: **what the formalisation left out.** Most real arguments
carry force that logic does not capture — probability, degree, cost,
reasonableness. If the argument's real weight lives there, say so plainly
rather than letting a clean verdict overstate what was tested.

## Failure modes

- **Verdict without dictionary.** Unfalsifiable by the reader. Always show it.
- **Formalising a conclusion into the premises.** Then everything is trivially
  valid. Check that no premise restates the conclusion.
- **Validity mistaken for truth.** State the distinction every time.
- **Over-formalising.** Arguments that are really about magnitude or judgement
  do not belong here. Say so instead of forcing them.
- **Ignoring the consistency check.** Running entailment on contradictory
  premises produces a meaningless "valid."
