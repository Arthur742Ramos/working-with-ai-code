# Event processor capture parity

This ledger maps the single captured repair and the reconstructed-review framing to the isolated final package while preserving the original red evidence.

| Item | Maintained source | Parity status |
|---|---|---|
| Reconstructed review boundary | `chapter-session.md` provenance | The broader review is reconstructed; only the missing-events repair is captured |
| Before filename | `before/event_processor.py` | Preserves the inspected red state |
| Human contract | `session.md`, section 1 | Explicitly reconstructed and bounded to missing versus explicitly empty `events` |
| Historical focused tests | `tests/focused_test.py` | Check the exact error and reject conflating missing input with an empty list |
| Focused red | `evidence/focused-red.txt` | Genuine output with exit status `1` |
| Rejected candidate | `evidence/discriminating-control.txt` | Proves `if not data.get("events")` fails the explicit-empty distinction |
| Exact patch | `patches/event_processor.diff` | Machine-generated four-line guard with no deletions |
| Historical focused green | `evidence/focused-green.txt` | Genuine output with exit status `0` |
| Historical broader green | `evidence/broader-green.txt` | Protects missing, explicit-empty, and one non-empty happy path |
| Printed focused command shape | package-root `focused_test.py` | Executable against a named module; final-state expectations are green |
| Printed broader command shape | package-root `full_capture_check.py` | Executable against a named module; verifies one written happy path |
| Top-level discovery | package-root `pytest.ini` | Collects `test_event_processor.py` and excludes `captures/` |
| Final-package green | `evidence/canonical-support-green.txt` | Eight maintained tests pass with color disabled before execution |
| Publication excerpt | `chapter-session.md` | Preserves current provenance, exact patch, historical output, and evidence boundary |
| Final implementation | package-root `event_processor.py` | Checksum-pinned green final state |
| Final tests | package-root `test_event_processor.py` | Checksum-pinned behavior and wrapper regression suite |
| Final independent certification | `evidence/independent-review.md` | Separate canonical review completed with verdict Pass after replay, patch regeneration, minimality, provenance, isolation, printed-parity, and policy-boundary checks |
| Review gate | `run_capture.py`, `metadata.json`, and `evidence/independent-review.md` | `complete_independently_reviewed` is rejected unless the active review is `completed`, its verdict is `Pass`, and the package-local artifact exists with its recorded checksum |
| Human policy boundary | `session.md`, sections 6 and 12; `evidence/independent-review.md` | Missing is malformed; explicit empty has empty-batch meaning; contract ownership remains human |
| Publication excerpt status | `chapter-session.md` and `metadata.json` | Current semantic excerpt: evidentiary content matches the live chapter while surrounding provenance and inspection wording need not be byte-identical |

## Historical output versus final commands

The transcript's `python3 focused_test.py event_processor.py` and `python3 full_capture_check.py event_processor.py` commands were run before and after the bounded guard in a disposable historical state. The package-root wrappers preserve those command shapes for the final module. They do not pretend that the final module still contains the later zero-average defect.

`run_capture.py` is the authority for reproducing the historical red, exact patch, focused green, and broader green. The package-root wrappers are the authority for showing that the same command names execute against the final green implementation without reaching into the capture directory.

## Intentional formatting

The chapter prints only the focused and broader commands, exact diff, stable output, and evidence-bound inspection. Checksums, replay mechanics, the rejected-candidate construction, and the separate final-package command remain internal.

The focused, negative-control, and broader historical outputs are stored without edits. The retained top-level output was recorded with color disabled before execution. Timing is absent because `pytest -qq` did not print it.

The printed diff omits no changed line from `patches/event_processor.diff`. The explicit-empty historical result proves only that the bounded guard does not reject an empty batch as missing. It does not claim that the captured slice repairs the later zero-average defect.

## Review state

Active package state is `complete_independently_reviewed`, review status is `completed`, and verdict is `Pass`. The independent receipt is attributable final-package evidence; the earlier capture and inspection language in `session.md` remains historical.

Immutable replay compares the fixture, capture tests, patch, outputs, exit statuses, final-package checksums, publication excerpt, and active review receipt. It runs entirely inside this package. The readable guard remains the narrowest behaviorally complete patch in the captured surrounding style.
