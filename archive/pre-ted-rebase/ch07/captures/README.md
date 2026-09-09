# Chapter 7 capture — strict float registration

The red before-state validator has no `float` entry in `CHECKS`, so every
`float` schema rule takes the malformed-rule branch before value validation.
A built-in float is rejected as a malformed rule, and `int`, `bool`, and
string values are never checked against float semantics.

## Files

- `before/validator.py` — the red before-state with no `float` type.

## Reproduce the red-to-green repair

Run from the chapter directory (`ch07/`):

```bash
# The strict smallest change (already applied in the maintained validator.py):
#   +    "float": lambda value: type(value) is float,

# Broader suite green against the maintained validator
python3 -m pytest -q
```

The maintained `validator.py` includes the strict `float` predicate, so the
suite reports `13 passed`. Use `before/validator.py` in a disposable copy to
reproduce the red result: a built-in float reported as `malformed schema
rule`, and `int`, `bool`, and string values not rejected with
`expected float`. Never leave the maintained `validator.py` in the
before-state.
