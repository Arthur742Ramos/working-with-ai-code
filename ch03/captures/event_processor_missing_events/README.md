# Event processor missing-events capture

This capture preserves one bounded repair inside the chapter's broader reconstructed review. It proves the missing-events ask-inspect-adjust turn; it does not turn the surrounding ranking, checkpoint, or timezone discussion into captured agent work. The historical independent-review receipt predates this terminology correction, so its use of *illustrative* is retained as historical wording rather than the current classification.

## Selected behavior

A JSON object without an `events` key must fail with:

```text
ValueError: input must be an object with an 'events' key
```

An explicit `{"events": []}` is an empty batch, not a missing collection. The captured patch changes only the missing-key behavior and leaves the later empty-result arithmetic defect in the captured workflow.

## Record and replay

From the final package root, replay without rewriting evidence:

```bash
python3 captures/event_processor_missing_events/run_capture.py
```

From this capture directory, the equivalent command is:

```bash
python3 run_capture.py
```

Recreate reviewed evidence intentionally only from this capture directory:

```bash
python3 run_capture.py --record
```

The runner verifies capture inputs, final-package checksums, and the active independent-review receipt; rebuilds disposable red and repaired states; exercises the rejected falsy-lookup candidate; compares the exact patch and stored outputs; runs the final package's maintained top-level suite; verifies `chapter-session.md`; and removes `.work/` on success or failure.

Default replay is read-only. Use `--record` only after intentionally reviewing a change to the fixture, tests, patch, final-package checks, or evidence.

## Direct historical evidence commands

The commands below are capture-internal. The repaired target exists only while `run_capture.py` is running:

```bash
python3 tests/focused_test.py before/event_processor.py
python3 tests/focused_test.py .work/event_processor.py
python3 tests/full_capture_check.py .work/event_processor.py
```

For executable versions of the printed command shapes against the final green module, run these from the package root:

```bash
python3 focused_test.py event_processor.py
python3 full_capture_check.py event_processor.py
```

The final-state wrappers intentionally expect the later zero-average repair. Capture replay remains the authority for the historical output in which an explicit empty list reaches the then-unrepaired arithmetic defect.

## Dependencies and assumptions

- Python 3 is available as `python3`.
- `diff` is available for the machine-generated patch.
- `pytest` is available for the final-package test run.
- The filesystem permits a disposable `.work/` directory and temporary files.

All executable paths resolve within the final Chapter 3 package. Replay has no repository-root, canonical-code, other-chapter, or Box dependency.

## Approval and policy boundary

Standing direction authorized the narrowest readable implementation without another checkpoint. The agent selected a fail-fast missing-key guard because the contract distinguishes malformed missing input from an explicit empty batch. The input-contract owner remains responsible for that policy choice.

## What the checks prove

Focused red proves that the immutable before state leaks `KeyError: 'events'`. The rejected-candidate control proves that `if not data.get("events")` incorrectly classifies an explicit empty list as missing. Focused green proves the exact error contract and the missing-versus-empty distinction. Broader green protects one representative non-empty input and its written summary. The separate top-level run proves that the final package remains green and that both final-state command wrappers execute.

## What the checks do not prove

The captured slice does not prove handling for non-object JSON, non-list `events`, malformed individual events, or the later empty-result repair. The final suite also leaves explicit UTF-8, atomic output, unsafe `type` values, some skipped-event details, summary logging, and output-failure behavior outside its evidence boundary.

Stored historical command output required no post-processing. Color was disabled before the retained final-package test run.

## Independent certification

A separate independent canonical capture review replayed the package from disposable and standalone copies, regenerated the patch, checked minimality, verified printed parity and provenance, and confirmed the human policy boundary. The attributable receipt is `evidence/independent-review.md`.

Active package state is `complete_independently_reviewed`, review status is `completed`, and the final verdict is `Pass`. Default replay rejects that completed stage if the active review status is missing or pending, the verdict is not `Pass`, or the review artifact is missing or checksum-invalid.

`chapter-session.md` remains a current semantic publication excerpt rather than a byte-for-byte mirror of the live chapter. Its contract, patch, commands, outputs, provenance boundary, and policy boundary match the chapter; surrounding inspection wording may differ. The excerpt retains the historical Listing 3.2 label for the patch; the restored active chapter renumbers that same patch as Listing 3.5 after adding the branch listings.
