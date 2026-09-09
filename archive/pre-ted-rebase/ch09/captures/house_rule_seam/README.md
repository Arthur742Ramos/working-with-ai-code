# House-rule seam capture

This public fixture preserves a bounded alert-routing repair. The before
feature uses a direct transport; the after feature routes the existing method,
endpoint, and JSON payload through `http_client.call`.

Run the replay from `ch09/`:

```bash
python3 captures/house_rule_seam/run_capture.py
```

The runner uses disposable package-local space, an offline transport stub, and
the stored patch. [`session.md`](session.md) records the generic contract,
focused red, exact repair, and green command/output evidence.

The focused red must contain the routing discriminator, not just any failing
test. Replay checks exact after-state parity, one focused green, ten broader
checks, and the maintained package suite. The routing observer accepts direct
and module-qualified shared-client calls. The stub and dynamically created
negative import fixture remain offline; no transport dependency is required.
Captured credentials stay sanitized. Author-only provenance and review records
are deliberately not part of this public replay.
