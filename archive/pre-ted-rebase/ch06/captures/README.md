# Chapter 6 capture — Boolean accepted as integer

The permissive before-state maps the `int` schema type to
`isinstance(value, int)`. Because Python's `bool` subclasses `int`, that
predicate accepts `True` where a schema requires an integer. The independent
tester's focused check detects this before any edit.

## Files

- `before/validator.py` — the permissive red before-state.

## Reproduce the red-to-green repair

Run from the chapter directory (`ch06/`):

```bash
# Focused red against the before-state
python3 test_bool_is_not_accepted_as_int.py captures/before/validator.py

# The strict smallest change (already applied in the maintained validator.py):
#   -    "int": lambda value: isinstance(value, int),
#   +    "int": lambda value: type(value) is int,

# Focused green against the maintained validator
python3 test_bool_is_not_accepted_as_int.py validator.py

# Broader suite green
python3 -m pytest -q
```

The focused red prints `FAIL: test_bool_is_not_accepted_as_int` and exits
`1`. After the one-line predicate change, the focused test prints `PASS` and
the broader suite reports `8 passed`. Never leave the maintained
`validator.py` in the permissive state; use this fixture in a disposable copy
to reproduce the red result.
