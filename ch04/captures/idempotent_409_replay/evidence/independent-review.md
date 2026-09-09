# Independent Chapter 4 capture review

## Certification

Verdict: **PASS**

No blocking or non-blocking package defect survived verification. This record certifies the canonical Chapter 4 `idempotent_409_replay` capture package and its mirrored final-code package.

## Attribution

- Reviewer role: Independent capture certification reviewer
- Reviewer tool: Claude Code 2.1.210
- Review date: 2026-07-15
- Runtime: Python 3.14.6 and pytest 9.1.1
- Review mode: Clean disposable copies of the canonical and mirrored packages
- Repository modified by reviewer: No
- Attribution limit: This package preserves the supplied independent review report. Raw vendor session logs are not retained here.

## Results

| Gate | Result |
|---|---|
| Canonical non-recording replay | PASS |
| Mirrored non-recording replay | PASS |
| Focused red | PASS: exit 1, expected `RuntimeError` at `.work/importer.py:83` |
| Exact patch | PASS: one removed line, one added line, byte-identical regenerated diff |
| Focused green | PASS: 1 passed |
| Broader green | PASS: 7 passed |
| Package-support green | PASS: 7 passed |
| Full canonical package | PASS: 16 passed |
| Full mirrored package | PASS: 16 passed |
| Cleanup | PASS for success, argument failure, malformed metadata, checksum preflight failure, and runtime failure after work creation |
| Isolation | PASS: both packages ran outside the repository with no external support dependency |
| Canonical-to-mirror parity | PASS: identical 35-file manifests |
| Recorded checksums | PASS: all 23 metadata-bound files matched |
| Migration evidence | PASS: exact output and SHA-256 `a54895f15f960161be8eb8e82733fc3dedfb3aa5ae9fad31c6f63a2f68af3a58` |
| Historical session | PASS: SHA-256 `ca829a8a4299495930be75f6d0a17d2f8993151f3f6e9da58e2a89159700aef6` |
| Minimality | PASS: exact one-line condition change |
| Policy boundary | PASS: only `409` returns among statuses 400 through 410 |
| Source parity | PASS: canonical and staged Chapter 4 Markdown were byte-identical |
| Printed parity | PASS: exact patch and required evidence appeared in both Word deliverables |
| Compilation and spelling | PASS |
| Runtime residue | PASS: no `.work/`, `shop.db`, SQLite, or cache residue covered by the gate |

The file and checksum counts above describe the package state reviewed before this certification artifact was integrated. The active package now contains this additional checksum-bound review file.

## Principal commands

The reviewer ran the following operations from disposable copies. Machine-specific roots are represented by variables.

```bash
python3 "$CANONICAL_COPY/captures/idempotent_409_replay/run_capture.py"
python3 "$MIRROR_COPY/captures/idempotent_409_replay/run_capture.py"

PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q -p no:cacheprovider "$CANONICAL_COPY"

PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest -q -p no:cacheprovider "$MIRROR_COPY"
```

The focused replay sequence used the immutable before fixture, applied the stored patch, regenerated the exact diff, and reran the focused and broader tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.work \
python3 -m pytest -q --color=no -p no:cacheprovider \
tests/test_importer.py::test_conflict_is_idempotent_replay

patch -s -p1 -i patches/idempotent_409_replay.patch

diff -u --label a/importer.py --label b/importer.py \
before/importer.py .work/importer.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.work \
python3 -m pytest -q --color=no -p no:cacheprovider \
tests/test_importer.py
```

The reviewer also reproduced the migration evidence and ran compilation and spelling checks against both packages.

## Findings

- No blocking or non-blocking package defect survived verification.
- The patch is behaviorally minimal. Statuses `400` through `408` and `410` still raise; only `409` returns.
- The patched capture function and focused test match their package-local green equivalents at the abstract syntax tree level.
- Provenance correctly labels the before fixture and bounded chapter contract as reconstructions. It does not claim a retained historical pre-repair blob.
- The shared session ledger correctly maps Chapter 4 to this capture package.
- The shared ledger and package records were intentionally pending during the review. That state was not treated as a negative verdict and was not edited by the reviewer.
- The disposable review copies were removed after verification.

## Final certification

**PASS**
