# Chapter 7 — Code Listings

The running example for chapter 7: a JSON config validator built by four
narrow roles (architect, coder, tester, explainer) and then extended by a
real agent session in section 7.6. Like chapter 6, this is a runnable
project rather than a set of standalone listing files.

- **`validator.py`** — Listing 7.1: The coder's validator implementation.
  `validate(config, schema) -> list[ValidationError]` walks the schema,
  never raises, and returns a list of dotted-path errors. `CHECKS` is the
  set of supported types.
- **`test_validator.py`** — Listings 7.2 and 7.3: Adversarial tests for
  the validator, one per category the tester role named. The core cases
  (happy path and top-level misses) are Listing 7.2; the boundary cases
  (empty schema, bool-is-not-int, malformed rules) are Listing 7.3. It
  also includes `test_float_type_is_supported`, the slice the agent adds
  in section 7.6.
- **`cli.py`** — Listing 7.4: A thin CLI runner for the validator. Loads
  `schema.json` and `config.json`, calls `validate`, prints errors, and
  exits 0 or 1. No validation logic lives here.
- **`listing_7_5_tool_use_loop.py`** — Listing 7.5: A minimal tool-use
  loop. An illustrative snippet that shows the shape of an agent loop; it
  references undefined names and is **not** run by the test suite.
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

The `float` test in `test_validator.py` starts red. Adding `"float"` to
`CHECKS` is the worked agent slice; section 7.6 shows the real capture
going from red to green.

Run the suite:

```bash
cd ch07 && python3 -m pytest -q
```

Expected: `8 passed`. The suite does not import
`listing_7_5_tool_use_loop.py`. The only dependency is `pytest`
(see [`requirements.txt`](requirements.txt)).

See the [main README](../README.md) for setup instructions.
