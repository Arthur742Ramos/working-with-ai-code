"""A golden set: evaluation made executable (listing 8.4).

A frozen list of (total, weights, expected) rows that any future
implementation of `allocate` must satisfy. The three-way $100.00 split is
pinned here on purpose: the case that once shipped broken is now a
regression test, so the same penny-drift bug cannot return quietly. Run
this on every change, not just once. Every new bug you find becomes a new
row, so the suite gets stronger exactly where you have been burned.
"""

from allocation import allocate

GOLDEN = [
    (9000, [1, 1, 1], [3000, 3000, 3000]),      # divides evenly
    (10000, [1, 1, 1], [3334, 3333, 3333]),     # shipped broken once
    (10000, [50, 30, 20], [5000, 3000, 2000]),  # weighted, exact
    (5, [1, 1], [3, 2]),                         # half-cent rounds up
    (0, [1, 1, 1], [0, 0, 0]),                   # nothing to split
    (10000, [1], [10000]),                       # a single share
]


def test_golden_set():
    for total, weights, expected in GOLDEN:
        assert allocate(total, weights) == expected, (total, weights)


if __name__ == "__main__":
    test_golden_set()
    print(f"golden set ok: {len(GOLDEN)} cases")
