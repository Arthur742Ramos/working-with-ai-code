"""Deliberately broken teaching draft, followed by its smoke check.

This is the pre-repair example from Listings 8.1 and 8.2, not the
validated publication implementation in allocation.py.
"""

def allocate(total, weights):
    total_weight = sum(weights)
    shares = []
    for weight in weights:
        shares.append(round(total * weight / total_weight))
    return shares


def conserves(shares, total):
    return sum(shares) == total


def smoke_test(total, weights):
    shares = allocate(total, weights)
    assert conserves(shares, total), shares
