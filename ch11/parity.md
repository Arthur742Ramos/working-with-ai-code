# Chapter 11 listing parity

This ledger maps every staged Chapter 11 listing to a package-local maintained source. It covers Listing 11.1, Listing 11.2, Listing 11.3, Listing 11.4, and Listing 11.5. The staged chapter remains the publication authority; this package provides runnable or byte-exact verification without reading that chapter at test time.

| Listing | Printed item | Maintained source | Exact mapping |
|---|---|---|---|
| 11.1 | Rollout-policy branch for unavailable capacity | `deployment_guard.py`, `rollout_violations()` | The printed branch is byte-equivalent after removing the function's four-space indentation. |
| 11.2 | Stopping the pipeline at the approval boundary | `pipeline.py`, `run_stage()` and `run_pipeline()` | The printed functions omit only their one-line docstrings. Signatures, launch-failure handling, statements, ordering, and strings are otherwise exact. |
| 11.3 | Selecting one deployment's events in time order | `incident_triage.py`, `select_timeline()` | The printed function omits only its one-line docstring. Signature, generator, filter, and sort are otherwise exact. |
| 11.4 | A source-linked incident timeline | `incident.jsonl` rendered by `python3 incident_triage.py incident.jsonl deploy-104` | `test_listing_parity.py` compares the complete deterministic command output with the printed text. |
| 11.5 | A post-change evidence packet | `listing_11_5.txt` | The maintained artifact is byte-for-byte identical to the printed packet, including placeholders and final newline. |

## Capture-session mapping

The real-session excerpt maps to `captures/deployment_policy_value/`. Its immutable `before/` configuration retains `max_unavailable: 2`, while top-level `deployment.json` is the green `max_unavailable: 1` state. The capture's focused red, exact patch, focused green, and 24-test broader green evidence remain preserved. `run_capture.py` reproduces those states from package-local files only.

The original canonical-support green artifact remains under `captures/deployment_policy_value/evidence/canonical-support-green.txt` as historical origin provenance. Replay checksum-verifies it but does not locate or execute the original repository-root source. A separately labeled `final-package-green.txt` records the current package-local top-level suite.

## Verification boundary

`test_listing_parity.py` verifies the five listing surfaces without opening the staged chapter. This prevents the final package from depending on repository layout while making publication drift explicit when the package is refreshed. The tests prove maintained parity with the currently staged text; they do not authorize a live deployment or validate the fictional operational thresholds against production traffic.
