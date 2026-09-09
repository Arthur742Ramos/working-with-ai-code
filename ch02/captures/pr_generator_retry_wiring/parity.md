# Parity map

## Promoted chapter implementation

| Printed or maintained item | Package-local source | Status |
|---|---|---|
| Fixed diff and deterministic response | `../../local_fixture.py` | Matches the staged offline listing |
| Output schema | `../../schema.py` | Matches the staged schema-only contract |
| Finished generator | `../../pr_generator.py` | Uses `jsonschema`, the local fixture, and the bounded retry in the CLI |
| Optional live-provider boundary | `../../anthropic_adapter.py` | Accepts only `end_turn` and classifies other stop reasons before content use |
| Green package suite | `../../test_pr_generator.py` | Exercises fixture, schema, nested lengths, checklist, retry, renderer, CLI, and provider stop reasons |
| Test collection boundary | `../../pytest.ini` | Collects only the green top-level suite and excludes `captures/` |
| Isolated replay copy | `run_capture.py` | Copies the package into `.package-work/` and runs the suite there |

## Historical captured repair

| Printed or captured item | Maintained source | Status |
|---|---|---|
| Historical filename | `before/pr_generator.py` and `after/pr_generator.py` | Immutable origin artifacts |
| Production excerpt | Command-line call inside `after/pr_generator.py` | One-line captured repair |
| Existing retry helper | `generate_with_retry()` in both states | Byte-identical; not edited by the captured repair |
| Focused test name | `test_cli_retries_after_malformed_json` in `tests/focused_test.py` | Genuine red and focused green |
| Broader test names | Three checks in `tests/broader_test.py` | Genuine broader green |
| Focused red command | `metadata.json`, `red.command`, `session.md`, and the chapter transcript | Printed exactly as executed against the disposable before state |
| Red output | `evidence/focused-red.txt` | Raw output, with exit status in `focused-red.exit` |
| One-sentence plan | `session.md`, Strict-smallest-change plan | Recorded before the production edit |
| Approval basis | `session.md`, Approval basis | Standing direction plus agent-selected bounded policy |
| Agent action record | `evidence/agent-actions.md` | Observable action sequence retained |
| Exact diff | `patches/pr_generator_retry_wiring.patch` | Machine-generated one-line unified diff |
| Focused green output | `evidence/focused-green.txt` | Raw output, with exit status in `focused-green.exit` |
| Broader green output | `evidence/broader-green.txt` | Raw output, with exit status in `broader-green.exit` |
| Human policy boundary | `README.md` and `session.md` | Retry classes and retry budget remain human-owned |
| First independent review | `evidence/first-independent-review.md` and `metadata.json` | Original verdict `Fail`; all three findings and their resolved disposition remain checksum-locked historical evidence |
| Active independent review | `evidence/independent-review.md` and `metadata.json` | Separate read-only review completed with verdict `Pass` after canonical and mirror replay, patch regeneration, isolation, cleanup, provenance, and publication-parity checks |
| Final-polish recertification | `evidence/final-polish-recertification.json` and `metadata.json` | Separately certifies 18 promoted-package tests, the applicable listing patch, current support checksums, and unchanged historical artifacts |
| Review-state gate | `run_capture.py` and `metadata.json` | `complete_independently_reviewed` requires completed active status, verdict `Pass`, no findings, checksum-valid review receipts, and the separate final-polish recertification |
| Cleanup gate | `run_capture.py` | Replay removes its disposable work and rejects generated cache or bytecode residue |
| Origin support provenance | `metadata.json`, `origin_support_checksums` | Historical checksums retained as provenance only |
| Origin chapter provenance | `metadata.json`, `origin_chapter_checksums` | Historical checksums retained as provenance only |

## Intentional excerpting and formatting

The chapter-facing transcript may omit package paths, fixture setup, checksum operations, and runner mechanics. It preserves the exact focused command, test names, red output, complete byte-exact patch (including the one-space blank context line), focused green output, broader green output, and human-owned policy boundary.

The capture's focused and broader harnesses keep deterministic stand-ins for the live adapter and third-party validator used during the original session. They are immutable reproduction mechanisms, not the promoted reader-facing implementation. The final package's top-level suite validates the offline fixture and standards-compliant validator directly. No capture output normalization was applied.

## Active certification

Stage is `complete_independently_reviewed`, active review status is `completed`, and verdict is `Pass`. `session.md` preserves the historical capture and first-review-repair language that was accurate when written. Current certification is carried by this parity map, `README.md`, `metadata.json`, `run_capture.py`, the checksum-bound active receipt, and the separate final-polish recertification. The shared ledger remains outside the package and was not edited.
