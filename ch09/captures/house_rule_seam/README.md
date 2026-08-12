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
