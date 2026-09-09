"""Maintained golden cases for proportional allocation."""

from allocation import allocate

GOLDEN = [
    (9000, [1, 1, 1], [3000, 3000, 3000]),
    (10000, [1, 1, 1], [3334, 3333, 3333]),
    (10000, [50, 30, 20], [5000, 3000, 2000]),
    (5, [1, 1], [3, 2]),
    (0, [1, 1, 1], [0, 0, 0]),
    (10000, [1], [10000]),
]


def test_golden_set():
    for total, weights, expected in GOLDEN:
        assert allocate(total, weights) == expected, (
            total,
            weights,
        )


if __name__ == "__main__":
    test_golden_set()
    print(f"golden set ok: {len(GOLDEN)} cases")
