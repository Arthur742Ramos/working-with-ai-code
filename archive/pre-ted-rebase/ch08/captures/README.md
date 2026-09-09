# Chapter 8 capture — the lost cent

The red before-state ranks fractional remainders as binary floats. For
`allocate(10, [1, 1, 4])` all three mathematical remainders are two-thirds,
but binary division stores the third residue slightly larger, so the stable
sort never sees an equal key and assigns the second leftover cent to the
wrong index (`[2, 1, 7]` instead of `[2, 2, 6]`).

## Files

- `before/allocation.py` — the red before-state ranking binary-float residues.
- `test_lost_cent.py` — the focused exact-tie test. It imports only
  `allocate`, so it runs against the before-state, which predates
  `split_charge`. `pytest.ini` keeps it out of the ordinary top-level run.

## Reproduce the red-to-green repair

Run from the chapter directory (`ch08/`). Copy the before-state and the
focused test into disposable space so the maintained `allocation.py` is never
left in the before-state:

```bash
WORK=$(mktemp -d)
cp captures/before/allocation.py captures/test_lost_cent.py "$WORK/"

# Focused red against the before-state
(cd "$WORK" && python3 -m pytest -q test_lost_cent.py)

# The bounded repair (already applied in the maintained allocation.py):
# convert each weight to an exact Fraction(str(weight)) before ranking
# residues, preserving the largest-remainder stages and stable sort.
cp allocation.py "$WORK/"

# Focused green against the maintained implementation
(cd "$WORK" && python3 -m pytest -q test_lost_cent.py)
rm -rf "$WORK"

# Broader suite green
python3 -m pytest -q
```

The focused red reports `1 failed, 1 passed`, with
`test_equal_exact_remainders_keep_input_order` failing on
`[2, 1, 7] != [2, 2, 6]`. After the exact-`Fraction` repair the focused test
reports `2 passed`, and the maintained suite reports `10 passed`.
