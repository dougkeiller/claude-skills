#!/usr/bin/env python3
"""Decision Matrix engine: weighted scoring plus real sensitivity analysis.

Answers the only question that matters about a scoring matrix: would the
answer change if the numbers were somewhat different?

Spec format:
{
  "decision": "Which EHR integration partner for a clinic pilot",
  "scale": [1, 5],
  "options": ["Redox", "Health Gorilla", "Direct HL7"],
  "criteria": [
    {"name": "Time to first site", "weight": 30, "direction": "benefit"},
    {"name": "Integration cost",   "weight": 25, "direction": "cost"}
  ],
  "scores": {"Redox": {"Time to first site": 4, "Integration cost": 2}, ...},
  "score_uncertainty": 0.5,
  "weight_confidence": "medium",
  "baseline": "Do nothing",
  "top_k": 5,
  "groups": {"Redox": "integration", "Health Gorilla": "integration"}
}

baseline (REQUIRED): the name of the do-nothing / status-quo option, which must
  be one of the options. Use null only when there genuinely is no status quo,
  and say why in the note. Without a baseline you cannot tell whether the winner
  is good or merely the least bad.
top_k (optional): screening mode, for cutting a long-list. Reports how often
  each option lands in the top k. Turned on automatically (k=5) at 10+ options.
groups (optional): for options that can be combined rather than chosen between.
  Maps each option to the job it does; the engine then picks one per group.

direction "benefit" = higher raw score is better (default).
direction "cost"    = higher raw score is worse; it gets inverted internally.
weight_confidence: "high" | "medium" | "low" — how firm the weights are.

Usage: python3 sensitivity.py spec.json
Needs numpy. If your python3 lacks it:  uv run --with numpy python sensitivity.py spec.json
"""
import json
import sys

try:
    import numpy as np
except ImportError:
    raise SystemExit("sensitivity.py needs numpy, which this python does not have.\n"
                     "Run it as:  uv run --with numpy python " + " ".join(sys.argv) + "\n"
                     "or with any python that has numpy installed.")

CONC = {"high": 80.0, "medium": 25.0, "low": 8.0}


def load(path):
    spec = json.load(open(path))
    opts = spec["options"]
    if "baseline" not in spec:
        raise SystemExit(
            'The spec has no "baseline". Add the do-nothing / status-quo option to\n'
            '"options" and name it: "baseline": "Do nothing". If there genuinely is\n'
            'no status quo, set "baseline": null and say why in the note.')
    if spec["baseline"] is not None and spec["baseline"] not in opts:
        raise SystemExit(f"Baseline '{spec['baseline']}' is not one of the options.")
    crits = spec["criteria"]
    lo, hi = spec.get("scale", [1, 5])
    names = [c["name"] for c in crits]

    w = np.array([float(c.get("weight", 1)) for c in crits], dtype=float)
    if w.sum() <= 0:
        raise SystemExit("Weights must sum to something positive.")
    w = w / w.sum()

    raw = np.zeros((len(opts), len(crits)))
    for i, o in enumerate(opts):
        if o not in spec["scores"]:
            raise SystemExit(f"No scores given for option '{o}'.")
        for j, c in enumerate(names):
            if c not in spec["scores"][o]:
                raise SystemExit(f"Option '{o}' has no score for criterion '{c}'.")
            raw[i, j] = float(spec["scores"][o][c])

    if raw.min() < lo or raw.max() > hi:
        raise SystemExit(f"Scores must fall inside the stated scale [{lo}, {hi}].")

    # Normalise everything to higher-is-better.
    adj = raw.copy()
    for j, c in enumerate(crits):
        if c.get("direction", "benefit").lower().startswith("cost"):
            adj[:, j] = (hi + lo) - adj[:, j]
    return spec, opts, names, crits, w, raw, adj, lo, hi


def totals(adj, w):
    return adj @ w


def rank(opts, t):
    order = np.argsort(-t)
    return [(opts[i], t[i]) for i in order]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: sensitivity.py <spec.json>")
    spec, opts, names, crits, w, raw, adj, lo, hi = load(sys.argv[1])
    span = hi - lo
    out = []
    add = out.append

    add("=" * 70)
    add("DECISION MATRIX — SCORES AND SENSITIVITY")
    add("=" * 70)
    if spec.get("decision"):
        add(f"Decision: {spec['decision']}")
    add(f"Scale: {lo}-{hi}   Options: {len(opts)}   Criteria: {len(names)}")
    add("")

    add("WEIGHTS AS STATED")
    for n, c, wi in zip(names, crits, w):
        d = c.get("direction", "benefit")
        flag = "  (lower raw score is better)" if d.startswith("cost") else ""
        add(f"  {wi * 100:5.1f}%  {n}{flag}")
    add("")

    t = totals(adj, w)
    r = rank(opts, t)
    add("BASE RESULT")
    for i, (o, v) in enumerate(r, 1):
        add(f"  {i}. {o:<28} {v:.3f}")
    winner, wv = r[0]
    runner, rv = r[1] if len(r) > 1 else (None, None)
    if runner:
        gap = (wv - rv) / span * 100
        add("")
        add(f"  Margin over runner-up: {wv - rv:.3f} points "
            f"({gap:.1f}% of the scale)")
        if gap < 5:
            add("  → This is a coin flip. The matrix is not deciding this for you.")
        elif gap < 12:
            add("  → Narrow. Expect the sensitivity tests below to flip it.")
    base = spec.get("baseline")
    b_idx = opts.index(base) if base is not None else None
    if base is None:
        add("")
        add("  No baseline declared: this ranking cannot say whether the winner")
        add("  beats doing nothing.")
    else:
        below = [o for o, v in r if v <= t[b_idx] and o != base]
        add("")
        add(f"  Baseline: {base} ({t[b_idx]:.3f}). "
            f"{len(opts) - 1 - len(below)} option(s) beat it; {len(below)} do not.")
        if winner == base:
            add("  → The baseline wins. Nothing here beats the status quo.")
    add("")

    # --- Equal weights ------------------------------------------------------
    te = adj.mean(axis=1)
    win_eq = opts[int(np.argmax(te))]
    add("EQUAL-WEIGHTS CHECK")
    if win_eq == winner:
        add(f"  With every criterion weighted the same, {winner} still wins.")
        add("  The choice of weights is not what decides this.")
    else:
        add(f"  With every criterion weighted the same, {win_eq} wins instead of")
        add(f"  {winner}. The result depends on the weights: be sure they are")
        add("  what you believe, and see Test 2 for how far each can move.")
    add("")

    groups = spec.get("groups") or {}
    if groups:
        add("COMBINABLE OPTIONS — BEST IN EACH GROUP")
        add("These options do different jobs and can be used together, so the")
        add("question is which to pick for each job, not which single one wins.")
        add("")
        seen = []
        for o in opts:
            g = groups.get(o, "(ungrouped)")
            if g not in seen:
                seen.append(g)
        for g in seen:
            members = [(o, v) for o, v in r if groups.get(o, "(ungrouped)") == g]
            add(f"  {g}:")
            for o, v in members:
                note = ""
                if b_idx is not None and o != base:
                    note = "" if v > t[b_idx] else "   (does not beat the baseline)"
                add(f"     {o:<28} {v:.3f}{note}")
        add("")

    # --- Drop-one-criterion -------------------------------------------------
    add("-" * 70)
    add("TEST 1 — DROP EACH CRITERION")
    add("If removing one criterion changes the winner, the whole decision is")
    add("resting on that one criterion.")
    add("")
    flips = []
    for j, n in enumerate(names):
        keep = [k for k in range(len(names)) if k != j]
        w2 = w[keep] / w[keep].sum()
        t2 = adj[:, keep] @ w2
        win2 = opts[int(np.argmax(t2))]
        if win2 != winner:
            flips.append(n)
            add(f"  WITHOUT {n:<30} winner becomes {win2}   ← FLIPS")
        else:
            add(f"  without {n:<30} winner stays   {win2}")
    add("")

    # --- Weight-flip threshold ---------------------------------------------
    add("-" * 70)
    add("TEST 2 — HOW WRONG CAN EACH WEIGHT BE?")
    add("Sweeping each weight from 0% to 100% (others held in proportion) and")
    add("recording where the winner changes.")
    add("")
    grid = np.linspace(0.0, 0.995, 400)
    for j, n in enumerate(names):
        others = [k for k in range(len(names)) if k != j]
        osum = w[others].sum()
        crossing = None
        for g in grid:
            w2 = np.empty_like(w)
            w2[j] = g
            w2[others] = w[others] / osum * (1 - g) if osum > 0 else 0
            win2 = opts[int(np.argmax(adj @ w2))]
            if win2 != winner:
                crossing = g
                break
        cur = w[j]
        if crossing is None:
            add(f"  {n:<34} never flips. Robust at any weight.")
        else:
            delta = abs(crossing - cur) * 100
            direction = "raised to" if crossing > cur else "cut to"
            add(f"  {n:<34} flips if {direction} {crossing * 100:.0f}% "
                f"(now {cur * 100:.0f}%, a {delta:.0f}pt move)")
    add("")

    # --- Monte Carlo --------------------------------------------------------
    conf = str(spec.get("weight_confidence", "medium")).lower()
    k = CONC.get(conf, 25.0)
    sd = float(spec.get("score_uncertainty", 0.5))
    n_draws = 20000
    rng = np.random.default_rng(20260826)

    add("-" * 70)
    add("TEST 3 — SHAKE EVERYTHING AT ONCE")
    add(f"{n_draws:,} runs. Weights jittered around your stated values "
        f"({conf} confidence),")
    add(f"every score jittered by +/-{sd} points. How often does each option win?")
    add("")
    alpha = np.maximum(w * k, 0.05)
    W = rng.dirichlet(alpha, size=n_draws)
    S = adj[None, :, :] + rng.normal(0, sd, size=(n_draws, len(opts), len(names)))
    S = np.clip(S, lo, hi)
    T = np.einsum("nij,nj->ni", S, W)
    wins = np.argmax(T, axis=1)
    counts = np.bincount(wins, minlength=len(opts)) / n_draws
    for i in np.argsort(-counts):
        bar = "#" * int(round(counts[i] * 40))
        add(f"  {opts[i]:<28} {counts[i] * 100:5.1f}%  {bar}")
    add("")
    top = counts.max()
    k_top = spec.get("top_k") or (5 if len(opts) >= 10 else None)
    screening = bool(k_top) and k_top < len(opts)
    if screening or groups:
        add("  (With a long-list or combinable options, a single winner is not the")
        add("  question. Read the screening table below instead.)")
    elif top >= 0.85:
        add("  → Robust. The ranking is not an artefact of the exact numbers.")
    elif top >= 0.6:
        add("  → Leaning, not settled. Tighten the criterion the flip is most")
        add("    sensitive to (see Test 2) before committing.")
    else:
        add("  → The matrix does NOT distinguish these options. Either the")
        add("    criteria are missing something that actually matters, or the")
        add("    options are genuinely equivalent and you should decide on a")
        add("    factor outside this matrix.")
    add("")

    if screening or b_idx is not None:
        order_all = np.argsort(-T, axis=1)
        add("-" * 70)
        add("SCREENING — WHO RELIABLY MAKES THE CUT?")
        head = f"  {'option':<28}"
        if screening:
            in_top = np.zeros(len(opts))
            for i in range(len(opts)):
                in_top[i] = np.mean(np.any(order_all[:, :k_top] == i, axis=1))
            head += f" in top {k_top:<3}"
        if b_idx is not None:
            beats = np.mean(T > T[:, [b_idx]], axis=0)
            head += "  beats baseline"
        add(head)
        key = in_top if screening else beats
        for i in np.argsort(-key):
            line = f"  {opts[i]:<28}"
            if screening:
                line += f"   {in_top[i] * 100:5.1f}%  "
            if b_idx is not None:
                line += "       —" if i == b_idx else f"      {beats[i] * 100:5.1f}%"
            add(line)
        add("")
        if screening:
            solid = [opts[i] for i in np.argsort(-in_top) if in_top[i] >= 0.8]
            maybe = [opts[i] for i in np.argsort(-in_top) if 0.3 <= in_top[i] < 0.8]
            add(f"  Reliably in the top {k_top}: {', '.join(solid) if solid else 'none'}")
            if maybe:
                add(f"  On the edge (the cut line is a judgement here): {', '.join(maybe)}")
        add("")

    # --- Dominance ----------------------------------------------------------
    add("-" * 70)
    add("TEST 4 — DOMINANCE AND DEAD WEIGHT")
    dom = []
    for i in range(len(opts)):
        for j2 in range(len(opts)):
            if i == j2:
                continue
            if np.all(adj[i] >= adj[j2]) and np.any(adj[i] > adj[j2]):
                dom.append((opts[i], opts[j2]))
    if dom:
        for a, b in dom:
            add(f"  {a} beats {b} on every criterion — {b} is dominated, drop it.")
    else:
        add("  No option beats another on every criterion. Every option here")
        add("  involves a real trade-off.")

    spread = adj.max(axis=0) - adj.min(axis=0)
    dead = [n for n, s in zip(names, spread) if s == 0]
    if dead:
        add("")
        for n in dead:
            add(f"  '{n}' scores identically for every option. It cannot affect")
            add("  the outcome — it is describing the field, not deciding it.")
    add("")
    add("=" * 70)
    if flips:
        add(f"HEADLINE: {winner} wins, but the result hangs on "
            f"{', '.join(flips)}.")
    elif top >= 0.85:
        add(f"HEADLINE: {winner} wins and survives everything thrown at it.")
    else:
        add(f"HEADLINE: {winner} wins on the stated numbers but only "
            f"{top * 100:.0f}% of the time under uncertainty.")
    add("=" * 70)
    print("\n".join(out))


if __name__ == "__main__":
    main()
