"""Behavior tests for exact proportional allocation."""

import pytest

from allocation import allocate, split_charge


def test_even_split_is_exact():
    assert allocate(9000, [1, 1, 1]) == [3000, 3000, 3000]


def test_pennies_are_conserved():
    shares = allocate(10000, [1, 1, 1])
    assert sum(shares) == 10000
    assert shares == [3334, 3333, 3333]


def test_equal_exact_remainders_keep_input_order():
    assert allocate(10, [1, 1, 4]) == [2, 2, 6]


def test_weighted_split_matches_weights():
    assert allocate(10000, [50, 30, 20]) == [5000, 3000, 2000]


def test_half_cent_rounds_up_not_down():
    assert allocate(5, [1, 1]) == [3, 2]


def test_zero_total_gives_zero_shares():
    assert allocate(0, [1, 1, 1]) == [0, 0, 0]


def test_empty_weights_raise():
    with pytest.raises(ValueError):
        allocate(10000, [])


def test_zero_weights_raise():
    with pytest.raises(ValueError):
        allocate(10000, [0, 0])


def test_split_charge_reconciles_to_total():
    usage = {"web": 50, "mobile": 30, "batch": 20}
    shares = split_charge(10000, usage)
    assert shares == {
        "web": 5000,
        "mobile": 3000,
        "batch": 2000,
    }
    assert sum(shares.values()) == 10000
