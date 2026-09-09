# Strict-float validator capture

This internal package preserves one complete coding-agent session for target Chapter 7, *Bounded agents and orchestration*. The selected behavior is a strict `float` schema type: a built-in float passes, while an `int`, `bool`, string, or `float` subclass remains invalid. The slice belongs in this chapter because one bounded contract, one tool-run failure, and one one-line repair make the agent's autonomy reviewable.

## Provenance

The original pre-repair file was not committed separately. `before/validator.py` is therefore a labeled reconstruction: it copies the maintained validator and removes only the strict-float registration documented by the approved architecture and existing chapter exchange. It is checksum-verified, but it is not represented as a historical byte copy.

The initial human contract is also reconstructed and labeled. Red, patch, focused green, broader green, origin canonical support green, and the action sequence come from the actual recorded coding-agent session. `session.md` distinguishes reconstructed text from retained tool evidence.

The original session read and tested repository files. Those paths and checksums remain in `metadata.json` as archival origin provenance. The final package removes executable coupling: replay uses `tests/test_validator.py`, a package-local snapshot of the eight origin test bodies plus one post-review subclass-policy test, and verifies package-local read-only checksums. The strengthened harness preserves the selected exact-float boundary and reruns its evidence rather than rewriting origin history.

## Record and replay

From this capture directory, intentionally recreate reviewed replay evidence with:

```bash
python3 run_capture.py --record
```

Replay all stored evidence without rewriting it with:

```bash
python3 run_capture.py
```

The runner performs the following sequence in self-cleaning `.work-*` space inside this package:

1. Verify the completed independent-review state, prior failed review history, checksum-bound review receipt, before fixture, focused test, localized broader test, runner, action record, and package-local checksums.
2. Reproduce the five-case focused red result from the immutable before fixture.
3. Apply the approved one-line exact-type registration to the disposable copy.
4. Regenerate and compare the exact unified diff.
5. Reproduce five-case focused green and nine-test broader green.
6. Replace the exact predicate with `isinstance(value, float)` in adversarial disposable space and require both test layers to reject it through the subclass case.
7. Verify the retained origin support evidence by stored checksum without executing its historical path.
8. Verify the package files stayed unchanged and parity coverage remains complete.
9. Remove disposable files on success or failure and fail if work state remains.

Default replay never writes the patch or evidence. `--record` is reserved for an intentional refresh after review and writes only package-local patch and replay evidence artifacts. It does not rewrite the retained origin support artifact.

## Direct commands

The discriminating red command is:

```bash
python3 tests/focused_test.py before/validator.py
```

The focused green command targets the disposable after-state:

```bash
python3 tests/focused_test.py <WORK>/validator.py
```

The broader command runs the strengthened nine-test snapshot beside the disposable after-state:

```bash
python3 -m pytest -q -p no:cacheprovider test_validator.py
```

`run_capture.py` prepares `.work/test_validator.py` before that command. Run the replay rather than invoking the broader command directly in a clean capture directory.

## Dependencies and environment

The recorded session used Python 3.14.6 and pytest 9.1.1. The focused test uses only the Python standard library. Broader replay requires pytest. The runner disables pytest color, third-party plugin auto-loading, bytecode output, and the pytest cache provider. It replaces only pytest's machine-dependent elapsed-time value with `<TIME>` in stored evidence.

## Approval basis and policy boundary

The standing direction authorized the coding agent to choose the best bounded implementation without another checkpoint. The agent selected exact built-in `float` semantics because `type(value) is float` rejects the named impostors and subclasses while matching the validator's strict `int` predicate. The record does not claim that the author named one option from a menu.

Humans still own any future change to that boundary. Accepting integer promotion, booleans, numeric strings, subclasses, decimal values, or coercion would be a different product contract. It would require new tests and a separately reviewed patch.

## What the checks prove

The focused red result proves that the reconstructed before state classifies every `float` rule as malformed. Focused green proves that one built-in float passes and four invalid values, including a `float` subclass, produce `expected float`. Broader green proves that the eight origin validator cases plus the subclass policy check pass against the disposable after-state. The adversarial replay proves that substituting `isinstance(value, float)` fails both test layers. Package checksum parity proves replay did not change the final local validator or its strengthened nine-test suite. The archived origin support output and checksums preserve what the original session observed without making the final package depend on those external files.

## What the checks do not prove

The capture checks do not prove that exact-type semantics are right for every validator, that coercion is always wrong, or that arbitrary numeric classes should follow this boundary in another product. They prove only the selected built-in-float policy and its named rejected values. The package also does not prove future reader-facing changes; an independent reviewer must compare any revised excerpt with these artifacts.

## Review status

The first independent review completed with `Fail`: the captured focused and broader checks did not distinguish exact built-in semantics from `isinstance`, and package review fields contradicted one another. That review and its blocking findings remain historical evidence. The independent read-only re-review passed the strengthened canonical and mirrored packages, so the active package state is now `complete_independently_reviewed`, review status `completed`, and package status `Pass`. The review receipt is checksum-bound at `evidence/independent-review.md`. The shared publication ledger was `Pending` during that read-only review and later moved to `Pass` during aggregate reconciliation. The package verdict itself did not change.
