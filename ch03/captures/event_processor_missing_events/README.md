# Event processor missing-events capture

This capture records the missing-events ask-inspect-adjust turn in the
chapter's broader reconstructed review. The surrounding ranking, checkpoint,
and timezone discussions are outside the captured work. The historical
independent-review receipt predates this terminology correction: its word
*illustrative* reflects the classification used at the time.

## Selected behavior

A JSON object without an `events` key must fail with:

```text
ValueError: input must be an object with an 'events' key
```

An explicit `{"events": []}` is an empty batch, not a missing collection. The
captured patch changes only the missing-key behavior. The empty-result
arithmetic defect remains in the captured workflow and was repaired later.

## Record and replay

Follow the isolated pytest setup in the [Chapter 3 guide](../../README.md#set-up-an-isolated-test-environment).
The runner uses the same interpreter for its final-package pytest checks.

From `ch03/` (the final package root), replay without rewriting evidence:

```bash
python3 captures/event_processor_missing_events/run_capture.py
```

From `ch03/captures/event_processor_missing_events/`, the equivalent command is:

```bash
python3 run_capture.py
```

To recreate evidence after reviewing it, run this from the capture directory:

```bash
python3 run_capture.py --record
```

The runner verifies the capture inputs, final-package checksums, and active
independent-review receipt before rebuilding disposable red and repaired
states. It exercises the rejected falsy-lookup candidate, then compares the
exact patch and stored outputs. It also runs the final package's maintained
top-level suite and verifies `chapter-session.md`. The runner removes `.work/`
after success or failure.

Default replay leaves the stored evidence unchanged. Use `--record` only after
reviewing a change to the fixture, tests, patch, final-package checks, or evidence.

## Direct historical evidence commands

Run the commands below from this capture directory. They show the historical
command shapes; the `before/` fixture remains available. The repaired `.work/`
target exists only while `run_capture.py` runs. Its `finally` block
deletes `.work/` after success or failure, including a missing-pytest failure.
Running the `.work/` commands after the runner exits raises
`FileNotFoundError`. Use replay to exercise the repaired historical state.

```bash
python3 tests/focused_test.py before/event_processor.py
python3 tests/focused_test.py .work/event_processor.py
python3 tests/full_capture_check.py .work/event_processor.py
```

To run the printed command shapes against the final green module, use these
wrappers from the package root:

```bash
python3 focused_test.py event_processor.py
python3 full_capture_check.py event_processor.py
```

The final-state wrappers expect the later zero-average repair. Capture replay
verifies the historical output, where an explicit empty list reaches the
arithmetic defect that was still present at the time.

## Dependencies and assumptions

- Python 3 is available as `python3`.
- `diff` is available for the machine-generated patch.
- `pytest` is available for the final-package test run.
- The filesystem permits a disposable `.work/` directory and temporary files.

All executable paths resolve within the final Chapter 3 package. Replay has no repository-root, canonical-code, other-chapter, or Box dependency.

## Approval and policy boundary

Standing direction authorized the narrowest readable implementation without another checkpoint. The agent selected a fail-fast missing-key guard because the contract distinguishes malformed missing input from an explicit empty batch. The input-contract owner remains responsible for that policy choice.

## What the checks prove

Focused red shows that the immutable before state leaks `KeyError: 'events'`.
The rejected-candidate control shows that `if not data.get("events")` incorrectly
classifies an explicit empty list as missing. Focused green checks the exact
error contract and the missing-versus-empty distinction. Broader green checks
one representative non-empty input and its written summary. The separate
top-level run checks the final green package and executes both final-state
command wrappers.

## What the checks do not prove

The captured slice does not prove handling for non-object JSON, non-list `events`, malformed individual events, or the later empty-result repair. The final suite also leaves explicit UTF-8, atomic output, unsafe `type` values, some skipped-event details, summary logging, and output-failure behavior outside its evidence boundary.

Stored historical command output required no post-processing. Color was disabled before the retained final-package test run.

## Independent certification

An independent canonical capture review replayed disposable and standalone
copies of the package. It regenerated the patch, checked minimality, verified
printed parity and provenance, and confirmed the human policy boundary.
The review receipt is `evidence/independent-review.md`.

Active package state is `complete_independently_reviewed`, review status is `completed`, and the final verdict is `Pass`. Default replay rejects that completed stage if the active review status is missing or pending, the verdict is not `Pass`, or the review artifact is missing or checksum-invalid.

`chapter-session.md` remains a current semantic publication excerpt rather than a byte-for-byte mirror of the live chapter. Its contract, patch, commands, outputs, provenance boundary, and policy boundary match the chapter; surrounding inspection wording may differ. The excerpt retains the historical Listing 3.2 label for the patch; the restored active chapter renumbers that same patch as Listing 3.5 after adding the branch listings.
