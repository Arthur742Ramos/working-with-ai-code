"""Focused regression tests for exact allocation order."""

from allocation import allocate


def test_pennies_are_conserved():
    shares = allocate(10000, [1, 1, 1])
    assert sum(shares) == 10000
    assert shares == [3334, 3333, 3333]


def test_equal_exact_remainders_keep_input_order():
    assert allocate(10, [1, 1, 4]) == [2, 2, 6]
