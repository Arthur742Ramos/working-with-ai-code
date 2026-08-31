# Chapter 6 — Roles that produce independent artifacts

A JSON config validator built by four narrow roles (architect, coder,
tester, explainer). An independent tester's focused test catches Python
`True` being accepted where a schema requires `int`, and the implementer
tightens exactly one predicate under an explicit policy.

- **`validator.py`** — Listing 6.1: The coder's validator implementation (maintained green version)
- **`test_validator.py`** — Listing 6.2 source: the eight maintained broader checks; the printed listing excerpts four of them
- **`test_bool_is_not_accepted_as_int.py`** — Listing 6.3: Independent focused test derived from the contract
- **`cli.py`** — Listing 6.4: A thin command-line runner for the verified validator
- **`schema.json`**, **`config.json`**, **`invalid_config.json`** — generic fixtures for the CLI commands
- **`captures/before/validator.py`** — the permissive red before-state fixture
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

## Setup and checks

Run from this directory (needs only `pytest`):

```bash
python3 -m pytest -q
python3 cli.py --schema schema.json --config config.json
python3 cli.py --schema schema.json --config invalid_config.json
python3 test_bool_is_not_accepted_as_int.py validator.py
```

`python3 -m pytest -q` reports **8 passed**. The valid CLI command prints
`ok` and exits `0`; the invalid one prints `service.port: expected int` and
exits `1`. The focused handoff test prints `PASS`.

## Listing map

- **Listing 6.1** follows the formatting of the maintained `validator.py`,
  but its printed `int` predicate (`isinstance(value, int)`) is the coder's
  permissive before-state, preserved under `captures/before/validator.py`.
  The maintained `validator.py` keeps the accepted strict predicate
  (`type(value) is int`).
- **Listing 6.2** excerpts four contract-derived cases from `test_validator.py`
  — `test_nested_missing_required_key`, `test_empty_schema_accepts_anything`,
  `test_bool_is_not_accepted_as_int`, and
  `test_malformed_schema_rule_reports_error`. The chapter prints the complete
  functions without modification; the maintained file keeps all eight checks.
- **Listing 6.3** is `test_bool_is_not_accepted_as_int.py`, the independent
  focused tester artifact and standalone green check.
- **Listing 6.4** is `cli.py`, the thin command-line runner.

## Red-to-green capture

The permissive before-state accepts `True` where an `int` is required. See
[`captures/README.md`](captures/README.md) to reproduce the focused red, the
one-line repair, and the focused and broader green.

## Limits

The validator supports only strings, exact built-in integers, Booleans,
dictionaries, and exact built-in floats. Arrays, coercion, custom messages,
and unknown-key validation are out of scope. The capture proves only the
Boolean-as-integer repair; it does not choose a product's schema policy.

See the [main README](../README.md) for setup instructions.
