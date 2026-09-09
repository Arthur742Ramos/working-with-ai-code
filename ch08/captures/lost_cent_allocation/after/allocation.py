"""Proportional allocation with stable input-order ties."""

from fractions import Fraction


def allocate(total, weights):
    exact_weights = [
        Fraction(str(weight))
        for weight in weights
    ]
    total_weight = sum(exact_weights)
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
