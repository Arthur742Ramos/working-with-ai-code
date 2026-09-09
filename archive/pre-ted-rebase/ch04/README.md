# Chapter 4 — Code Listings

Plans you can review and redirect: a staged execution plan for a customer
importer, a complete walking skeleton, a focused idempotent-replay test, the
exact bounded replay-policy diff, and a staged execution contract for a larger
user migration.

- **`listing_4_1_staged_execution_plan.txt`** — Listing 4.1: Staged execution plan for the customer importer
- **`listing_4_2_walking_skeleton.py`** — Listing 4.2: Walking skeleton for a dry-run-capable importer
- **`listing_4_3_idempotent_replay_test.py`** — Listing 4.3: Focused test for an idempotent replay
- **`listing_4_4_bounded_replay_policy.diff`** — Listing 4.4: Exact diff for the bounded replay policy
- **`listing_4_5_migration_execution_contract.txt`** — Listing 4.5: Staged execution contract for a user migration
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listing 4.2 is the complete importer walking skeleton printed in the
manuscript, including parsing, request construction, retry behavior, and the
dry-run runner. Listing 4.3 remains a focused test excerpt and assumes the
importer definitions are in scope. Listing 4.4 is the exact applied diff
against `importer.py`.

See the [main README](../README.md) for setup instructions.
