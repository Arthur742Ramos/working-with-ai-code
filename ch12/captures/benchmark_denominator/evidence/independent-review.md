# Independent canonical capture review

## Certification

Verdict: **PASS**

No blocking capture, replay, parity, isolation, minimality, provenance, or policy-boundary defect was found. This record preserves the independent review of the canonical Chapter 12 benchmark-denominator package.

## Attribution

- Reviewer role: Independent canonical capture reviewer
- Reviewer tool: Claude Code 2.1.210
- Review date: 2026-07-15
- Method: Read-only review using a disposable package copy and an independently assembled package-local fixture
- Repository modified by reviewer: No
- Attribution limit: The human contract is explicitly condensed and non-verbatim. The transcript is a mixed contemporaneous record. Replay verifies the executable evidence but does not claim to recover an unavailable verbatim conversation log.

## Reviewed authorities

The review covered the canonical package, the real-session capture standard, the active mapping, the canonical and staged Chapter 12 Markdown, and the package-local final-code mirror. The disposable review copy was removed after review.

## Commands executed

Core replay and package checks ran from the disposable Chapter 12 package:

```bash
python3 captures/benchmark_denominator/run_capture.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_workflow_metrics
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest --collect-only -q
```

The reviewer independently reconstructed the state transition from the package-local fixture:

```bash
python3 -m unittest -v \
  test_workflow_metrics.QualitySuccessRateTests.\
test_failed_attempts_remain_in_denominator

patch -p1 -i patches/production.diff

python3 -m unittest -v \
  test_workflow_metrics.QualitySuccessRateTests.\
test_failed_attempts_remain_in_denominator

python3 -m unittest -v test_workflow_metrics
```

The exact patch was regenerated mechanically:

```bash
diff -u \
  --label a/workflow_metrics.py \
  --label b/workflow_metrics.py \
  before/workflow_metrics.py \
  workflow_metrics.py
```

Isolation replay ran with a sanitized environment:

```bash
python_bin=$(command -v python3)
env -i \
  PATH="$(dirname "$python_bin"):/usr/bin:/bin:/usr/sbin:/sbin" \
  HOME=<empty-home> \
  PYTHONDONTWRITEBYTECODE=1 \
  FORCE_COLOR=0 \
  NO_COLOR=1 \
  "$python_bin" \
  captures/benchmark_denominator/run_capture.py
```

## Results

| Check | Result |
|---|---|
| Clean-copy manifest | 21 of 21 files matched |
| Default non-recording replay | Exit 0 |
| Focused red | 1 test, 1 failure, `AssertionError: 1.0 != 0.5`, exit 1 |
| Patch application | Exit 0 |
| Focused green | 1 of 1 passed, exit 0 |
| Broader green | 4 of 4 passed, exit 0 |
| Promoted package green | 4 of 4 passed, exit 0 |
| Top-level pytest | 4 of 4 passed |
| Pytest collection | Exactly 4 tests, none under `captures/` |
| Maintained before-state broader run | 4 tests, 1 expected failure, exit 1 |
| Residual replay work directories | 0 |
| Watched files changed by non-recording replay | 0 of 21 |
| Declared checksum assertions | 16 of 16 matched |
| Final canonical hash recheck | 6 of 6 matched |
| Printed parity assertions | 21 of 21 passed |
| Reader-facing private or internal path hits | 0 |
| External code prerequisite hits | 0 |

## Minimality

The stored patch is the exact regenerated machine diff. It contains one hunk, adds four lines, deletes one line, and changes only the denominator expression. The patched source SHA-256 is `e76cb6640d3e2081fc75604779b1c548416edc6d1247e5eed08666a1af84ef0c`.

Adversarial checks produced these results:

- Stored implementation: 6 of 6 cases passed.
- Dividing by all attempts: 4 of 6 passed because pending and unknown states incorrectly entered the denominator.
- Dividing by all non-pending attempts: 5 of 6 passed because unknown states were incorrectly treated as terminal.
- Counting successes plus failures separately: 6 of 6 passed, but duplicated computation and required either a 107-character line or a larger wrapped edit.

The stored denominator-only expression is the smallest reviewable patch that states the approved terminal-status policy directly.

## Provenance

The package identifies Claude Code 2.1.210 and capture date 2026-07-15. The claimed pre-session commit is `38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6`, and the review confirmed that the chapter and canonical Chapter 12 code were absent from that commit as recorded. Historical source and test matched their retained SHA-256 hashes.

The package does not present reconstructed text as a vendor quotation. The human contract is labeled condensed and non-verbatim, and the transcript is labeled a mixed contemporaneous record. Independent replay verifies the red, exact patch, and green evidence.

## Printed transcript and listing parity

The review found Listing 12.1 byte-identical to the retained before source, Listing 12.2 byte-identical to the focused test excerpt, and Listing 12.3 byte-identical to the stored machine patch. The red assertion, commands, test names, counts, timing, green results, and exit statuses matched the package under the disclosed condensation. Canonical and staged Chapter 12 Markdown were byte-identical at review time.

## Policy boundary

The evidence proves only that explicit `succeeded` and `failed` attempts belong in the denominator for the maintained examples. It does not validate `0.80` as a production threshold, classify additional statuses, establish sample representativeness, prove operational safety, or authorize standardization or rollout.

Threshold acceptance, status taxonomy, representative scope, and rollout remain owned by the human workflow owner.

## Isolation

Replay succeeded from a copy containing only the Chapter 12 package and also under a sanitized environment. No executable file depends on the restructuring tree, the historical support package, chapter prose, repository-root paths, or user-specific absolute paths. Historical paths occur only in metadata provenance fields. No network, provider command, cloud credential, or target-system write was required.

The final-code Chapter 12 mirror was byte-identical to the canonical package at review time. The shared session ledger still pointed to the historical support tree, but that was a publication-control follow-up rather than an executable package blocker and was outside this integration scope.

## Final certification

**PASS**
