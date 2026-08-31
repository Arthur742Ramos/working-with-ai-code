# CH06 Prompts

Prompt blocks extracted from the current manuscript source.

## Architect the config validator

````text
You are designing a small JSON config validator in Python.
It must return a list of errors instead of raising, support
`str`, `int`, `bool`, `float`, required keys, and nested
dictionaries, and accept plain Python dictionaries for both
schema and config.

Do not write code. Produce the public function signatures,
the data structure used to report an error, the decisions
about supported types and nested paths, the work that stays
out of scope, and any decision that needs a product owner.

Use only the standard library. Keep the design note under
250 words and include no implementation code.
````

## Implement the validator

````text
Implement the validator from the approved design note.

Honor the exact contract: `validate(config, schema)` returns
`list[ValidationError]`; each error carries a dotted path;
supported types are `str`, `int`, `bool`, `dict`, and
`float`; required keys and nested dictionaries are checked;
unknown configuration keys are ignored.

Use only the standard library, one file, one public
function, and no new public classes. Never raise for a
validation failure. Do not add a loader, command-line entry
point, documentation, or tests.
````

## Test the validator

````text
You are testing the `validate` function against the
approved design note and the public interface. Before
writing any test code, list the categories of cases you
will cover.

Be adversarial: include cases the implementation might
mishandle silently, such as empty schemas, nested misses,
malformed rules, and values that sit between two declared
types.

Use only the standard library and pytest. Write one test
function per case, named after the behavior. Pass plain
dictionaries without mocks. Assert on `path` and on a
substring of `message`.
````

## Explain the validator

````text
Write the supporting material for the verified validator
slice.

Produce a thin runner that loads `schema.json` and
`config.json`, calls `validate`, prints any errors, and
exits `0` or `1`. Add a short usage note that explains the
schema format, supported types, exit codes, and limits.

Use only the standard library and `argparse`. Add no new
validation logic; the runner must remain a thin caller.
State what is unsupported as plainly as what works.
````

## Independent tester handoff

````text
Act as the independent tester at the handoff from tester to implementer.
Verify one bounded behavior: when a schema requires `int`, Python `True`
must not be accepted as a valid integer. Inspect `validator.py` and the
focused test, run the focused test against the before state, report the
observed result, and propose the strict smallest implementation change in
one sentence. Do not edit the implementation before observing red.
````

## Implementer handoff

````text
Standing direction: choose the best bounded implementation without another
approval checkpoint. Replay the genuine red first. Select and state the schema
behavior that best preserves the distinct Boolean type, apply the strict
smallest production diff only to the disposable after state, then run the
focused test and the broader validator suite. Do not broaden the behavior.
````
