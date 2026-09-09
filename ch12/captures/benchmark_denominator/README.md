# Benchmark denominator capture

## Selected behavior

This internal package preserves a complete coding-agent session for one denominator defect. Every explicit terminal workflow attempt must remain in the quality denominator, including failed attempts. The red before-state filters to successful attempts first, so one qualifying success and one failed attempt produce `1.0` instead of `0.5`.

The exact stored patch changes only the denominator. The final package promotes that patched implementation at its top level while this capture retains the immutable red evidence.

## Replay

Run from the final package directory:

```bash
python3 captures/benchmark_denominator/run_capture.py
```

Default replay does not rewrite evidence. It verifies package-local fixture and evidence checksums, reproduces the focused red, applies the exact machine patch in disposable space, reproduces the focused and broader greens, checks the top-level source, test, and pytest configuration, validates the active independent-review receipt, and removes temporary work on success or failure. It does not resolve the repository paths retained in metadata as capture-time provenance.

The capture runner retains `--record` for intentional evidence regeneration. Do not use it unless the evidence and its checksum locks are being reviewed and updated together.

## Dependencies and environment

The capture used Claude Code 2.1.210, CPython 3.14.6, macOS, and standard-library `unittest`. Replay also requires local POSIX `diff` and `patch` commands. It disables color and Python bytecode output. Output comparison normalizes elapsed time and the disposable traceback path; assertions, test names, counts, and exit statuses remain exact.

No network access, cloud credential, provider command, or target-system write is required.

## Selected implementation

The repair keeps the existing successful-attempt list, passing count, and early return. It replaces only the final denominator with an explicit count of `succeeded` and `failed` statuses. This leaves pending and unrecognized states outside the denominator without broadening the captured behavior.

## What the checks prove

The focused red proves that the before implementation returns `1.0` where the contract requires `0.5`. The focused green proves that the exact patch repairs that input. The broader green protects quality-threshold evaluation, pending-attempt exclusion, and zero when no terminal attempts exist. The final-package check proves the promoted top-level implementation matches the reviewed after-state and passes the same four tests.

## Independent certification

A separate independent canonical capture review replayed the package from disposable and isolated copies, regenerated the exact patch, checked minimality, verified printed parity and provenance, and confirmed the human policy boundary. The attributable receipt is `evidence/independent-review.md`.

Active package state is `complete_independently_reviewed`, review status is `completed`, and the final verdict is `Pass`. Default replay rejects that completed stage if the active review status is missing or pending, the verdict is not `Pass`, or the review artifact or a checksum-locked package record is missing or invalid.

## Remaining limitations and policy boundary

The checks do not establish that `0.80` is the correct quality threshold, that the benchmark sample represents production work, that the status taxonomy is complete, or that the workflow is safe to standardize or widen. The workflow owner must classify additional terminal statuses and decide whether broader operational evidence supports any rollout.
