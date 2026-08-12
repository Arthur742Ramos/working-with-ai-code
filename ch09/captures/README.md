# Chapter 9 captures — the house-rule seam

The `house_rule_seam/` fixture preserves the public red before state, the exact
three-line repair, and a sanitized command/output transcript. The red feature
imports a transport directly (`import requests`) and reads
`response.status_code`; the green feature routes the same method, endpoint, and
JSON through `http_client.call`.

## Replay the current session

Run from `ch09/`:

```bash
python3 captures/house_rule_seam/run_capture.py
```

Replay runs the focused red, applies the stored patch in disposable
package-local space, then runs focused and broader green. It uses the local
offline transport stub and never calls a live endpoint.

The capture's [`session.md`](house_rule_seam/session.md) records the contract,
failure, exact diff, and output. The fixture stays generic and public; it does
not reproduce internal book workspace paths or provenance identifiers.

## Retained before-state

- `house_rule_seam/before/alerts.py` imports `requests` directly.
- `house_rule_seam/before/http_client.py` is the shared client boundary.
- `house_rule_seam/before/requests.py` is an offline stub used only by replay.
- `house_rule_seam/after/` shows the repaired feature and unchanged boundary.
- `house_rule_seam/patches/house_rule_seam.patch` is the machine-readable repair.
