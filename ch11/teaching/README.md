# Current policy probe

`policy_probe.py` is the complete standalone program printed in Listing 11.1. Run it from the Chapter 11 directory with:

```bash
python3 teaching/policy_probe.py
```

It prints `['max_unavailable must be 0 or 1']`. In a disposable copy, change only the supplied value from `2` to `1` and it prints `[]`; a Boolean is still rejected. The branch matches the unavailable-capacity check in `deployment_guard.py`, with setup and output included so the listing runs on its own.

This probe tests the adopted six-replica teaching rule. It does not query a service, establish a safe threshold for other traffic or replica counts, or deploy anything. The top-level capture package and its sealed listing ledger retain the original branch-only presentation and captured evidence unchanged. The current printed example adds the existing probe's setup and output.
