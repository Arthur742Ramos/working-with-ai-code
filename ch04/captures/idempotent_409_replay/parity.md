# Parity ledger

Capture status: implementation and evidence complete. The historical session record remains explicit about reconstruction; this final copy removes executable coupling while retaining the origin account.

Stage: `complete_independently_reviewed`; independent review: `completed`; status: `Pass`.

| Printed item | Package source | Verification |
|---|---|---|
| Filename | `importer.py` | The chapter-facing name matches the staged before and disposable after state |
| Importer excerpt | `before/importer.py`, `send_with_retry`, plus `patches/idempotent_409_replay.patch` | Before state is checksum-verified; after state is recreated only in disposable space |
| Focused test | `tests/test_importer.py::test_conflict_is_idempotent_replay` | Retained capture test; the final package test has a distinct module name to avoid collection collision |
| Red command and output | `metadata.json`, `evidence/focused-red.txt` | Genuine capture output, exit status `1`; replay remains intentionally red before patching |
| One-sentence plan and approval basis | `session.md` | Recorded before the implementation edit without claiming an author-selected syntax |
| Exact diff | `patches/idempotent_409_replay.patch` | Machine-generated one-line replacement, SHA-256 recorded in metadata |
| Focused green | `evidence/focused-green.txt` | Genuine capture output, exit status `0` |
| Broader capture green | `evidence/broader-green.txt` | Genuine seven-test capture output, exit status `0` |
| Final package support green | `evidence/package-support-green.txt` | Package-local renamed importer test, seven tests passed, exit status `0` |
| Human policy boundary | `README.md` and `session.md` | The supplied human contract accepts `409` only for the exact endpoint and stable identity; repository evidence does not establish upstream behavior |
| Independent review | `evidence/independent-review.md` and `metadata.json` | Attributable clean-state review completed on 2026-07-15 with verdict `Pass`; replay verifies artifact locality and checksum |

## Intentional reconstruction and formatting

The before importer is not claimed as a retained historical blob. It was reconstructed by removing only the documented `409` acceptance behavior from the source used during the original session. The final package preserves that origin as provenance but does not read or execute the other chapter where the source was once maintained.

Raw red output and exact exit status remain retained. Replay compares normalized copies that mask only Python function memory addresses and pytest elapsed times. Markdown line wrapping in `session.md` changes presentation only; the command arguments, failure location, diff content, test counts, and exit statuses match the stored artifacts.

## Package locality

`run_capture.py` resolves the Chapter 4 final package from its own location. It validates `importer.py` and `test_importer_package.py` beside that package, never searches for a repository root, and never imports or runs another chapter. The package-level `pytest.ini` excludes `captures/` from routine collection, while replay invokes the capture test explicitly.

## Independent review certification

The first independent clean-state review confirmed the one-line endpoint-specific patch, neighboring retry behavior, Chapter 4 transcript parity, package isolation, and the human-owned conflict policy boundary. Certification still failed because preflight failure could leave stale `.work/` residue and the active package overstated its review status.

The runner now removes `.work/` after success, argument failure, malformed metadata, checksum preflight failure, and runtime failure after work creation. A second independent reviewer replayed the repaired canonical and mirrored packages from clean disposable copies, verified identical manifests, confirmed all policy-boundary and printed-parity checks, and issued verdict `Pass`. The attributable record is `evidence/independent-review.md`.

`session.md` preserves the historical pending-review language that was accurate when the coding-agent capture was assembled. Current certification is carried by this parity record, `metadata.json`, `README.md`, and the checksum-bound independent review artifact. The shared session ledger remains outside this package and was not edited.
