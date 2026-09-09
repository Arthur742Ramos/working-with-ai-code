# First independent canonical capture review

## Outcome

The first independent review returned `Fail` on 2026-07-15. This receipt preserves that result and its repair boundary. It is not a Pass certification.

- Reviewer role: Independent canonical capture reviewer, read-only
- Reviewer tool: Claude Code 2.1.210.814
- Reviewer model: `gpt-5.6-sol[1m]`
- Review method: Canonical package replay and adversarial checks in disposable copies
- Repository modified by reviewer: No
- Original verdict: `Fail`

## Canonical package results

The reviewer found the canonical `pr_generator_retry_wiring` package executable and internally consistent:

- Metadata-bound checksums: 27 of 27 matched.
- Before-state checksums: 3 of 3 matched.
- Recreated after-state checksums: 3 of 3 matched.
- Package `unittest` suite: 12 of 12 passed.
- Package `pytest` suite: 12 of 12 passed.
- Minimal isolated suite: 12 of 12 passed.
- Broader capture checks: 3 of 3 passed.
- Canonical and final-code mirror comparison: no differences across 29 files.
- The machine-generated patch was the exact one-line substitution and was the smallest behaviorally complete repair.

The focused red exited `1` after one chat call. Applying the stored patch succeeded. Focused green exited `0` after two chat calls. Broader green exited `0` and protected first-response success, schema-feedback retry, and bounded exhaustion.

## Blocking findings from the first review

1. The active publication mapping pointed to a stale historical support package and labeled it Pass. That mapped replay depended on repository-root files and failed against the current support package.
2. The chapter printed the genuine focused red output without the exact focused-test command that generated it.
3. The chapter's printed patch lost the stored patch's single space on one blank context line, so the claim that the complete patch was unaltered was not byte-exact.

## Repair disposition

- The shared publication mapping now points to this canonical package and is intentionally `Pending`. This package does not treat that Pending state as a replay failure and does not modify the shared ledger.
- The canonical and staged chapter sources now print the exact focused-test command recorded in `metadata.json`.
- The canonical and staged chapter sources now preserve the patch's one-space blank context line.
- The canonical package and `final_code/ch02` mirror include the same repaired records and replay invariants.
- Replay now rejects a false completed-review state, checksum-locks this failed-review receipt, and rejects generated cache or working-directory residue.

## Active review state

The repairs resolve the first review's listed blockers, but they do not convert its `Fail` verdict into `Pass`. The active package state remains `Pending` until a separate independent reviewer replays the repaired package and issues a new attributable Pass receipt.
