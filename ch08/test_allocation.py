"""Adversarial tests for `allocate` (listing 8.3).

One test per category the tester and red-team prompts named. The star is
`test_pennies_are_conserved`: it fails against the plausible first draft,
which rounded each share on its own and lost a cent, and passes once the
split floors and distributes the remainder. Assertions are on exact
returned shares, so a wrong split cannot hide behind the right shape.
"""

import pytest

from allocation import allocate, split_charge


def test_even_split_is_exact():
    # The happy path the buggy draft also passed: divides evenly.
    assert allocate(9000, [1, 1, 1]) == [3000, 3000, 3000]


def test_pennies_are_conserved():
    # $100.00 split three ways. The buggy draft returned
    # [3333, 3333, 3333], which is 9999 cents, and lost one.
    shares = allocate(10000, [1, 1, 1])
    assert sum(shares) == 10000
    assert shares == [3334, 3333, 3333]


def test_weighted_split_matches_weights():
    assert allocate(10000, [50, 30, 20]) == [5000, 3000, 2000]


def test_half_cent_rounds_up_not_down():
    # 5 cents split evenly. round(2.5) is 2 in Python (banker's
    # rounding), so the draft returned [2, 2] and lost a cent.
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
    assert shares == {"web": 5000, "mobile": 3000, "batch": 2000}
    assert sum(shares.values()) == 10000
