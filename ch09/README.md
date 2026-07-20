# Chapter 9 — Context engineering: data, tools, and trust

A short project rule with an executable enforcement point, an approved
outbound-HTTP boundary with auth and bounded retries, an alert feature routed
through that seam, and a retrieval helper that preserves provenance before
injecting evidence into a prompt.

- **`AGENTS.md`** — Listing 9.1: A short project rule with an enforcement point
- **`http_client.py`** — Listing 9.2: The response interface and alert call
- **`retrieval.py`** — Listing 9.3: Retrieve, preserve provenance, then inject
- **`alerts.py`** — the house-correct alert feature that uses `http_client.call`
- **`test_alerts.py`** — routing, auth, and failure checks for the alert feature
- **`test_http_client.py`** — credential, retry, and fail-closed checks
- **`test_house_rules.py`** — an executable AST guard against direct HTTP transports
- **`test_retrieval.py`** — provenance, selection, injection, and recall checks
- **`captures/before/`** — the red before-state that imports `requests` directly
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

## Setup and checks

Run from this directory (needs only `pytest`):

```bash
python3 -m pytest -q
```

`python3 -m pytest -q` reports **14 passed**.

## Listing map

- **Listing 9.1** is the `## Outbound HTTP` rule in `AGENTS.md`; its last
  line names `test_house_rules.py` as the enforcement point.
- **Listing 9.2** is the `Response` dataclass and `call` signature in
  `http_client.py`. The printed listing shows the interface (`...`); the
  maintained file adds the injected transport, auth header, and bounded
  transient retries.
- **Listing 9.3** is `format_evidence` and `answer` in `retrieval.py`, which
  also carries the deterministic `InMemoryStore` and `recall_at_k` metric
  used by the tests.

## Red-to-green capture

See [`captures/README.md`](captures/README.md) to reproduce the seam red
result (a feature importing `requests` directly) and the routing repair.

## Limits

These checks do not prove a live alert service, credential validity,
production transport behavior, or backoff timing. The retrieval example uses
deterministic token overlap, not a production embedding model.

See the [main README](../README.md) for setup instructions.
