# Order-summary incident support

This package contains the runnable order-summary incident and a separately
recorded observability correction. The implementation raises `MissingProductError`
for an orphaned product, logs the integrity incident, and returns a fail-closed
`422` response. The immutable capture under `captures/` records the original
repair, whose tests missed the silent 422 path. Its green evidence and review
receipt apply to that historical state, not to the later logging correction.

## Files

- `server.py` contains the complete green service implementation.
- `seed.py` builds the deterministic SQLite database.
- `tests/test_orphan_policy.py` checks the named domain failure.
- `tests/test_orphan_policy_broader.py` protects a valid summary and the API boundary.
- `tests/test_request_logging.py` protects the 422 diagnostic, 500 traceback,
  successful-request/cache logs, and missing-order log.
- `captures/incident_orphan_product_policy/` preserves the historical session unchanged.
- `corrections/missing_product_logging/` records the follow-on diff, evidence and parity.
- `run_checks.py` verifies the historical capture and current publication separately.

## Run the green checks

From this directory:

```bash
python3 tests/test_orphan_policy.py
python3 tests/test_orphan_policy_broader.py
python3 tests/test_request_logging.py
python3 tests/test_capture_inventory.py
```

These scripts are the intended top-level suite. Run them explicitly.
Recursively collecting `captures/` also collects tests that drive the retained red
before-state for replay evidence.

To rebuild the database and run the service:

```bash
python3 seed.py
python3 server.py 8080
```

Leave the server running and open
[http://localhost:8080/orders/1/summary](http://localhost:8080/orders/1/summary)
for the seeded valid order (HTTP 200). Open
[http://localhost:8080/orders/7/summary](http://localhost:8080/orders/7/summary)
to exercise the seeded orphan: it returns HTTP 422 with
`{"error": "order 7 references missing product 90233"}` under the accepted
fail-closed policy.

The service exposes `/orders/{id}/summary`. Visiting
`http://localhost:8080/` returns HTTP 404 with `{"error": "not found"}`
because no root route is defined. That response is expected.
Stop the server with Ctrl+C when finished.

## Replay the capture and the follow-on correction

```bash
python3 run_checks.py
```

Replay reconstructs the old package in temporary space and runs its unchanged
runner, then shows the new logging test fail against the historical after-state
and pass after the separate correction. Both patches must reproduce their exact
target source. It also reruns the original behavioral checks against the current
server and verifies the current inventory and checksums. No evidence is rewritten.
Do not run the old capture runner directly against the expanded current package:
its historical source and inventory checks intentionally reject that mismatch.

The complete package can be copied elsewhere and run without the repository
root or another chapter. Replay requires Python 3.9 or later with SQLite and
POSIX `patch` and `diff`. Runtime files are confined to temporary space.

## Remaining limitations

The checks cover the deterministic orphan, a neighboring valid order, the
selected `422` response and its error log, unexpected-error tracebacks, and basic
cache/missing-order logs. They do not settle the public status contract, cover
every corruption shape, repair upstream referential integrity, verify concurrent
cache behavior or external monitoring, or demonstrate a latency improvement.
The per-item unindexed lookup remains unchanged and requires a separate
controlled optimization and measurement.
