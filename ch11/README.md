# Chapter 11 final support package

This internal package keeps the green deployment-policy example, operational fixtures, listing-parity checks, and the verified `max_unavailable` capture together. It runs without the repository root, staged chapters, canonical support files, or another chapter package.

## Files

- `deployment_guard.py` contains the complete policy, approval-surface, and post-change verification implementation. Its unavailable-capacity branch matches Listing 11.1 exactly after removing function indentation.
- `deployment.json` is the green book state. Its six-replica rollout sets `max_unavailable` to `1`.
- `pipeline.py` preserves launched child exit codes, reports a launch error with `tool_error` and exit `127`, and stops before the production write boundary. Its two printed functions map to Listing 11.2.
- `incident_triage.py` builds the bounded selector in Listing 11.3 and renders `incident.jsonl` as the exact Listing 11.4 timeline.
- `listing_11_5.txt` is the maintained byte-exact post-change evidence packet for Listing 11.5.
- `observation.json` supplies generic post-change facts used by verification.
- `test_deployment_guard.py`, `test_incident_triage.py`, and `test_pipeline.py` preserve the 24 operational checks used by the captured broader run.
- `test_listing_parity.py` adds five checks, one for each staged listing.
- `parity.md` records exact source, excerpting, formatting, command-output, and artifact mappings for Listings 11.1 through 11.5.
- `pytest.ini` prevents top-level pytest discovery from collecting the intentionally red capture test.
- `captures/deployment_policy_value/` preserves the immutable red before-state, focused test, exact one-line patch, raw evidence, and package-local replay runner.

## Verify the final implementation

Run from this directory:

```bash
python3 -m pytest -q -p no:cacheprovider
```

The expected result is 29 passing tests: 24 operational tests plus five listing-parity checks. Pytest does not collect capture internals during this run.

Run the read-only operational examples with:

```bash
python3 deployment_guard.py plan deployment.json
python3 deployment_guard.py verify \
  deployment.json observation.json
python3 incident_triage.py incident.jsonl deploy-104
python3 pipeline.py
```

The pipeline stops at `READY_FOR_APPROVAL`. It performs no production write, provider-native plan, approval lookup, credential exchange, target query, verification, or recovery action. Its test stage runs the 24 operational checks; the five listing-parity checks remain a separate package and publication gate.

## Replay the captured repair

Run from this directory:

```bash
python3 captures/deployment_policy_value/run_capture.py
```

Replay reconstructs the disposable red and repaired states from files inside this package, compares focused red, exact patch, focused green, and 24-test broader green with stored evidence, then runs all 29 top-level package tests. It verifies package-local checksums and removes temporary work on success or failure. Default replay does not rewrite evidence.

The original 24-test canonical-support output remains in `evidence/canonical-support-green.txt` as historical origin provenance. Replay checksum-verifies that artifact but does not locate or execute the original repository-root files. The separately labeled `evidence/final-package-green.txt` records the current package-local suite.

## Verify isolation

A copied package supports the same commands:

```bash
cp -R . /tmp/ch11-final
cd /tmp/ch11-final
python3 -m pytest -q -p no:cacheprovider
python3 captures/deployment_policy_value/run_capture.py
```

No command needs the source repository after the copy finishes.

## Remaining limitations

- The package makes no cloud call, issues no live credential, and changes no target system.
- The small release driver does not generate a provider-native plan, read an approval record, or execute provider-side Apply, Verify, or Recovery jobs.
- A launched child preserves its own exit code; a launch failure has no child exit and returns `127` with a `tool_error` record.
- The verifier returns policy block `2` before observation, input/tool error `1` for unreadable or malformed input, and verification failure `3` for failed loaded postconditions.
- A failed loaded postcondition emits `recovery=REQUESTED`; the marker is a request, not recovery authorization.
- The rollout thresholds are teaching decisions, not universal production defaults.
- The tests do not prove that five replicas can carry live traffic or preserve rollback headroom.
- Repository policy checks do not detect target drift or replace a provider-native plan.
- The observation and incident fixtures do not exercise live telemetry, approval systems, deployment controllers, or rollback execution.
- The capture proves only the bounded configuration repair and its maintained regression surface.
