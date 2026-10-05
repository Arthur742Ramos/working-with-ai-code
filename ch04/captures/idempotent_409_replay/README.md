# Idempotent 409 replay capture

This internal package preserves a Chapter 4 coding-agent session in which a customer
importer rejects a `409 Conflict` replay. The supplied human contract defines that
exact response for the same stable `source_id` and idempotency key as "already
created." Active certification is stage `complete_independently_reviewed`,
independent review `completed`, verdict `Pass`. The attributable record is
`evidence/independent-review.md`.

The importer was already repaired when the source used for the original capture
entered git. To reconstruct the before-state, the `before/importer.py` fixture
removes only the documented `409` acceptance behavior from that checksum-recorded
source. `tests/test_importer.py` preserves the focused and broader session checks.
The final package keeps local copies of the repaired importer and its maintained
seven-test suite. The historical origin is recorded. Replay runs without another
chapter or the repository root.

## Record and replay

Follow the isolated pytest setup in the [Chapter 4 guide](../../README.md#set-up-an-isolated-test-environment).
Run routine replay from `ch04/` (the final package directory):

```bash
python3 captures/idempotent_409_replay/run_capture.py
```

From this capture directory, the equivalent command is `python3 run_capture.py`.
Use `python3 run_capture.py --record` only when intentionally replacing
evidence after reviewing the fixture, tests, patch, and environment. Recording
overwrites raw and normalized historical output; it is not a remedy for
unexpected replay drift.

Routine replay is non-recording. It verifies the active completed-review stage,
`Pass` verdict, attributable review artifact and checksum, runner, before fixture,
focused test, patch, documentation, stored evidence, and package-support checksums.

The runner copies the before fixture into `.work/` and reproduces the focused red
result. It applies the stored patch, regenerates the unified diff, and compares
that diff byte for byte. It then runs focused and broader capture checks and the
package-local importer suite, comparing normalized output and exit statuses.
It removes `.work/` on success or failure.

Successful replay prints `RED EXIT STATUS: 1` and a `RuntimeError` from the
before-state, followed by `PATCH VERIFIED`, three green exit statuses of 0,
and `PARITY VERIFIED`; its own exit status is 0. The patch repairs the
before-state failure. A nonzero runner exit is a replay
failure, even if the expected red traceback appears in its diagnostic.

## Dependencies and environment

- Python 3.14.6 and pytest 9.1.1 produced the completed capture.
- The standard `patch` and `diff` command-line tools apply and regenerate the stored unified diff.
- The importer otherwise uses only the Python standard library.
- No network access or API credential is required.

The runner normalizes only hexadecimal function addresses and pytest elapsed
times. It does not normalize traceback layout or path separators. Different
Python/pytest versions and platforms can therefore fail exact output matching
despite the same importer behavior. Preserve the retained evidence and inspect
output drift separately from the expected red-to-green behavior.

## Selected implementation

The patch changes only the existing success condition in `send_with_retry`:

```python
if result.status < 400 or result.status == 409:
```

The one-line production diff adds no general conflict policy or success range
through `409`. The function builds only the fixed `/customers` request and always
sends the stable key derived from `source_id`. The equality check stays within the
approved endpoint and identity contract.

## Human-owned policy boundary

The human-owned decision is whether this exact endpoint's `409 Conflict` response for the same stable `source_id` and idempotency key guarantees that the requested customer already exists and is safe to count as sent. The standing author direction authorizes this bounded meaning. It does not authorize treating `409` as success for another endpoint, another identity rule, or a generic conflict handler.

The author did not select a code shape. The coding agent chose the one-line
exact-status condition as the smallest implementation within the approved boundary.

## Evidence boundary

The focused red check shows that the reconstructed before implementation sends
`409` through the generic non-transient error branch. Focused green checks that the
one-line patch returns the replay result. The broader seven-test check covers
parsing, stable-key derivation, transient retries, a nonretryable `400`, and dry-run
behavior. The separate package-support run verifies that the final package's
maintained importer and renamed top-level test remain green.

These checks do not establish the upstream contract, identify the existing
resource, prove payload equivalence, or authorize another endpoint's conflicts.
Independent review passed after replaying both packages, checking isolation and
cleanup, and adversarially verifying the exact-status policy boundary. The shared
ledger remains outside this package and is intentionally unchanged.
