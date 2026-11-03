# Chapter 2 final support package

This internal package contains the finished offline PR-description generator and the verified retry-wiring capture. The top-level files are the green reader-facing implementation. They run without a network, credentials, a Git repository, or another chapter's files.

## Files

- `local_fixture.py` supplies the fixed diff and deterministic responses used by the default path.
- `schema.py` defines the output contract.
- `pr_generator.py` parses, validates with `jsonschema`, retries, renders, and saves the generated description.
- `anthropic_adapter.py` is an optional live-provider boundary that uses Anthropic's official Python SDK and rejects incomplete stop reasons before text extraction.
- `test_pr_generator.py` checks the offline fixture, standards-compliant schema failures, retry bounds, formatting, command-line behavior, and provider stop reasons.
- `pytest.ini` limits ordinary pytest collection to the green top-level suite and excludes `captures/`.
- `captures/pr_generator_retry_wiring/` preserves the historical red state, exact one-line repair, evidence, and replay runner.

## Install dependencies

Install the package dependencies from the checked-in manifest:

```bash
python3 -m pip install -r requirements.txt
```

The offline path requires `jsonschema`; `anthropic` supports the optional live-provider adapter.

## Run the offline generator

After installing `jsonschema`, run from any directory:

```bash
python3 /path/to/ch02/pr_generator.py
```

The command prints the formatted description and writes `pr_description.json` in the current working directory. Its first deterministic response is malformed. The bounded retry carries the parser feedback, and the second response succeeds.

## Run the top-level tests

From this directory, run the top-level suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 test_pr_generator.py
```

If pytest is installed, this command runs the same intended top-level suite without collecting capture internals:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
```

## Replay the captured repair

```bash
python3 captures/pr_generator_retry_wiring/run_capture.py
```

Replay verifies the historical before state, genuine red output, stored one-line patch, focused and broader green evidence, and package-local checksums. It also copies this package into disposable isolated space and runs the promoted top-level tests there. Default replay never rewrites historical evidence. The final-polish recertification is a separate current-package record; it does not revise the captured retry session.

## Optional live provider

The offline path is the default and has no provider prerequisite. To use the optional adapter, install the official SDK:

```bash
python3 -m pip install anthropic
```

Then change only the import boundary in `pr_generator.py`: import `FIXED_DIFF` from `local_fixture` and import `chat` from `anthropic_adapter`. Configure credentials through a credential source supported by the SDK, and set `ANTHROPIC_MODEL` to a currently supported model identifier. The parser, local schema validator, renderer, and retry policy stay unchanged.

## Remaining limitations

- Schema validation checks structure, not whether generated claims are true.
- Automatic retry covers only JSON parsing and schema-validation failures, with three attempts total.
- The offline fixture proves the package wiring, not live-model compliance or provider behavior.
- The SDK may retry connection errors and HTTP `408`, `409`, `429`, and `5xx` responses before an error reaches the adapter.
- The adapter accepts only `end_turn`; refusal, truncation, authentication, exhausted transport retries, and no-text failures stay outside the JSON-validation retry loop.
- The retry classes and retry budget remain human-owned product and cost decisions.
