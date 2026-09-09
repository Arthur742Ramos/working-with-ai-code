# Migration parity ledger

The migration implementation is a package-local reconstruction from the staged Chapter 4 contract and printed dry-run report. The schemas and three-row fixture preserve their historical Chapter 5 origin, but this package neither imports nor executes Chapter 5 support.

| Chapter item | Package source | Verification |
|---|---|---|
| Stable source identity and rerunnable upsert | `migrate.py`, `run_migration` | `test_apply_is_idempotent_on_rerun` keeps three accounts and nine audit rows after a second apply |
| Email, date, and account-type normalization | `migrate.py`, `normalize_row` | `test_apply_commits_normalized_rows_and_audits` checks the Jane Doe row printed in the chapter |
| Skip-and-report validation policy | `migrate.py`, `run_migration` | `test_invalid_rows_are_skipped_and_reported` adds a bad date and checks the reconciled counts |
| Rollback-based dry run | `migrate.py`, `run_migration` | `test_dry_run_matches_printed_evidence_and_rolls_back` checks that target tables remain empty |
| Printed dry-run counts and sample audits | `evidence/dry-run.txt` | The dry-run test rejects Markdown backticks, byte-compares `format_report` with the evidence, and verifies SHA-256 `a54895f15f960161be8eb8e82733fc3dedfb3aa5ae9fad31c6f63a2f68af3a58` |
| Unexpected-error rollback | `migrate.py`, `run_migration` | `test_unexpected_error_rolls_back_the_transaction` forces an audit write failure and checks that no account remains |

The reconstruction proves that one implementation can produce the chapter's stated evidence against the supplied fixture. It does not prove that this exact implementation generated the original staged prose, and it does not settle the human-owned timezone or skip-versus-abort policies.
