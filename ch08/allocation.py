"""Proportional money allocation (chapter 8 running example).

Split a charge across the parties that share it: a shared invoice across
the cost centers that used the service, a marketplace sale across the
seller, the platform fee, and tax. The rule sounds trivial, divide by
weight, and the first AI draft (listing 8.1) got it plausibly wrong.

The draft rounded each share on its own:

    return [round(total * w / total_weight) for w in weights]

For a $100.00 charge split three ways that returns [3333, 3333, 3333],
which is 9999 cents, not 10000. The missing cent has to come from
somewhere, so the ledger stops reconciling. The happy-path tests the
model wrote alongside it passed, because they only used inputs that
divide evenly, like $90.00 across three shares.

The fix is not one token. A correct split floors every share, then hands
the leftover cents to the shares with the largest fractional part, one
cent each, until the money is gone. This is the largest-remainder
(Hamilton) method, and it guarantees two things the draft could not: the
shares sum to exactly `total`, and no share is more than a cent off its
ideal proportional value.

Everything here works in integer cents. Money is not a float: dollars as
floats accumulate rounding error of their own, so the whole domain stays
in the smallest unit and converts to dollars only for display.
"""

from collections.abc import Mapping, Sequence

Weight = float  # a share weight: usage, headcount, ownership fraction


def allocate(total: int, weights: Sequence[Weight]) -> list[int]:
    """Split `total` cents across `weights`, proportional and exact.

    Returns one integer-cent share per weight. The shares sum to
    exactly `total`, and each share is within a cent of its ideal
    proportional value. Raises ValueError on inputs that cannot be
    split: no weights, negative money, or weights that sum to zero.
    """
    if not weights:
        raise ValueError("need at least one share to allocate to")
    if total < 0 or any(w < 0 for w in weights):
        raise ValueError("total and weights must be non-negative")

    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("weights sum to zero, cannot split by them")

    ideal = [total * w / total_weight for w in weights]
    shares = [int(x) for x in ideal]          # floor each share
    leftover = total - sum(shares)            # cents still to place

    # Give the leftover cents to the largest fractional parts, one each.
    order = sorted(
        range(len(weights)),
        key=lambda i: ideal[i] - shares[i],
        reverse=True,
    )
    for i in order[:leftover]:
        shares[i] += 1
    return shares


def split_charge(
    total_cents: int,
    usage: Mapping[str, Weight],
) -> dict[str, int]:
    """Split a charge across named cost centers by their usage weight.

    The real consumer in the opening scenario: `usage` maps each cost
    center to how much of the service it used, and the result maps each
    to its share in cents. The shares sum to `total_cents`, so the
    chargeback ledger reconciles to the amount actually billed.
    """
    names = list(usage)
    shares = allocate(total_cents, [usage[name] for name in names])
    return dict(zip(names, shares))
