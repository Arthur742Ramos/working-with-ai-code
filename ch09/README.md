# Chapter 9 — Context engineering: data, tools, and trust

A short project rule with an executable enforcement point, an approved
outbound-HTTP boundary with auth and bounded retries, an alert feature routed
through that seam, and a retrieval helper that preserves provenance before
injecting evidence into a prompt. The chapter also models host-owned MCP
capability policy without pretending to implement protocol transport.

- **`AGENTS.md`** — Listing 9.1: A short project rule with an enforcement point
- **`http_client.py`** — Listing 9.2: The response interface used by the notification
- **`retrieval.py`** — Listing 9.4: Retrieve, preserve provenance, then inject
- **`alerts.py`** — the house-correct alert feature that uses `http_client.call`
- **`test_alerts.py`** — routing, auth, and failure checks for the alert feature
- **`test_http_client.py`** — credential, retry, and fail-closed checks
- **`test_house_rules.py`** — an executable AST guard against direct HTTP transports
- **`test_retrieval.py`** — provenance, selection, injection, and recall checks
- **`mcp_policy.py`** — host-owned MCP resources, prompts, and tool postures
- **`test_mcp_policy.py`** — approval, allowlist, and lethal-trifecta checks
- **`parity.md`** — the public listing-to-source parity map
- **`test_package_parity.py`** — checks for the maintained teaching surfaces
- **`captures/before/`** — the red before-state that imports `requests` directly
- **`captures/house_rule_seam/`** — the sanitized red-to-green session fixture
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

## Setup and checks

Run from this directory (needs only `pytest`):

```bash
python3 -m pytest -q
```

`python3 -m pytest -q` reports **28 passed**.

## Listing map

- **Listing 9.1** is the `## Outbound HTTP` rule in `AGENTS.md`; its last
  line names `test_house_rules.py` as the enforcement point.
- **Listing 9.2** is the `Response` dataclass and `call` signature in
  `http_client.py`. The printed listing shows the interface (`...`); the
  maintained file adds the injected transport, auth header, and bounded
  transient retries.
- **Listing 9.3** is an illustrative metadata-first skill shape. It teaches
  progressive disclosure as a compact file shape rather than a universal
  format, so it has no maintained companion source and nothing here runs it.
- **Listing 9.4** is `format_evidence` and `answer` in `retrieval.py`, which
  also carries the deterministic `InMemoryStore` and `recall_at_k` metric
  used by the tests.
- The MCP section is represented by `mcp_policy.py`; its tests keep
  capability selection, read/propose/apply postures, and host-level
  containment explicit.

## Red-to-green capture

See [`captures/README.md`](captures/README.md) to reproduce the seam red
result (a feature importing `requests` directly), the exact routing repair,
and the recorded command/output transcript.

## Limits

These checks do not prove a live alert service, credential validity,
production transport behavior, or backoff timing. The retrieval example uses
deterministic token overlap, not a production embedding model. The MCP example
is a local policy model, not a networked MCP client or server.

See the [main README](../README.md) for setup instructions.
