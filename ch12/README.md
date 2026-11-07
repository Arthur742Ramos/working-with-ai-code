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

## Separate behavioral verifier

For a non-recording check verified on Linux with CPython 3.12.14 and 3.13.5:

```bash
python3 verify_behavior.py
python3 -B -m unittest -v test_verify_behavior
```

The first command uses the unchanged historical runner's input, review-state,
semantic and checksum checks. It stages the red source and tests in temporary
space, requires the recorded denominator failure, applies the stored patch,
verifies the exact repaired source and generated diff, then checks the focused,
four-test broader and four-test maintained green results. The second command
runs ten verifier regressions and negative controls. These are separate from
the sealed four-test package suite.

This verifier compares all recorded output after the historical path/time
normalization, with one additional equivalence: the exact caret line beneath
`self.assertEqual(rate, 0.50)` may be absent immediately before the unchanged
`AssertionError: 1.0 != 0.5` diagnostic. Other output, failure values, test
names/counts, exit statuses and hashes must still match. Its output explicitly
states that strict historical transcript equality is not asserted.

There is no `--record` mode. The verifier writes only to temporary space and
leaves the historical runner, metadata, raw evidence, patch and review receipt
unchanged. That historical receipt does not certify this new verifier. Other
Python versions and platforms have not been verified by these checks.

## Replay compatibility

The maintained four-test suite and the strict historical replay have different
compatibility limits. On Linux, the maintained suite passed with CPython
3.12.14 and 3.13.5. The unchanged replay passed with CPython 3.13.5.
These observations do not establish compatibility with Python 3.11, every
3.13 release, or other platforms.

On CPython 3.12.14, the replay reaches the required denominator failure,
applies the exact stored patch, and passes its focused, broader, and maintained
green checks, but then exits nonzero with `stored focused-red output drifted`.
The difference is the traceback caret line beneath `self.assertEqual`: it is
absent in that runtime and present in the retained transcript. The runner
normalizes paths and elapsed time, not traceback caret formatting. This is a
strict transcript-compatibility failure, not a passing replay.

The capture metadata records macOS with Python 3.14.6 as the original runtime;
that environment was not rerun for this compatibility check. Use the verified
CPython 3.13.5 Linux environment for the strict replay, with `patch` and `diff`
available, or verify another environment before relying on its result.
Do not use `--record` or edit the runner, metadata, patch, or evidence to make a
formatting mismatch pass. Those files remain the historical capture record.

## Remaining limitations

- Only `succeeded` and `failed` are classified as terminal. The workflow owner must classify any additional status before changing the denominator policy.
- The `0.80` quality minimum is an input used by the tests, not a validated production threshold.
- Four examples do not establish benchmark representativeness, sample adequacy, or complete failure taxonomy coverage.
- Passing tests verify this metric behavior. They do not authorize standardization, wider rollout, or stronger write authority.
