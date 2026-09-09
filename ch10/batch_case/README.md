# Batch snooze: a captured integration-driven replan

This independent extension preserves the single-reminder API while adding
an all-or-nothing batch across handler, service, and SQLite adapter.
It requires Python 3.10+ and pytest. Run from this directory:

```sh
python -m pytest -q
python probe_atomicity.py batch
python replay_capture.py
```

The captured baseline had 49 tests; the final suite has 85. The legacy probe
is intentionally red: `python probe_atomicity.py legacy` must exit 1.
Do not interpret that expected failure as a broken supported batch API.

## What actually happened

Codex inspected the existing adapter, recorded the teaching contract,
ran the existing 49 tests, and tested whether existing per-item saves
could compose atomically. A deliberately installed trigger aborted the
second update. A second connection observed the first update committed.
That genuine failure rejected the composition route. Codex recorded a
replan, changed the adapter and added batch service and handler modules,
then reran the unchanged fault/observer oracle through the batch API and
ran the 85-test suite. No human product-approval exchange is claimed.

`evidence/` retains the contract, baseline, real red output, replan,
green outputs, original module snapshot, exact production patch, and
SHA-256 manifest. Output is the actual run; timing and local traceback
paths are incidental. The printed account condenses and wraps output.
`replay_capture.py` checks hashes, reconstructs the production after-state
from the before-state and patch in a temporary directory, checks exact
module parity, then repeats baseline, expected red, batch green and final
suite. It does not overwrite the original observed outputs.

## Rules and boundaries

The body contains exactly `reminder_ids` and `minutes`. Accept 1–20 distinct,
nonempty, non-whitespace string IDs and exact integer minutes 5, 15, 30 or
60. Identity is trusted request context. Invalid shape is 422 before reads;
missing/other-owner is 404; completed is 409. Semantic validation uses
request order, with the first invalid reminder determining the response.
Validate all selected rows before any write or clock access. One aware
clock reading supplies every reset timestamp. Preserve `due_at` and request
order; return one timestamp and the IDs. Storage errors propagate after
rollback. There is no HTTP error middleware in this example.

The batch adapter requires an idle connection using legacy transaction
control (the mode available on Python 3.10+) with non-None isolation_level.
It rejects caller-owned active transactions and autocommit modes. This is
a deliberate small-application contract, not a general transaction manager.
The experiment uses a file-backed database and a separate observer connection.
See the [Python sqlite3 transaction documentation](https://docs.python.org/3/library/sqlite3.html#transaction-control).

Concurrent completion-versus-snooze, notifications, authentication, deployment,
and crash/disk-failure recovery are outside this case. An injected statement
failure proves rollback for that path, not every possible storage failure.
The original chapter's earlier row-conversion capture remains unchanged.
