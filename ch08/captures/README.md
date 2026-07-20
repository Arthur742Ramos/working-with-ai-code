# Chapter 8 capture — the lost cent

The red before-state ranks fractional remainders as binary floats. For
`allocate(10, [1, 1, 4])` all three mathematical remainders are two-thirds,
but binary division stores the third residue slightly larger, so the stable
sort never sees an equal key and assigns the second leftover cent to the
wrong index (`[2, 1, 7]` instead of `[2, 2, 6]`).

## Files

- `before/allocation.py` — the red before-state ranking binary-float residues.

## Reproduce the red-to-green repair

Run from the chapter directory (`ch08/`):

```bash
# The bounded repair (already applied in the maintained allocation.py):
# convert each weight to an exact Fraction(str(weight)) before ranking
# residues, preserving the largest-remainder stages and stable sort.

python3 -m pytest -q
```

The maintained `allocation.py` uses exact `Fraction` residues, so the suite
reports `10 passed`. Use `before/allocation.py` in a disposable copy to
reproduce the red result, where `test_equal_exact_remainders_keep_input_order`
fails with `[2, 1, 7] != [2, 2, 6]`. Never leave the maintained
`allocation.py` in the before-state.
