---
name: chain-of-thought
description: >
  Force a conclusion through explicit linked steps where each step must consume
  a named prior output, so nothing can be skipped, assumed, or quietly bridged.
  Use for any multi-step derivation where a wrong intermediate step poisons
  everything after it: financial models, eligibility and qualification logic,
  root-cause traces, sizing and unit-economics builds, migration sequences,
  legal or regulatory chains, "how did we get to this number" questions. Also
  use when a conclusion feels right but nobody can reconstruct how it was
  reached, or when two people work the same problem and get different answers.
  Trigger on "walk me through", "show your work", "how did we get to that
  number", "step by step", "prove out", "does this actually follow", "trace
  this back", "reconstruct how".
---

# Chain of Thought

Ordinary step-by-step reasoning fails silently: step 4 quietly assumes something
step 3 never established, and because the prose flows nicely nobody notices. The
fix is mechanical. Every step must declare which prior output it consumes and
quote it. A step that cannot quote its input is a broken link, and a broken link
means the conclusion is unsupported no matter how good it sounds.

Read `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` first.

## Stage 1 — Write the contract before deriving anything

Open the working note and lay out the chain **before** doing any of the work.
Naming the steps in advance is what stops you from working backwards from a
conclusion you have already decided on.

For each step record: number, what it establishes, and which prior step numbers
it consumes (`S0` = the given inputs).

```markdown
## Chain contract
| # | Establishes | Consumes |
|---|-------------|----------|
| 1 | Addressable clinics in the three pilot states | S0 |
| 2 | Share running an EHR we integrate with        | 1 |
| 3 | Reachable clinics                             | 1, 2 |
```

Then check the contract itself:

- **Every step consumes something.** A step consuming nothing is either an
  assumption in disguise (label it, and say where the value comes from) or it
  belongs in S0.
- **Nothing consumes a later step.** Circular chains prove themselves.
- **The final step consumes the chain.** If the last step could be reached
  directly from S0, everything in between is decoration.

## Stage 2 — Execute one link at a time

One step per block, in order. Never two at once. Each step must be written in
this shape:

```markdown
### Step 3 — Reachable clinics
Consumes: Step 1 → "4,180 clinics across the three states"
          Step 2 → "61% run Epic or athenahealth"
Operation: 4,180 x 0.61
Output:   2,550 reachable clinics
Confidence: derived arithmetic; inherits Step 2's survey uncertainty (+/-8pts)
```

Non-negotiable: **quote the consumed output**, do not reference it by number
alone. Quoting is what makes a mismatch visible — you cannot quote a number that
was never established.

When you cannot quote an input because it does not exist:

> **BROKEN LINK at Step 3.** Requires the EHR share from Step 2; Step 2 produced
> a range, not a share. Options: (a) go back and settle Step 2, (b) carry the
> range through and widen every downstream figure, (c) declare an assumption and
> mark the chain conditional on it.

Stop and resolve it. Do not bridge the gap with a plausible number, and do not
carry on and mention it at the end.

Append each completed step to the note before starting the next.

## Stage 3 — Audit the chain

Three checks, all recorded in the note.

**Link audit.** Walk the chain and confirm every declared input was actually
produced upstream, with matching values. Values drift between where they are
established and where they are used; this is where you catch it.

**Decorative-step test.** For each step: delete it and ask whether the
conclusion still holds. If it does, that step was never load-bearing. Say so
explicitly. A chain of nine steps where three are decorative is really a chain
of six, and pretending otherwise inflates confidence.

**Weakest-link statement.** Confidence in the conclusion is the confidence of
the weakest load-bearing step, not the average. Name that step, and say what it
would take to firm it up. A chain with one guessed input and eight solid
derivations is a guess.

## Stage 4 — Deliver

Lead with the conclusion and the weakest link in the same breath — "2,550
reachable clinics, and the whole figure moves with the EHR share in Step 2,
which is a vendor estimate we have not verified." Then the chain in brief.

## Failure modes

- **Backwards derivation.** Deciding the answer, then building steps toward it.
  The Stage 1 contract exists to prevent this; write it first, genuinely.
- **Reference without quotation.** "From step 2, we get..." — quote it or the
  drift goes unnoticed.
- **Silent bridging.** Filling a missing input with a reasonable-sounding number
  rather than declaring a broken link. This is the failure that makes the whole
  exercise worthless.
- **Padding.** Adding steps to look rigorous. The decorative-step test catches
  this; run it honestly.
- **Averaged confidence.** Nine strong steps and one weak one is a weak chain.
