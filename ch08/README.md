# Chapter 8 — From checks to evaluations

Proportional money allocation by largest exact remainder. Two focused checks
with different jobs (penny conservation and stable input-order ties), the
exact-rational-residue repair that fixes binary-float misordering, and a
frozen golden set that makes evaluation executable.

- **`allocation.py`** — Listing 8.2 target: the maintained allocation using exact `Fraction` residues
- **`test_allocation.py`** — Listing 8.1: two checks with different jobs, plus the broader behavior suite
- **`test_golden.py`** — Listing 8.3: excerpt from the maintained allocation golden set
- **`captures/before/allocation.py`** — the red before-state using binary-float residues
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

## Setup and checks

Run from this directory (needs only `pytest`):

```bash
python3 -m pytest -q
```

`python3 -m pytest -q` reports **10 passed** (nine behavior checks plus the
golden set).

## Listing map

- **Listing 8.1** is the pair `test_pennies_are_conserved` and
  `test_equal_exact_remainders_keep_input_order` in `test_allocation.py`:
  one proves the shares sum to the total, the other pins a stable tie.
- **Listing 8.2** converts each weight to an exact `Fraction(str(weight))`
  before ranking residues, so equal mathematical remainders keep input
  order. The maintained `allocation.py` is the green after-state;
  `captures/before/allocation.py` is the red before-state that ranks binary
  floats and misassigns a leftover cent.
- **Listing 8.3** is the frozen `GOLDEN` set and `test_golden_set` in
  `test_golden.py`.

## Red-to-green capture

See [`captures/README.md`](captures/README.md) to reproduce the exact-tie
red result and the exact-residue repair.

## Limits

These checks do not cover every numeric type, non-finite input, extreme
magnitude, or fairness policy. The golden set is a maintained baseline, not a
proof of representativeness.

See the [main README](../README.md) for setup instructions.
