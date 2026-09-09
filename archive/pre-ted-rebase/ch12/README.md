# Chapter 12 — Measuring and governing AI-assisted work

A workflow quality metric whose population is wrong: it reports `1.0` for a
sample with one qualifying success and one failed terminal attempt. An
independent test states the denominator policy, the bounded repair counts
every terminal attempt, and a reviewable decision record keeps the scope
judgment with a human owner.

- **`workflow_metrics.py`** — Listing 12.3 target: the green metric that counts every terminal attempt in the denominator
- **`test_workflow_metrics.py`** — Listing 12.2: the denominator test, plus the three maintained checks
- **`listing_12_3_terminal_denominator.diff`** — Listing 12.3: Counting terminal attempts in the denominator
- **`listing_12_4_decision_record.py`** — Listing 12.4: A reviewable workflow decision record
- **`captures/before/workflow_metrics.py`** — Listing 12.1: the defective before-state metric
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

## Setup and checks

Run from this directory (needs only the standard library; `pytest` is
optional):

```bash
python3 -m unittest -v test_workflow_metrics
# or, equivalently:
python3 -m pytest -q
```

Either command reports **4 passing tests**: failed-attempt inclusion,
quality-threshold evaluation, pending-attempt exclusion, and the
no-terminal-attempt result.

## Listing map

- **Listing 12.1** is the defective metric that filters to successful
  attempts before computing the denominator. It is preserved as the red
  before-state at `captures/before/workflow_metrics.py`; the maintained
  `workflow_metrics.py` is the green after-state.
- **Listing 12.2** is `test_failed_attempts_remain_in_denominator` in
  `test_workflow_metrics.py`, which states the denominator policy with two
  terminal outcomes.
- **Listing 12.3** is the one-change repair (`listing_12_3_terminal_denominator.diff`):
  the denominator becomes the count of attempts whose status is explicitly
  `succeeded` or `failed`.
- **Listing 12.4** is `listing_12_4_decision_record.py`, a decision record
  that records a `pause` action and its evidence boundary.

## Red-to-green capture

See [`captures/README.md`](captures/README.md) to reproduce the denominator
red result (`1.0` instead of `0.5`) and the bounded repair.

## Limits

Only `succeeded` and `failed` are treated as terminal; any other status must
be classified before changing the denominator policy. The `0.80` quality
minimum is a test input, not a validated production threshold. Four examples
do not establish benchmark representativeness, and passing tests do not
authorize standardization, wider rollout, or stronger write authority.

See the [main README](../README.md) for setup instructions.
