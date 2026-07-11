# AGENTS.md - alerts service

These instructions are the persistent contract for any coding agent working
in this directory. They describe system facts that a model cannot infer from
general training data. Keep changes small, specific, and enforceable.

## House rules

- All outbound HTTP goes through `http_client.call`. Feature modules must not
  import `requests`, `httpx`, `aiohttp`, `urllib`, `http.client`, `socket`, or
  another transport. `test_house_rules.py` enforces this outside the model.
- The sample must not make live network calls. Tests inject a transport, and
  the default transport fails closed.
- Credentials come from `API_TOKEN` or an explicit `Authorization` header.
  Never add a default, example secret, or credential to source.
- Money is integer cents, never floats.
- Timestamps are timezone-aware UTC, never naive `datetime` values.

## Conventions

- Use Python's standard library plus `pytest`; do not add runtime dependencies.
- Feature functions return a plain value or raise `ValueError` for bad input.
- Keep side effects behind narrow, injectable interfaces.
- Do not weaken or exclude the executable house-rule check to make a change
  pass.

## Verify

Run from this directory:

```bash
python3 -m pytest -q
python3 -m py_compile alerts.py http_client.py test_alerts.py \
    test_house_rules.py test_http_client.py
```

A green run means both behavior tests and repository policy checks pass.
