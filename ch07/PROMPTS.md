# CH07 Prompts

Prompt blocks extracted from the current manuscript source.

## Architect for config validator

````text
You are designing a small JSON config validator in Python.
It must return a list of errors instead of raising, support
`str`, `int`, `bool`, required keys, and nested dicts, and
accept plain Python dicts for both schema and config.
Do not write code. Produce:

- The function signatures for the public API
- A short data structure for reported errors
- The decisions you are making (what types are supported,
  how nested keys are reported, what is out of scope)

Constraints:
- Standard library only
- Keep the design note under 250 words
- No implementation code
````

## Implement the validator

````text
Implement the validator from the architect's sketch.

Honor the contract exactly:
- `validate(config, schema) -> list[ValidationError]`
- `ValidationError(path, message)` with dotted paths
- Supported types: `str`, `int`, `bool`, `dict`
- Required keys, nested dicts, and ignored unknown keys

Constraints:
- Standard library only
- One file, 30 nonblank lines or fewer
- No new public functions or classes
- Never raise
````

## Test the validator

````text
You are testing the `validate` function in the previous
message. Before writing test code, list the categories of
cases you will cover. Then write pytest-style tests for each.

Be adversarial: include cases the implementation might
mishandle silently, such as empty schemas, nested misses,
and wrong types at the top level.

Constraints:
- Standard library and pytest only
- One test function per case, named after the behavior
- No mocking; pass plain dicts
````

## Explain the validator

````text
Write the supporting material for the validator slice.

Produce:
- A small CLI that loads `schema.json` and `config.json`,
  calls `validate`, prints any errors, and exits 0 or 1
- A short README paragraph (3-4 sentences) explaining the
  schema format and the exit codes

Constraints:
- Standard library only
- Use argparse
- No new validation logic; the CLI is a thin runner
````

## One slice: support a float type

````text
The validator is in `validator.py` with tests in
`test_validator.py`. The contract now needs a `float` type:
a real float is valid, anything else is rejected. Run the
tests, say what fails and why, then make the smallest change
to pass. Keep floats strict: do not accept ints or bools.
````
