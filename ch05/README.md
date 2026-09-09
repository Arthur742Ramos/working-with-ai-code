# Order-summary incident support

This internal package preserves the runnable order-summary incident in its accepted green state. The top-level implementation raises `MissingProductError` for an orphaned product and maps that failure to a fail-closed `422` response. The capture under `captures/` retains the immutable red before-state, exact patch, and recorded red-to-green evidence.

## Files

- `server.py` contains the complete green service implementation.
- `seed.py` builds the deterministic SQLite database.
- `tests/test_orphan_policy.py` checks the named domain failure.
- `tests/test_orphan_policy_broader.py` protects a valid summary and the API boundary.
- `captures/incident_orphan_product_policy/` preserves and replays the verified session.

## Run the green checks

From this directory:

```bash
python3 tests/test_orphan_policy.py
python3 tests/test_orphan_policy_broader.py
```

These two scripts are the intended top-level suite. Run them explicitly rather than recursively collecting `captures/`, whose tests drive the retained red before-state as part of replay evidence.

To rebuild the database and run the service:

```bash
python3 seed.py
python3 server.py 8080
```

## Replay the captured session

```bash
python3 captures/incident_orphan_product_policy/run_capture.py
```

Replay uses a disposable work directory, verifies the package-local final implementation and publication transcript, and does not replace the top-level green files. The complete package can be copied elsewhere and run without the repository root or another chapter.

## Remaining limitations

The checks cover one deterministic orphan, one neighboring valid order, and the selected `422` handler response. They do not settle the public status contract, cover every corruption shape, repair upstream referential integrity, verify cache or concurrency behavior, or demonstrate a latency improvement. The per-item unindexed lookup remains unchanged and requires a separate controlled optimization and measurement.
