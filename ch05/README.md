# Order-summary incident support

This internal package contains the runnable order-summary incident in its accepted
green state. The top-level implementation raises `MissingProductError` for an
orphaned product and returns a fail-closed `422` response. The capture under
`captures/` retains the immutable red before-state, exact patch, and recorded
red-to-green evidence.

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

These two scripts are the intended top-level suite. Run them explicitly.
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

## Replay the captured session

```bash
python3 captures/incident_orphan_product_policy/run_capture.py
```

Replay uses a disposable work directory to verify the package-local final
implementation and publication transcript. It leaves the top-level green files
unchanged. The complete package can be copied elsewhere and run without the
repository root or another chapter.

## Remaining limitations

The checks cover one deterministic orphan, one neighboring valid order, and the selected `422` handler response. They do not settle the public status contract, cover every corruption shape, repair upstream referential integrity, verify cache or concurrency behavior, or demonstrate a latency improvement. The per-item unindexed lookup remains unchanged and requires a separate controlled optimization and measurement.
