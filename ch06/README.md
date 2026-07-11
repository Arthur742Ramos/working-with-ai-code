# Chapter 6 — Code Listings

The running example for chapter 6: a CSV customer importer built slice by
slice in a planner-executor flow. Parse one row and derive a stable
idempotency key, build and retry the API request, then run a dry import
that counts outcomes. This chapter is a runnable project rather than a set
of standalone listing files, so a reader can `cd` in and run the tests.

- **`importer.py`** — Listings 6.1–6.3: `parse_customer` (6.1: parsing rows
  and deriving a stable idempotency key), `build_request` and
  `send_with_retry` (6.2: building requests and retrying transient
  failures), and `run_import` (6.3: running a dry import). The sender is
  injected so retry behavior is testable without real network calls.
- **`test_importer.py`** — One test per slice's inspection question:
  parsing, stable keys, transient retry, nonretryable failure, dry run, and
  the `409 Conflict` idempotent-replay case.
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

The `409` test is the worked "change the plan on new evidence" slice from
section 6.3: it starts red, and adding `IDEMPOTENT_REPLAY = {409}` to
`send_with_retry` takes it green.

Run the suite:

```bash
cd ch06 && python3 -m pytest -q
```

Expected: `7 passed`. The only dependency is `pytest`
(see [`requirements.txt`](requirements.txt)).

See the [main README](../README.md) for setup instructions.
