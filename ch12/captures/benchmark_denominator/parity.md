# Capture parity ledger

| Printed or recorded item | Final package source | Parity status |
|---|---|---|
| Green `quality_success_rate` implementation | `workflow_metrics.py` | Matches the checksum-verified patched after-state |
| Maintained four-test suite | `test_workflow_metrics.py` | Contains the complete behavior suite; the staged chapter prints the focused test and invokes the `test_workflow_metrics` module without claiming the `.py` filename |
| Top-level test discovery | `pytest.ini` | Collects only the maintained top-level test module and excludes `captures/` |
| Defective before-state | `before/workflow_metrics.py` | Preserves the verified red implementation |
| Focused denominator test | `tests/test_workflow_metrics.py` | Byte-identical to the top-level maintained test suite |
| Human contract and action record | `session.md` | Retained capture-time record, condensed where explicitly labeled |
| Red output and exit | `evidence/focused-red.txt` and `.exit-status` | Raw `unittest` failure with `1.0 != 0.5`, exit 1 |
| Exact repair | `patches/production.diff` | Machine-generated denominator-only diff, checksum-locked |
| Focused green output and exit | `evidence/focused-green.txt` and `.exit-status` | Raw one-test success, exit 0 |
| Broader green output and exit | `evidence/broader-green.txt` and `.exit-status` | Raw four-test success, exit 0 |
| Threshold behavior | `test_successes_are_checked_for_quality` | Protected by broader green |
| Pending-attempt exclusion | `test_pending_attempts_are_excluded` | Protected by broader green |
| Empty-terminal behavior | `test_no_terminal_attempts_returns_zero` | Protected by broader green |
| Replay integrity | `run_capture.py` | Reproduces red and green states using package-local inputs without mutating the green source or stored evidence |
| Independent certification | `evidence/independent-review.md` | Separate final-package review completed with verdict Pass after clean replay, minimality, provenance, isolation, printed-parity, and policy-boundary checks |
| Review gate | `run_capture.py`, `metadata.json`, and `evidence/independent-review.md` | `complete_independently_reviewed` is rejected unless active review status is `completed`, verdict is `Pass`, and the package-local review artifact exists with its recorded checksum |
| Record integrity | `run_capture.py` and `metadata.json` | The completed package checksum-locks the runner, README, parity ledger, session record, and independent-review receipt |
| Origin provenance | `metadata.json`, `origin_provenance` | Retains the original repository paths and hashes as historical facts; replay neither resolves nor verifies those paths |
| Human policy boundary | `README.md`, `metadata.json`, `session.md`, and `evidence/independent-review.md` | `0.80` remains provisional and rollout is not authorized |

## Publication mapping

The staged chapter names `workflow_metrics.py`, the `test_workflow_metrics` module in its commands, `QualitySuccessRateTests`, and `test_failed_attempts_remain_in_denominator`. Those names match this package. The `.py` suffix on the package's maintained test file is an internal filename, not a filename claim made by the chapter. Its defective source, discriminating test, exact patch, focused outputs, and four-test broader output match the captured session.

The chapter presents the defective implementation and focused test as complete listings, then presents the exact repair as a diff. The final package preserves the full runnable green implementation and all four tests rather than reducing the files to printed excerpts.

## Evidence boundary

The capture proves the explicit `succeeded` and `failed` denominator behavior for the maintained examples. It does not validate the provisional threshold, classify new statuses, establish benchmark representativeness, or authorize rollout. Those decisions remain with the workflow owner.
