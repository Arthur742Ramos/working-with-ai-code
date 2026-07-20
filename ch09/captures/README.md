# Chapter 9 capture — the house-rule seam

The red before-state feature imports a transport directly (`import requests`)
and reads `response.status_code`. It returns success through that direct
transport, but the shared `http_client.call` observer records no method, URL,
or JSON, so the routing test fails and the house-rule guard flags the
unapproved import.

## Files

- `before/alerts.py` — the red feature that imports `requests` directly.
- `before/http_client.py` — the before-state shared client.

## Reproduce the red-to-green repair

Run from the chapter directory (`ch09/`):

```bash
# The exact repair (already applied in the maintained alerts.py):
#   -import requests
#   +from http_client import call
#   -    response = requests.post(ALERTS_URL, json={"text": message})
#   -    return response.status_code < 400
#   +    response = call("POST", ALERTS_URL, json={"text": message})
#   +    return response.status < 400

python3 -m pytest -q
```

The maintained `alerts.py` routes through `http_client.call`, so the suite
reports `14 passed`. Use `before/alerts.py` in a disposable copy to reproduce
the red result, where `test_send_alert_routes_through_house_client` fails and
the AST guard reports an unapproved `requests` import. Never leave the
maintained feature modules in the before-state.
