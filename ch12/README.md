# Chapter 12 final support package

This internal package keeps the final workflow-quality metric, its maintained tests, and the verified denominator capture together.

## Files

- `workflow_metrics.py` is the green book-state implementation. It counts every explicit `succeeded` or `failed` terminal attempt in the denominator.
- `test_workflow_metrics.py` contains the four maintained tests used by the chapter.
- `pytest.ini` keeps top-level pytest collection out of `captures/`, whose fixture is intentionally red before replay applies the patch.
- `captures/benchmark_denominator/` preserves the defective red before-state, exact patch, raw evidence, session record, and replay runner.

## Verify the final implementation

Run from this directory:

```bash
python3 -m unittest -v test_workflow_metrics
```

The expected result is four passing tests. The suite checks failed-attempt inclusion, quality-threshold evaluation, pending-attempt exclusion, and the no-terminal-attempt result. Run this explicit module command rather than recursively collecting `captures/`. If you use pytest, the package-local `pytest.ini` enforces the same boundary.

## Replay the captured repair

Run from this directory:

```bash
python3 captures/benchmark_denominator/run_capture.py
```

Replay rebuilds the red state in disposable space, applies the exact stored patch, reproduces the focused and broader green results, verifies the package-local source, test, and pytest configuration checksums, and removes temporary work on success or failure. Default replay does not rewrite evidence. It reads no repository-root, staged-chapter, canonical-code, or other-chapter file.

## Remaining limitations

- Only `succeeded` and `failed` are classified as terminal. The workflow owner must classify any additional status before changing the denominator policy.
- The `0.80` quality minimum is an input used by the tests, not a validated production threshold.
- Four examples do not establish benchmark representativeness, sample adequacy, or complete failure taxonomy coverage.
- Passing tests verify this metric behavior. They do not authorize standardization, wider rollout, or stronger write authority.
