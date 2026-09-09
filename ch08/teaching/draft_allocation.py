"""Deliberately broken teaching draft, followed by its smoke check.

This is the pre-repair example from Listings 8.1 and 8.2, not the
validated publication implementation in allocation.py.
"""

def allocate(total, weights):
    total_weight = sum(weights)
    return [
        round(total * weight / total_weight)
        for weight in weights
    ]


def conserves(shares, total):
    return sum(shares) == total


def smoke_test(total, weights):
    shares = allocate(total, weights)
    assert conserves(shares, total), shares
