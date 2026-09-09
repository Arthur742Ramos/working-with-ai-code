from types import SimpleNamespace

plan = SimpleNamespace(max_unavailable=2)
failures = []
if (
    type(plan.max_unavailable) is not int
    or plan.max_unavailable not in (0, 1)
):
    failures.append(
        "max_unavailable must be 0 or 1"
    )
print(failures)
