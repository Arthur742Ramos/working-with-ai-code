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

The commands that set `PYTHONDONTWRITEBYTECODE` use POSIX shell syntax. In PowerShell, set `$env:PYTHONDONTWRITEBYTECODE = '1'` first, then omit the leading assignment from each command. On Windows, if `python3` is unavailable, replace it with an available Python 3 launcher such as `python` or `py -3`.

For the offline generator and the unittest suite, install `jsonschema`:

```bash
python3 -m pip install 'jsonschema>=4.0'
```

To run the optional pytest command, install pytest as well:

```bash
python3 -m pip install 'pytest>=8,<10'
```

To install both dependencies and Anthropic's optional SDK from the checked-in manifest, run this command from the `ch02` directory:

```bash
python3 -m pip install -r requirements.txt
```

## Run the offline generator

After installing `jsonschema`, run from any directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /path/to/ch02/pr_generator.py
```

The command prints the formatted description and writes `pr_description.json` in the current working directory, overwriting an existing file of that name. The offline fixture uses a fixed diff; it does not read staged Git changes. Its first deterministic response is malformed. The bounded retry carries the parser feedback, and the second response succeeds.

## Run the top-level tests

From this directory, run the top-level suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 test_pr_generator.py
```

A passing run reports a test count and `OK` and exits 0. The CLI test writes `pr_description.json` in a temporary directory, which is removed afterward. It does not leave that file beside the test script; run the generator above to keep an output file.

If pytest is installed, this command runs the same intended top-level suite without collecting capture internals:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider
```

Pytest reports the number of passing tests and exits 0 on success; a test failure exits nonzero.

Bytecode suppression and the pytest cache flag prevent two kinds of new cache residue; they do not remove existing files. Inspect any existing `__pycache__`, `.pytest_cache`, and `*.pyc` entries and preserve anything you do not recognize. Use a fresh disposable copy for verification rather than blanket-cleaning working files or captured evidence.

## Replay the captured repair

From this directory, run the wrapper. The historical verifier requires the `patch` executable on `PATH`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 run_checks.py
```

The wrapper restores the original `README.md`, `local_fixture.py`, and `test_pr_generator.py` from `corrections/retry_feedback/historical/` into a temporary copy and runs the unchanged capture verifier there. This verifies the historical red output, one-line repair, focused and broader green evidence, and original 18-test package. It then demonstrates that the new repeated-diff regression fails against that original fixture, and runs all 21 tests against the corrected current package. No historical evidence is rewritten.

The historical red subprocess is expected to exit 1, and the repaired checks should pass. The follow-on regression also fails against the original fixture. Successful verification exits 0 overall. A checksum, generated-residue, or unexpected test failure is a replay failure, not the expected red result.

Historical checksums cover exact file bytes, including line endings. If a checkout changes those bytes, use a fresh copy that preserves the recorded files rather than altering evidence or checksums. The wrapper excludes existing cache and work directories from its temporary historical copy; it does not remove them from your working files.

The unchanged historical focused test can fail on Windows with `WinError 32` when it tries to remove its current working directory. This makes the wrapper fail overall, even if the current top-level tests pass when run separately.

The follow-on correction in `corrections/retry_feedback/` strengthens the fixture: a repeated prompt containing the word “invalid” no longer counts as parser feedback. The fixture now checks the three-message history, preserved malformed reply, and the parser-error prefix for that known reply. This checks the deterministic example, not arbitrary provider behavior or every possible schema-validation error.

The original direct capture runner and its final-polish recertification describe the historical package. Use the wrapper above for the current package; the historical receipt does not certify the updated README or the later fixture correction.

## Optional live provider

The offline path is the default and has no provider prerequisite. To use the optional adapter, install the official SDK:

```bash
python3 -m pip install 'anthropic>=0.75'
```

Then change only the import boundary in `pr_generator.py`: import `FIXED_DIFF` from `local_fixture` and import `chat` from `anthropic_adapter`. Configure credentials through a credential source supported by the SDK, and set `ANTHROPIC_MODEL` to a currently supported model identifier. The parser, local schema validator, renderer, and retry policy stay unchanged.

To remove that SDK from the selected environment, run `python3 -m pip uninstall anthropic`. This disables the optional adapter in that environment.

## Remaining limitations

- Schema validation checks structure, not whether generated claims are true.
- Automatic retry covers only JSON parsing and schema-validation failures, with three attempts total.
- The offline fixture proves the package wiring, not live-model compliance or provider behavior.
- The SDK may retry connection errors and HTTP `408`, `409`, `429`, and `5xx` responses before an error reaches the adapter.
- The adapter accepts only `end_turn`; refusal, truncation, authentication, exhausted transport retries, and no-text failures stay outside the JSON-validation retry loop.
- The retry classes and retry budget remain human-owned product and cost decisions.
