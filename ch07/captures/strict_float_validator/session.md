# Strict-float validator session

Capture status: repaired after first-review `Fail`; independent re-review pending.

## Provenance

This session started from the staged inspection, red, and plan package. The initial bounded contract is reconstructed and labeled because the original prompt was not retained. The inspection, command sequence, production action, machine-generated diff, and green runs come from the current Claude Code tool log. The transcript is condensed for readability without changing command results.

The action record and origin checksums retain the repository paths used during the session. The final replay runner does not resolve those paths. After the first independent review found that the captured checks accepted an `isinstance` predicate, the package-local focused and broader harnesses gained an explicit `float`-subclass case. The same before state and one-line production patch were then rerun to produce the refreshed evidence below. The retained origin support artifact remains checksum-only history, so the repair strengthens certification without rewriting what the original repository run observed.

## 1. Human contract

**Reconstructed bounded contract:**

> Inspect the staged validator and focused test before editing. The validator lacks a strict `float` type. A built-in float must pass, while `int`, `bool`, and string values must be rejected with `expected float`. Run the focused test, report the failure and its cause, then give the strict smallest-change plan. Do not edit yet.

## 2. Inspection before editing

The agent read `before/validator.py` and `tests/focused_test.py`. The staged `CHECKS` mapping contains `str`, strict `int`, `bool`, and `dict` handlers, but no `float` handler. The original focused test checked one valid built-in float and three named invalid values independently. The repaired harness adds a fourth invalid value, `DerivedFloat(0.5)`, to enforce the exact-type policy the agent selected.

## 3. Genuine focused red

Command:

```bash
python3 tests/focused_test.py before/validator.py
```

Exit status: `1`

Raw output:

```text
FAIL: test_real_float_is_accepted
expected: []
observed: [('ratio', 'malformed schema rule')]
FAIL: test_int_is_rejected_as_float
expected: [('ratio', 'expected float')]
observed: [('ratio', 'malformed schema rule')]
FAIL: test_bool_is_rejected_as_float
expected: [('ratio', 'expected float')]
observed: [('ratio', 'malformed schema rule')]
FAIL: test_string_is_rejected_as_float
expected: [('ratio', 'expected float')]
observed: [('ratio', 'malformed schema rule')]
FAIL: test_float_subclass_is_rejected_as_float
expected: [('ratio', 'expected float')]
observed: [('ratio', 'malformed schema rule')]
5 failed
```

## 4. Agent observation

`"float"` is absent from `CHECKS`, so every schema rule that names it takes the malformed-rule branch before value validation. The valid float and all four forbidden values therefore produce the same wrong error.

## 5. One-sentence plan

Add exactly one `"float": lambda value: type(value) is float` entry to `CHECKS`, then rerun the focused strict-float test and the broader validator suite.

## 6. Approval basis and selected policy

The standing direction authorized the coding agent to choose the best bounded implementation without another approval checkpoint. Acting under that direction, the agent selected exact built-in `float` semantics because that predicate rejects `int`, `bool`, strings, and `float` subclasses while matching the existing strict `int` rule.

This record does not claim that the author named one option from a menu. It records the agent's selection, the standing basis for proceeding, and the reason the selected predicate fits the bounded contract.

## 7. Actual agent action record

The machine-readable action sequence is preserved in `evidence/agent-actions.jsonl`. Sequences 1 through 9 retain the origin coding-agent actions: inspection, red, plan, policy selection, disposable edit, diff, focused green, broader green, and read-only canonical support. Sequences 10 through 13 record this repair: review inspection, test and runner strengthening, genuine evidence refresh, and the adversarial `isinstance` rejection with cleanup verification.

No canonical chapter or canonical code file was changed. The before and after checksums in `metadata.json` cover `chapters/ch07.md` and every tracked file under `code/ch07/`.

## 8. Exact applied production diff

The agent generated this patch with `diff -u` from the immutable before fixture and the disposable after-state:

```diff
--- a/validator.py
+++ b/validator.py
@@ -14,6 +14,7 @@
     "int": lambda value: type(value) is int,
     "bool": lambda value: isinstance(value, bool),
     "dict": lambda value: isinstance(value, dict),
+    "float": lambda value: type(value) is float,
 }
 
 
```

The patch adds one production line and removes none. A zero-line change cannot register a missing schema type. Changing the malformed-rule branch, widening the `int` rule, or coercing values would affect neighboring behavior, so no smaller production patch satisfies the selected contract.

## 9. Genuine focused green

Command:

```bash
python3 tests/focused_test.py .work/validator.py
```

Exit status: `0`

Raw output:

```text
PASS: test_real_float_is_accepted
PASS: test_int_is_rejected_as_float
PASS: test_bool_is_rejected_as_float
PASS: test_string_is_rejected_as_float
PASS: test_float_subclass_is_rejected_as_float
0 failed
```

## 10. Genuine broader green

The runner copied the checksum-verified canonical `test_validator.py` into the disposable after-state and ran:

```bash
python3 -m pytest -q -p no:cacheprovider test_validator.py
```

Exit status: `0`

Stored output, with only elapsed time normalized:

```text
.........                                                                [100%]
9 passed in <TIME>s
```

The same command also ran in the canonical support directory without editing it:

```text
........                                                                 [100%]
8 passed in <TIME>s
```

Exit status: `0`

## 11. Evidence boundary and human-owned decision

The red result proves the before fixture lacks `float` registration. Focused green proves that a built-in float passes and that four named invalid values, including a `float` subclass, return `expected float`. Broader green proves that the eight origin validator cases and the added subclass-policy case pass against the disposable after-state. Adversarial replay proves that both layers fail when the exact predicate is replaced by `isinstance(value, float)`. Canonical support green proves only that the original eight-test support suite was green and unchanged during the origin capture.

These checks do not prove coercion policy, compatibility with arbitrary numeric classes, or that every future schema should use exact Python types. If maintainers later want subclass acceptance, integer promotion, or string coercion, that is a new human-owned contract and needs a different test and patch. This capture keeps that boundary visible instead of smuggling a wider numeric policy into one green check.

## 12. Review gate

The first independent review completed with `Fail`. It confirmed the one-line patch and isolation, then showed that `isinstance(value, float)` passed both captured test layers and found contradictory active review fields. The repaired package now records `ready_for_independent_re_review`, `pending`, and `Pending` consistently. A separate reviewer must replay from clean state, rerun the adversarial predicate check, compare the revised chapter excerpt, and confirm cleanup before any publication control moves to `Pass`.
