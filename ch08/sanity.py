"""Sanity checks for `allocate`, independent of how it is implemented.

`conserves` is the cheap invariant that catches the penny-drift bug:
the shares must add back to the money you started with. The broken first
draft returned [3333, 3333, 3333] for a $100.00 three-way split, which is
9999 cents, so this check fails without knowing anything about the
algorithm. It is a conservation law, and conservation laws do not share
the code's blind spot.

`is_fair` pins the other half of a correct split: no share is more than a
cent off its ideal proportional value. It catches an implementation that
conserves the total but distributes it unfairly, for example by dumping
all the leftover cents onto the last share.
"""

from collections.abc import Sequence

from allocation import Weight, allocate


def conserves(shares: Sequence[int], total: int) -> bool:
    return sum(shares) == total


def is_fair(
    shares: Sequence[int],
    total: int,
    weights: Sequence[Weight],
) -> bool:
    total_weight = sum(weights)
    return all(
        abs(share - total * w / total_weight) < 1
        for share, w in zip(shares, weights)
    )


def smoke_test(total: int, weights: list[Weight]) -> None:
    shares = allocate(total, weights)
    assert conserves(shares, total), (shares, total)
    assert is_fair(shares, total, weights), (shares, total, weights)


if __name__ == "__main__":
    smoke_test(10000, [1, 1, 1])       # the split that shipped broken
    smoke_test(9000, [1, 1, 1])
    smoke_test(10000, [50, 30, 20])
    smoke_test(5, [1, 1])
    smoke_test(0, [1, 1, 1])
    print("smoke ok")
