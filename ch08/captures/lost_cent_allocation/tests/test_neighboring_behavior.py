"""Broader checks for neighboring allocation behavior."""

from allocation import allocate


def test_even_split_stays_exact():
    assert allocate(9000, [1, 1, 1]) == [3000, 3000, 3000]


def test_weighted_split_stays_proportional():
    assert allocate(10000, [50, 30, 20]) == [5000, 3000, 2000]


def test_largest_remainder_receives_leftover():
    assert allocate(10, [3, 1, 2]) == [5, 2, 3]


def test_round_then_force_first_is_rejected():
    assert allocate(1, [1, 1, 2]) == [0, 0, 1]
