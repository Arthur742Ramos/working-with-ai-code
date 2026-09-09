# Chapter 4 final support package

This internal package keeps the staged customer importer, the reconstructed migration case, and the verified idempotent-replay capture together without depending on the repository root or another chapter.

## Contents

The print fences for Listings 4.4 and 4.5 use `python keep-together` to keep
each compact block on one page. This is a converter layout
option, not part of the Python source; it rejects blocks over 40 lines.

- `walking_skeleton.py` is the pre-replay implementation printed across Listings 4.2 through 4.5. It deliberately treats every status at or above `400` as a failure; Section 4.5 adds the endpoint-specific `409` rule.
- `test_skeleton.py` is Listing 4.6, the dry-run discriminator. Run it explicitly with `python3 -m pytest -q test_skeleton.py`; the archival package suite remains unchanged.
- `importer.py` is the green book-state implementation. Its `409` condition matches the exact captured patch printed in the staged chapter.
- `test_importer_package.py` covers parsing, normalization, stable identity, retry behavior, dry run, and the endpoint-specific replay policy. Its distinct module name prevents collision with the capture's retained `tests/test_importer.py`.
- `test_capture_certification.py` runs disposable package copies to enforce `.work/` cleanup after success, preflight failure, and runtime failure. It also enforces the completed independent-review stage, active verdict, attributable artifact, and preserved historical session language.
- `migration_case/` contains the schemas, deterministic fixture, reconstructed migration implementation, tests, parity ledger, and plain-text dry-run evidence checked by exact bytes and SHA-256.
- `captures/idempotent_409_replay/` preserves the immutable red before-state, exact patch, raw evidence, and a replay runner that checks this package's own importer suite.
- `pytest.ini` limits routine top-level collection to the maintained package suites and certification checks. Capture internals run only through `run_capture.py`, where the red state is expected and verified.

## Verify

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q -p no:cacheprovider .

PYTHONDONTWRITEBYTECODE=1 \
python3 -m migration_case.seed

PYTHONDONTWRITEBYTECODE=1 \
python3 -m migration_case.migrate --dry-run

python3 captures/idempotent_409_replay/run_capture.py
```

The top-level suite should report sixteen passing tests: seven importer checks, five migration checks, three cleanup-state checks, and one review-state check. The seed command creates a database with three legacy rows and empty target tables. The migration dry run executes all transformations, reports three upserts and nine audit rows in plain text, then rolls back. Its test rejects Markdown backticks and checks both byte parity and the retained evidence checksum. Replay reproduces the focused red state, applies the one-line patch in disposable space, and verifies focused, broader, and package-support green evidence.

## Provenance and limits

The importer capture originated from a previously maintained Chapter 6 implementation and test, but this final package carries checksum-verified local copies and does not read or execute that chapter. The migration schemas and fixture originated in earlier Chapter 5 support. No historical migration script was retained, so `migration_case/migrate.py` is explicitly a reconstruction from Chapter 4's accepted contract and printed evidence rather than a claimed original artifact.

The importer has no file reader, production network client, command-line interface, logging policy, injected retry clock, or large-file performance check. Its `409` behavior is valid only for the documented endpoint and identity contract. The migration checks prove behavior against three supplied rows; they do not establish production date coverage, stable source identity, concurrency safety, or the human-owned timezone and skip-versus-abort policies.
