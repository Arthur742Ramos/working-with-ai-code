# Chapter 7 final support package

This self-contained package keeps the bounded tool-use loop, the final JSON validator and command-line runner, maintained tests, runnable fixtures, and the verified strict-float capture together.

## Chapter parity

- `agent_loop.py` is the complete implementation printed as Listing 7.1, "A minimal bounded tool-use loop."
- `captures/strict_float_validator/patches/strict_float_validator.diff` is the exact one-line production diff printed as Listing 7.3, "The strict smallest float registration."
- `demo_agent.py` and `contract.txt` make Listing 7.2 runnable with `python3 demo_agent.py`. Its adapter is scripted: no model or network is invoked.
- `validator.py` is the maintained green after-state exercised by the package tests. It is support code, not a separate numbered listing.
- `cli.py` is the runnable command-line wrapper for the validator. It is support code, not a numbered listing.
- Tables 7.1 through 7.5 describe stop conditions, workflow choice, worker contracts, failure routing, and autonomy postures. They are conceptual decision aids and have no executable table artifact in this package.

## Files

- `test_agent_loop.py` checks final text, allowed tool execution, forbidden tools, and step-budget exhaustion.
- `test_validator.py` contains nine final-state checks, including the explicit policy that a `float` subclass is rejected.
- `fixtures/` contains one schema plus valid and invalid configuration files for the CLI.
- `pytest.ini` limits top-level discovery to `test_*.py` outside `captures/`, so historical capture internals run only through their replay command.
- `captures/strict_float_validator/` preserves the reconstructed red before-state, exact one-line patch, stored origin evidence, and isolated replay runner.

## Verify the final implementation

Run from this directory:

```bash
python3 -m pytest -q -p no:cacheprovider
```

The expected result is thirteen passing tests: four bounded-loop tests and nine validator tests. Pytest does not recurse into `captures/`.

## Run the validator CLI

The fixture schema requires a string host, a strict built-in integer port, and a strict built-in float ratio under `service`.

A valid configuration prints `ok` and exits 0:

```bash
python3 cli.py \
  --schema fixtures/schema.json \
  --config fixtures/config-valid.json
```

```text
ok
```

The invalid fixture uses a Boolean port and an integer ratio. It prints both dotted-path errors and exits 1:

```bash
python3 cli.py \
  --schema fixtures/schema.json \
  --config fixtures/config-invalid.json
```

```text
service.port: expected int
service.ratio: expected float
```

File, permission, and malformed-JSON errors remain caller-visible exceptions rather than validation results.

## Replay the captured repair

Run from the capture directory:

```bash
cd captures/strict_float_validator
python3 run_capture.py
```

Replay rebuilds disposable red and repaired states, compares them with the stored evidence, verifies the exact patch and package-local checksums, and removes its working directory. Default replay does not rewrite evidence. The original canonical support checksums and green output remain archival provenance; replay does not resolve or execute repository-root paths.

## Remaining limitations

- `run_agent` limits tools and steps, but it does not enforce path or argument policy, spend caps, wall-clock deadlines, repeated-failure stops, or external success checks.
- A model response without a tool call ends `run_agent`; the caller must still verify any completion claim.
- The validator deliberately rejects `float` subclasses, integers used as floats, decimal objects, strings, and coercion. The final suite now tests the subclass boundary explicitly.
- The capture's original focused test names the four cases retained in the printed transcript. The later top-level subclass test strengthens the final package without rewriting that red evidence.
- The package has no networked model adapter or production sandbox. Callers supply `ask_model` and `run_tool` and own their security boundaries.
