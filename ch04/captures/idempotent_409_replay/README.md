# Idempotent 409 replay capture

This internal package preserves the Chapter 4 coding-agent session in which a customer importer rejects a `409 Conflict` replay even though the supplied human contract defines that exact response, for the same stable `source_id` and idempotency key, as "already created." Active certification is stage `complete_independently_reviewed`, independent review `completed`, verdict `Pass`; the attributable record is `evidence/independent-review.md`.

The importer was already repaired when the source used for the original capture entered git. The `before/importer.py` fixture is therefore an explicit reconstruction made by removing only the documented `409` acceptance behavior from that checksum-recorded source. `tests/test_importer.py` preserves the focused and broader session checks. The final package keeps local copies of the repaired importer and its maintained seven-test suite. Historical origin is recorded, but replay has no executable dependency on another chapter or the repository root.

## Record and replay

Run from the Chapter 4 final package directory:

```bash
python3 captures/idempotent_409_replay/run_capture.py --record
python3 captures/idempotent_409_replay/run_capture.py
```

Routine replay is non-recording. It verifies the active completed-review stage, `Pass` verdict, attributable review artifact and checksum, runner, before fixture, focused test, patch, documentation, stored evidence, and package-support checksums. It copies the before fixture into `.work/`, reproduces the focused red result, applies the stored patch, regenerates and byte-compares the unified diff, runs focused and broader capture checks, runs the package-local importer suite, compares normalized output and exit statuses, and removes `.work/` on success or failure.

## Dependencies and environment

- Python 3.14.6 and pytest 9.1.1 produced the completed capture.
- The standard `patch` and `diff` command-line tools apply and regenerate the stored unified diff.
- The importer otherwise uses only the Python standard library.
- No network access or API credential is required.

## Selected implementation

The patch changes only the existing success condition in `send_with_retry`:

```python
if result.status < 400 or result.status == 409:
```

This one-line production diff is narrower than adding a general conflict policy or accepting a range through `409`. The function builds only the fixed `/customers` request and always sends the stable key derived from `source_id`, so the explicit equality check remains inside the approved endpoint and identity contract.

## Human-owned policy boundary

The human-owned decision is whether this exact endpoint's `409 Conflict` response for the same stable `source_id` and idempotency key guarantees that the requested customer already exists and is safe to count as sent. The standing author direction authorizes this bounded meaning. It does not authorize treating `409` as success for another endpoint, another identity rule, or a generic conflict handler.

The author did not select a code shape. The coding agent chose the one-line exact-status condition as the strict smallest implementation consistent with the approved boundary.

## Evidence boundary

The focused red check proves that the reconstructed before implementation sends `409` through the generic non-transient error branch. Focused green proves that the one-line patch returns the replay result. The broader seven-test check protects parsing, stable-key derivation, transient retries, a nonretryable `400`, and dry-run behavior. The separate package-support run proves the final package's maintained importer and renamed top-level test remain green.

These checks do not establish the upstream contract, identify the existing resource, prove payload equivalence, or authorize another endpoint's conflicts. Independent review passed after replaying both packages, checking isolation and cleanup, and adversarially verifying the exact-status policy boundary. The shared ledger remains outside this package and is intentionally unchanged.
