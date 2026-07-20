# Chapter 4 — Code Listings

Plans you can review and redirect: a staged execution plan for a customer
importer, a dry-run-capable walking skeleton, a focused idempotent-replay
test, the exact bounded replay-policy diff, and a staged execution contract
for a larger user migration.

- **`listing_4_1_staged_execution_plan.txt`** — Listing 4.1: Staged execution plan for the customer importer
- **`listing_4_2_walking_skeleton.py`** — Listing 4.2: Walking skeleton for a dry-run-capable importer
- **`listing_4_3_idempotent_replay_test.py`** — Listing 4.3: Focused test for an idempotent replay
- **`listing_4_4_bounded_replay_policy.diff`** — Listing 4.4: Exact diff for the bounded replay policy
- **`listing_4_5_migration_execution_contract.txt`** — Listing 4.5: Staged execution contract for a user migration
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 4.2 and 4.3 are excerpts of the importer and its test harness:
`Sender`, `parse_customer`, `send_with_retry`, and `fake_sender` are defined
elsewhere in the project, so these mirror the printed listings rather than
standing alone as runnable modules. Listing 4.4 is the exact applied diff
against `importer.py`.

See the [main README](../README.md) for setup instructions.
