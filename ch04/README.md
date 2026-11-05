# Chapter 4 final support package

This internal package keeps the staged customer importer, the reconstructed migration case, and the verified idempotent-replay capture together without depending on the repository root or another chapter.

## Contents

The print fences for Listings 4.4, 4.5, 4.9, and 4.10 use `python keep-together` to keep
each compact block on one page. This is a converter layout
option, not part of the Python source; it rejects blocks over 40 lines.

- `walking_skeleton.py` is the pre-replay implementation printed across Listings 4.2 through 4.5. It deliberately treats every status at or above `400` as a failure; Section 4.5 adds the endpoint-specific `409` rule.
- `test_skeleton.py` is Listing 4.6, the dry-run discriminator. Run it explicitly with `python3 -m pytest -q test_skeleton.py`; the archival package suite remains unchanged.
- `teaching/idempotency_probe.py` sends a create, a verified replay, and a conflicting payload to two local HTTP fixtures. Both reject the changed payload, even when its status is `409`. The server computes its receipt from the stored request only after matching the payload. These fixtures do not establish a real service contract.
- `importer_current.py` is the maintained implementation after the capture. It requires the endpoint-owned JSON replay signal, matching key, and request fingerprint shown in Listings 4.9 and 4.10. Use this module for new experiments. `test_importer_current.py` covers rejection, retry, and counting behavior.
- `importer.py` is the archival green book-state implementation, not the maintained sender. Its `409` condition matches the exact captured patch printed in the staged chapter.
- `test_importer_package.py` covers parsing, normalization, stable identity, retry behavior, dry run, and the endpoint-specific replay policy. Its distinct module name prevents collision with the capture's retained `tests/test_importer.py`.
- `test_capture_certification.py` runs disposable package copies to enforce `.work/` cleanup after success, preflight failure, and runtime failure. It also enforces the completed independent-review stage, active verdict, attributable artifact, and preserved historical session language.
- `migration_case/` contains the schemas, deterministic fixture, reconstructed migration implementation, tests, parity ledger, and plain-text dry-run evidence checked by exact bytes and SHA-256.
- `captures/idempotent_409_replay/` preserves the immutable red before-state, exact patch, raw evidence, and a replay runner that checks this package's own importer suite.
- `pytest.ini` limits routine top-level collection to the maintained package suites and certification checks. Capture internals run only through `run_capture.py`, where the red state is expected and verified.

## Try the local idempotency probe

From `ch04/`, run:

```bash
python3 teaching/idempotency_probe.py
python3 -m pytest -q -p no:cacheprovider teaching/test_idempotency_probe.py
```

The first local server returns `409` only for an identical replay and
`422` for a changed payload. The second returns `409` for both cases:
the maintained importer rejects the conflicting payload because it lacks a verified replay signal.
These loopback servers demonstrate why the real endpoint's contract and a
service-level integration test still matter.

## Set up an isolated test environment

Start in `ch04/`, the directory containing this README. The tests and capture
runner require pytest. Python 3.14.6 and pytest 9.1.1 produced the retained
capture; use that pair when reproducing its exact transcript.

```bash
python3 -m venv ../.venv-ch04
source ../.venv-ch04/bin/activate
python3 -m pip install pytest==9.1.1
```

Keep the environment beside `ch04/` so it stays out of certification's
disposable package copies. Capture replay also requires the `patch` and `diff`
command-line tools on `PATH`.

In PowerShell, create the environment with `py -m venv ..\.venv-ch04` and
install with `..\.venv-ch04\Scripts\python.exe -m pip install pytest==9.1.1`.
Use that interpreter in place of `python3` below; activation is optional. For
the bash command groups below, PowerShell users can set
`$env:PYTHONDONTWRITEBYTECODE = '1'` once, then run each Python command without
the bash environment prefix and `\` continuation.

## Verify

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q -p no:cacheprovider

PYTHONDONTWRITEBYTECODE=1 \
python3 -m migration_case.seed

PYTHONDONTWRITEBYTECODE=1 \
python3 -m migration_case.migrate --dry-run

python3 captures/idempotent_409_replay/run_capture.py
```

The top-level suite includes the original sixteen archival and migration checks, plus the maintained importer checks and two loopback contract tests. Run `test_skeleton.py` separately as above. The seed command creates a database with three legacy rows and empty target tables. The migration dry run executes all transformations, reports three upserts and nine audit rows in plain text, then rolls back. Its test rejects Markdown backticks and checks both byte parity and the retained evidence checksum.

Replay separately reproduces the deliberately failing before-state. A successful
run prints `RED EXIT STATUS: 1`, verifies the one-line patch, then reports zero
exit status for the focused, broader, and package-support green checks and
`PARITY VERIFIED`. The runner itself exits 0.

Replay compares retained pytest output exactly after masking only function
addresses and elapsed times. A different Python or pytest version or platform
can change traceback formatting and cause output drift, including in the
successful-replay cleanup test. Treat a nonzero runner exit or a failed
top-level test as a verification failure and inspect the diagnostic. See the
[capture guide](captures/idempotent_409_replay/README.md) for the recorded
environment; do not use `--record` to make a failing replay pass.

## Provenance and limits

The importer capture originated from a previously maintained Chapter 6 implementation and test, but this final package carries checksum-verified local copies and does not read or execute that chapter. The migration schemas and fixture originated in earlier Chapter 5 support. No historical migration script was retained, so `migration_case/migrate.py` is explicitly a reconstruction from Chapter 4's accepted contract and printed evidence rather than a claimed original artifact.

The importer has no file reader, production network client, command-line interface, logging policy, injected retry clock, or large-file performance check. The archival sender accepts every `409`; it is retained only to reproduce the historical session. The maintained sender fails closed unless its explicit replay signal matches. That signal still depends on a verified endpoint contract and a trusted transport. It is not a cryptographic receipt or proof of production correctness. The migration checks prove behavior against three supplied rows; they do not establish production date coverage, stable source identity, concurrency safety, or the human-owned timezone and skip-versus-abort policies.

## Replay contract after the capture

The endpoint must atomically associate a successful POST to `/customers` with
its idempotency key and stored payload. Only an identical replay may receive
`409` with exactly `code`, `key`, and `request_sha256` fields, where `code` is
`idempotent_replay`. The SHA-256 input is UTF-8 JSON of `method`, `path`, and
`json`, serialized with sorted keys, compact separators, ASCII escaping, and
nonfinite values forbidden. This deliberately small schema rejects extra
fields too; coordinate any schema change with the client. The fingerprint
covers every normalized payload field, not just `source_id`.

Loopback tests use a lock and an in-memory record to demonstrate the contract.
They do not establish durable storage, authentication, retention, concurrency
across instances, or the semantics of a real endpoint. Validate those with the
service owner before integrating. The capture directory, original importer,
and its checksum-pinned tests remain byte-for-byte historical evidence.
