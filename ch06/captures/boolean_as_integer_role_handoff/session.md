# Boolean-as-integer role handoff session

Status: red, strict smallest patch, focused green, and broader green captured. Independent review and final Chapter 6 integration are complete.

## Provenance

The contract below is reconstructed from the approved restructuring architecture dated 2026-07-14 and the author's staging direction for target Chapter 6. It is not a verbatim retained prompt and must not be attributed to a vendor as a quotation. The tester and implementer artifacts, including the inspection, commands, outputs, observation, plan, selection, action, diff, and green results, were recorded contemporaneously in this one coding-agent session with Claude Code 2.1.210. The verifier JSON was maintained later as an integration-review receipt, not captured as a separate verifier transcript.

The before fixture is also a transparent reconstruction, not a historical committed snapshot. It originated from the earlier maintained role-relay validator at the repository commit recorded in `metadata.json`, with the permissive integer predicate staged as the blind spot. Final packaging removed the retired chapter label and original support path from this copy without changing the red behavior. The top-level Chapter 6 implementation remains green.

## Human contract (reconstructed)

Act as the independent tester at the handoff from tester to implementer. Verify one bounded behavior: when a schema requires `int`, Python `True` must not be accepted as a valid integer. Inspect the staged validator and the focused test, run the focused test against the before fixture, report the observed result, and propose the strict smallest implementation change in one sentence. Do not edit the implementation before observing the red result.

## Agent inspection

I read `before/validator.py` and `tests/test_bool_is_not_accepted_as_int.py` before running the test.

The staged source maps the `int` schema type to `isinstance(value, int)`. Because `bool` is a subclass of `int` in Python, that predicate accepts `True`. The independent test passes `{"port": True}` against a required `int` rule and requires one error at `port` whose message contains `int`.

## Genuine focused red

Command:

```text
python3 captures/boolean_as_integer_role_handoff/tests/test_bool_is_not_accepted_as_int.py captures/boolean_as_integer_role_handoff/before/validator.py
```

Exit status: `1`

Raw output:

```text
FAIL: test_bool_is_not_accepted_as_int
expected: port: expected int
observed: no validation errors; True was accepted
```

## Agent observation

The test discriminates the selected behavior: the before implementation silently accepts `True`, so no `ValidationError` is returned for a field whose schema requires `int`.

## One-sentence strict-smallest-change plan

Change only the `CHECKS["int"]` predicate from `isinstance(value, int)` to `type(value) is int`, leaving boolean and every other schema behavior unchanged.

## Approval basis and selected policy

The author's standing direction authorizes the agent to choose the best bounded implementation without another approval checkpoint. It does not say that the author selected a named option from a menu.

Under that direction, I selected exact built-in `int` semantics: an `int` rule accepts values whose type is exactly `int` and rejects `bool`. The rationale is structural. This schema already exposes `bool` as a distinct type, and JSON represents booleans separately from numbers. The schema semantics remain a human-owned product boundary even though the agent selected this implementation under delegated direction.

## Agent action record

1. Read the capture standard, staged before fixture, focused test, red evidence, runner, metadata, session ledger, and parity ledger.
2. Read the maintained validator and its eight-test suite only to establish the broader-check source and canonical checksums.
3. Ran the existing non-recording replay and observed the genuine focused red result with exit status `1` before any staged production edit.
4. Selected exact built-in `int` semantics under the standing direction and retained the one-sentence plan.
5. Upgraded `run_capture.py` inside this package so it copies the immutable before fixture into `.work/`, performs one exact predicate replacement there, and removes `.work/` on success or failure.
6. Ran `run_capture.py --record`. The runner generated the unified diff, focused green evidence, broader green evidence, and exit-status files from the disposable copy.
7. Removed only unstable pytest presentation noise: ANSI color sequences and elapsed timing. Test progress, counts, text, and exit status remain unchanged.
8. Re-recorded after normalization and verified the same red, diff, focused green, broader green, and canonical checksums.
9. An auxiliary `git diff --no-index` diagnostic displayed the same one-line change but its shell wrapper ended with status `1` because zsh reserves `status` as read-only. It changed no file and is not evidence for this capture.
10. Completed the metadata, session, README, and parity records, then used default replay to compare stored artifacts without rewriting them.
11. Rejected an initial text-integrity probe because it called unavailable `rg`; its apparent success was not accepted as evidence.
12. Replaced that probe with a Python scan. The scan found only a dead cleanup reference to the removed staging placeholder, so I deleted that branch, reran replay, and confirmed no forbidden dash, personal path, or stale marker remained.

## Exact applied diff

The runner generated this diff by comparing the immutable before fixture with the disposable after-state copy:

```diff
--- before/validator.py
+++ after/validator.py
@@ -11,7 +11,7 @@
 
 CHECKS = {
     "str": lambda value: isinstance(value, str),
-    "int": lambda value: isinstance(value, int),
+    "int": lambda value: type(value) is int,
     "bool": lambda value: isinstance(value, bool),
     "dict": lambda value: isinstance(value, dict),
     "float": lambda value: type(value) is float,
```

The patch changes one production line. A smaller patch cannot implement the selected exact-type policy because the permissive predicate itself is the complete behavior under repair. No test, message, branch, helper, or neighboring type predicate changed.

## Genuine focused green

Command executed against the disposable after-state copy:

```text
python3 captures/boolean_as_integer_role_handoff/tests/test_bool_is_not_accepted_as_int.py captures/boolean_as_integer_role_handoff/.work/validator.py
```

Exit status: `0`

Raw output:

```text
PASS: test_bool_is_not_accepted_as_int
observed: port: expected int
```

## Genuine broader green

The runner copied the maintained eight-test validator suite into disposable `.work/` space beside the after-state `validator.py`, then ran:

```text
cd captures/boolean_as_integer_role_handoff/.work && python3 -m pytest -q test_validator.py
```

Exit status: `0`

Recorded output with only ANSI color and elapsed timing normalized:

```text
........                                                                 [100%]
8 passed in <TIME>s
```

The broader suite protects valid strings, missing required keys, top-level type errors, nested paths, empty schemas, the Boolean-as-integer boundary, malformed rules, and strict floats.

## Agent evidence-boundary statement

The focused red proves that the reconstructed before fixture accepts `True` for an `int` field and that the independent tester catches it. The one-line patch plus focused green proves that exact built-in `int` semantics reject that value in the disposable after state. The broader green proves that the eight maintained validator checks still pass against that after state.

These checks do not prove that every Python numeric edge case has the desired schema meaning, that another runtime should use identical rules, or that every malformed schema shape is handled. The independent review checks this bounded evidence path, not the whole validator domain.

## Author inspection and human-owned policy decision

The author supplied standing direction to choose the best bounded implementation and the policy constraint that the schema has a distinct Boolean type. The approval basis did not name a specific option as the author's selection. Applying that direction, the agent selected exact built-in `int` semantics for this slice.

The product owner still owns the schema contract. If the intended contract later changes to Python subclass semantics, this patch should not survive merely because it is green. Green tests confirm the selected contract; they do not choose it.

A later integration review replayed the capture, challenged patch minimality, checked the policy boundary, and stored the maintained verifier receipt for the final Chapter 6 package. No separate verifier transcript was captured.
