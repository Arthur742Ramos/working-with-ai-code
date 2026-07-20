# Chapter 12 capture — the benchmark denominator

The defective before-state filters to successful attempts before computing
both the numerator and the denominator. One qualifying success over two
terminal attempts is reported as `1.0` instead of `0.5`, because the failed
terminal attempt is removed before division.

## Files

- `before/workflow_metrics.py` — the defective before-state metric.

## Reproduce the red-to-green repair

Run from the chapter directory (`ch12/`):

```bash
# The bounded repair (already applied in the maintained workflow_metrics.py):
#   -    return passing_count / len(successful_attempts)
#   +    return passing_count / sum(
#   +        attempt.status in {"succeeded", "failed"}
#   +        for attempt in attempts
#   +    )

python3 -m unittest -v test_workflow_metrics
```

The maintained `workflow_metrics.py` counts every terminal attempt, so the
suite reports four passing tests. Use `before/workflow_metrics.py` in a
disposable copy to reproduce the red result, where
`test_failed_attempts_remain_in_denominator` fails with
`AssertionError: 1.0 != 0.5`. Never leave the maintained
`workflow_metrics.py` in the defective before-state.

Treat the repaired fixture as code evidence, not rollout evidence. The
workflow owner still needs to accept the per-attempt `0.80` quality minimum,
define a separate readiness-rate threshold, choose a representative sample and
status taxonomy, and set the evidence required before widening access.
