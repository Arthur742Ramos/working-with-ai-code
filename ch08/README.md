# Chapter 8 — Code Listings

The running example for chapter 8: proportional money allocation, split
across the parties that share a charge. The point is not the arithmetic;
it is the verification around it. The first AI draft of `allocate` looked
finished and passed its own happy-path tests, but it rounded each share on
its own, so the shares did not add back to the total: a $100.00 charge
split three ways came out as $99.99. Like chapters 6 and 7, this is a
runnable project rather than a set of standalone listing files.

- **`allocation.py`** — Listing 8.1: The corrected `allocate`. The book's
  Listing 8.1 shows the broken first draft; this file is the fixed
  version. `allocate(total, weights) -> list[int]` floors each share, then
  hands the leftover cents to the largest fractional parts (the
  largest-remainder method), so the shares sum to exactly `total`.
  `split_charge` is the real consumer: split a charge across named cost
  centers so the chargeback ledger reconciles.
- **`sanity.py`** — Listing 8.2: Cheap, implementation-independent checks.
  `conserves` asserts the shares sum to `total`; `is_fair` asserts no
  share is more than a cent off its ideal. Run `python3 sanity.py` and it
  prints `smoke ok`.
- **`test_allocation.py`** — Listing 8.3: Adversarial tests, one per
  category the tester and red-team prompts named.
  `test_pennies_are_conserved` is the slice the agent turns from red to
  green in section 8.8.
- **`test_golden.py`** — Listing 8.4: A frozen golden set, evaluation made
  executable. The three-way split that once shipped broken is pinned here
  so it cannot return quietly.
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft.

Run the suite:

```bash
cd ch08 && python3 -m pytest -q
```

Expected: `9 passed`. The only dependency is `pytest` (see
[`requirements.txt`](requirements.txt)).

To see the bug the chapter starts from, replace the body of `allocate` in
`allocation.py` with the naive draft:

```python
total_weight = sum(weights)
return [round(total * w / total_weight) for w in weights]
```

Rerun: `test_pennies_are_conserved` goes red and `sanity.py` raises on the
three-way split, while the even-split happy-path test stays green.

See the [main README](../README.md) for setup instructions.
