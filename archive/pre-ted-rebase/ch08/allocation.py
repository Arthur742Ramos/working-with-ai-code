"""Proportional allocation with exact remainder ranking."""

from collections.abc import Mapping, Sequence
from fractions import Fraction

Weight = int | float


def allocate(
    total: int,
    weights: Sequence[Weight],
) -> list[int]:
    """Split an integer total by largest exact remainder.

    Returns one integer share per weight. Equal exact
    remainders keep their input order.
    """
    if not weights:
        raise ValueError("need at least one share to allocate to")
    if total < 0 or any(weight < 0 for weight in weights):
        raise ValueError("total and weights must be non-negative")

    exact_weights = [
        Fraction(str(weight))
        for weight in weights
    ]
    total_weight = sum(exact_weights)
    if total_weight == 0:
        raise ValueError("weights sum to zero, cannot split by them")

    ideal = [
        total * weight / total_weight
        for weight in exact_weights
    ]
    shares = [int(value) for value in ideal]
    leftover = total - sum(shares)
    order = sorted(
        range(len(weights)),
        key=lambda index: ideal[index] - shares[index],
        reverse=True,
    )
    for index in order[:leftover]:
        shares[index] += 1
    return shares


def split_charge(
    total_cents: int,
    usage: Mapping[str, Weight],
) -> dict[str, int]:
    """Split a charge across names by usage weight."""
    names = list(usage)
    shares = allocate(
        total_cents,
        [usage[name] for name in names],
    )
    return dict(zip(names, shares))
