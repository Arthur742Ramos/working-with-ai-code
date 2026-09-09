# Lost-cent allocation capture

## Selected behavior

This package records one bounded coding-agent session inside a largest-remainder allocation workflow. The before fixture conserves the total but ranks fractional remainders with binary floats. For `allocate(10, [1, 1, 4])`, all three mathematical remainders are exactly two-thirds. Binary division represents the third residue slightly larger, so the implementation returns `[2, 1, 7]` instead of preserving input order as `[2, 2, 6]`.

The repair converts each numeric weight through its decimal string to `Fraction`, then keeps the existing named `ideal`, `leftover`, and `order` stages. Exact rational residues remain equal, and Python's stable sort keeps tied claims in input order. This is one corrected implementation of the existing largest-remainder workflow, not a second allocation path.

## Record and replay

Run from the final package directory:

```bash
python3 captures/lost_cent_allocation/run_capture.py --record
python3 captures/lost_cent_allocation/run_capture.py
```

Use `--record` only after intentional review. It recreates red and green evidence from the byte-checked before fixture and records the final-package verification. Default replay does not write evidence. It compares commands, output, exit statuses, the machine-generated patch, fixture checksums, package checksums, metadata, parity entries, and session records.

Both modes use disposable working space inside this capture directory and remove it on success or failure. The runner performs these steps in order:

1. Copy the before source and capture tests into disposable space.
2. Run the focused exact-tie test and require exit status `1`.
3. Apply `patches/allocation.patch` and require an exact match with `after/allocation.py`.
4. Run the focused test and require exit status `0`.
5. Run the six-test capture suite and require exit status `0`.
6. Run the nine canonical-equivalent checks plus the promoted exact-tie test against the top-level final implementation and require ten passes.
7. Confirm that every checksummed final-package file remains unchanged.

`pytest.ini` prevents an ordinary top-level pytest run from collecting the capture tests a second time. Replay runs those capture tests only inside its disposable work directory.

Replay rejects stale `.work-*` directories before starting, exercises an intentional exception inside a temporary cleanup probe, and checks cleanup again after the real replay. The success path and the exception path must both leave zero work directories.

## Independent review state

The coding-agent session is complete and reproducible. Current package stage is `complete_independently_reviewed`, independent review status is `completed`, and verdict is `Pass` as of 2026-07-15. The attributable receipt is `evidence/independent-review.md`; `metadata.json` records its checksum and replay verifies its fixed path, attribution, status, verdict, and checksum.

The independent reviewer replayed canonical and mirror copies from clean disposable state, reproduced the manual red, regenerated and applied the exact patch, obtained focused and broader green, and ran the ten-test final package. The review matched all 20 metadata checksum claims and all 28 canonical and mirror non-cache files. Its minimality verdict was `Pass, narrowly` because a shorter candidate removed the explicit representation boundary used by the final implementation and chapter explanation.

During the read-only package review, the shared publication ledger was `Pending`. Aggregate reconciliation later moved Chapter 8 to `Pass`. The historical receipt preserves the earlier state. The ledger and package verdict now agree, but replay still treats them as separate controls and does not read or edit the ledger.

## Dependencies and environment

The recorded environment used:

- Claude Code 2.1.210
- Python 3.14.6
- pytest 9.1.1
- POSIX `diff` and `patch`

The runner disables pytest color and Python bytecode output. Stored outputs are raw. Replay ignores only the machine-dependent elapsed-time value when comparing pytest output.

## Origin provenance

The original session ran nine maintained behavior and golden checks against an unchanged baseline. That output remains byte-checked in `evidence/canonical_support_green.txt`. It proves the baseline was green at capture time, not that the staged repair was compatible with it.

The final package later promoted the exact-rational implementation and exact-tie regression. `evidence/final_package_green.txt` is a separately labeled post-capture run of all ten top-level tests. Replay executes this local run and treats the original nine-test result as `preserved_not_executed` provenance. No repository-root path is resolved.

## Approval basis and human-owned boundary

The direct task instruction authorized this bounded implementation without another approval checkpoint. The agent selected `Fraction(str(weight))` because ordinary numeric weights often express decimal quantities, and this conversion ranks those stated decimal values exactly instead of ranking binary-float artifacts. The existing stable input-order tie rule remains unchanged.

This record does not claim that every domain should interpret numeric weights through decimal strings. Domain owners decide which numeric types the interface accepts, whether decimal-string interpretation matches those types, and whether stable input order is the right fairness rule.

## Minimality rationale

The patch changes one implementation path. It adds one standard-library import and one named conversion stage, then reuses the existing largest-remainder calculation, floor, leftover count, stable ranking, and mutation loop. Removing the conversion would restore the bug. Replacing the named stages with dense expressions would shorten the diff without narrowing behavior or improving reviewability.

The focused assertion `allocate(10, [1, 1, 4]) == [2, 2, 6]` rejects the old float ranking. The prior cases remain: conservation for three equal claims, exact even and weighted splits, unequal largest remainder, and `allocate(1, [1, 1, 2]) == [0, 0, 1]` to reject round-then-force-index-zero.

## What the checks prove

The focused red proves that the reviewed float implementation misorders an ordinary exact tie. The focused green proves that the applied patch returns `[2, 2, 6]` for that case. The six-test broader green protects the original lost-cent behavior and the four earlier neighboring cases.

The historical nine-test output preserves honest origin evidence. The final-package ten-test run supplies the release evidence the chapter identifies as missing: the promoted exact-rational allocator passes all nine canonical-equivalent checks and the exact-tie regression in one suite.

## What the checks do not prove

These checks do not prove behavior for every numeric type, non-finite value, extreme magnitude, negative or empty capture input, or every possible weight distribution. They do not prove that decimal-string interpretation or stable input order is the correct product policy.

The capture adds no validation, public interface, feature flag, or second allocation workflow. The top-level final package supplies validation and the named consumer without changing the preserved before fixture, after fixture, patch, or original session evidence.
