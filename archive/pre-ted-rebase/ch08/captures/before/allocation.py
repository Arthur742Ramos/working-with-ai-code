"""Proportional allocation with stable input-order ties."""


def allocate(total, weights):
    total_weight = sum(weights)
    ideal = [total * weight / total_weight for weight in weights]
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
