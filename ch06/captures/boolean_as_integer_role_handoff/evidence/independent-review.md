# Independent canonical capture rereview

## Certification

Verdict: **PASS**

No blocking capture, replay, parity, isolation, minimality, provenance, policy-boundary, cleanup, or review-state defect remains. This record certifies the canonical Chapter 6 Boolean-as-integer role-handoff package after correction and independent replay of the two findings from the preceding failed rereview.

## Attribution

- Reviewer role: Independent canonical capture reviewer
- Reviewer tool: Claude Code CLI 2.1.210
- Reviewer model: `gpt-5.6-sol[1m]`
- Review date: 2026-07-15
- Mode: Disposable-copy replay, adversarial path testing, and canonical-to-mirror audit after required repairs
- Attribution limit: Raw vendor session logs are not retained in this package. The capture labels reconstructed material and does not present it as a vendor quotation.

## Resolved blocking findings

The preceding rereview found two blockers in both package trees:

1. Replacing the complete `evidence/` directory with a symlink to byte-identical external evidence was accepted.
2. A default replay left `.pytest_cache/` at the Chapter 6 package root.

The runner now verifies that the resolved evidence root remains under the resolved capture root before it validates the selected review artifact. The broader replay now passes `-p no:cacheprovider` to pytest. A regression test replaces the complete evidence root with an external symlink, while the existing cases continue to reject a direct outside artifact and a child symlink escape.

## Reviewed authorities

The review covered the capture standard, canonical package, final-code mirror, canonical and staged Chapter 6 sources, and active session mapping. The shared session ledger points to this canonical package and intentionally remains Pending for publication-control reconciliation. That external state is not a package failure and was not edited.

The commands below replace the disposable review directory with `$REVIEW_ROOT`. Filenames, arguments, environment controls, and working-directory relationships are unchanged.

## Commands and observed results

Plain default replay from each disposable package:

```bash
python3 \
  "$REVIEW_ROOT/ch06/captures/boolean_as_integer_role_handoff/run_capture.py"
```

Observed result in canonical and mirror copies: exit `0`. Red exited `1`; the patch matched; focused green exited `0`; broader green reported `8 passed`; final support remained unchanged; parity replayed; independent review printed `PASS`.

Post-replay residue search:

```bash
find "$REVIEW_ROOT/ch06" -type d \
  \( -name .work -o -name .pytest_cache \
  -o -name __pycache__ \) -print
```

Observed result in both copies: no output.

Top-level package and path-control checks:

```bash
env -C "$REVIEW_ROOT/ch06" \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  python3 -m pytest -q -p no:cacheprovider

PYTHONDONTWRITEBYTECODE=1 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python3 -m pytest -q -p no:cacheprovider \
  captures/boolean_as_integer_role_handoff/tests/test_review_artifact_path.py
```

Observed results per copy:

- Support package: `8 passed`, exit `0`
- Review-path controls: `2 passed`, exit `0`
- Direct outside artifact: rejected
- Child symlink escape: rejected
- Complete external evidence-root symlink: rejected before artifact acceptance

Independent state transition:

```bash
python3 tests/test_bool_is_not_accepted_as_int.py \
  before/validator.py

patch -s -p1 -d "$REVIEW_ROOT/manual" \
  -i patches/strict-int.patch

python3 tests/test_bool_is_not_accepted_as_int.py \
  "$REVIEW_ROOT/manual/validator.py"

env -C "$REVIEW_ROOT/manual" \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  python3 -m pytest -q -p no:cacheprovider test_validator.py
```

Observed results:

- Focused red: exact stored three-line failure, exit `1`
- Patch application: exit `0`
- Focused green: exact stored two-line result, exit `0`
- Broader green: `8 passed`, exit `0`
- Regenerated patch: byte-identical to `patches/strict-int.patch`
- Patch SHA-256: `4eb382c672ad7618878c117e1c5011f16376ac95d38b38f9d37127a105789b9c`
- Production diff: one removed line and one added line

## Patch and minimality

The patch changes only the integer predicate:

```diff
-    "int": lambda value: isinstance(value, int),
+    "int": lambda value: type(value) is int,
```

The zero-line state fails the focused behavior. The one-line state passes the focused check and all eight neighboring checks. A test edit would hide the defect. A separate branch, helper, or generalized numeric policy would add scope. No smaller non-empty production patch exists.

## Active controls and checksums

The active package records are:

- Capture stage: `complete_independently_reviewed`
- Independent-review status: `completed`
- Independent-review verdict: `Pass`
- Runner SHA-256: `ffb98acd68bc94ddff8d2d821d5477128530ad8e818f3108c84ccc3126d3b719`
- Path-regression SHA-256: `ba10ae54ceef26ee1a0d570fe988241f26ad0d1929fedbce1c1979a4f16a3f54`

All declared before-state, focused-test, patch, evidence, exit-status, runner, regression-test, and final-support checksums matched. The protected red, green, patch, and status artifacts did not change.

## Provenance and three-role boundary

The canonical record distinguishes three separate facts:

1. One Claude Code session produced the tester and implementer artifacts.
2. A later maintained integration-review receipt represents the verifier role in the printed handoff. It is not a separate verifier transcript.
3. This file is the independent package certification. It is not the printed verifier-role artifact.

The implementer prompt does not attribute the named exact-integer option to the author. The chapter and package state that the agent selected exact semantics under standing delegation because the schema exposes a distinct Boolean type. The schema or application owner retains the policy boundary.

The before fixture and contract remain explicitly reconstructed. `session.md` remained byte-identical in canonical and mirror packages with SHA-256 `aede9ddf99cb08e6f73bcad81b2660a47b8a51e71455be1d4e76e723fa2c0ed6`.

## Printed transcript and package parity

Canonical and staged Chapter 6 Markdown and DOCX files are byte-identical. The chapter discloses that internal staging prefixes are removed from commands. The current runner adds a replay-only pytest cache control to the preserved historical broader command; it does not change test collection, output, or exit status.

Canonical and final-code Chapter 6 packages contain the same files with byte-identical content. Outputs, statuses, eight-test count, exact diff, normalized timing, provenance, and the human-owned policy boundary match. Reader-facing prose exposes no private support path or external code prerequisite.

## Superseding evidence-scope clarification

This clarification supersedes only any broad reading of `strict floats` in the historical session record. The eight-test broader suite executes one accepted built-in float (`0.5`) and one nonnumeric rejection (`"half"`). It does not test integer-versus-float discrimination, Boolean-as-float behavior, float subclasses, or every numeric boundary. The protected output, exact patch, and historical observations above remain unchanged.

## Final certification

**PASS**
