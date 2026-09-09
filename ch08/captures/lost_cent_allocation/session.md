# Lost-cent allocation session

Capture stage: complete exact-tie red, reviewable exact-rational repair, focused green, broader green, canonical behavior and golden verification, authorial inspection, and non-recording replay.

## 1. Human contract

The retained contract below is condensed from the current task instruction. It is not presented as a verbatim quotation.

> Work only inside the staged Chapter 8 lost-cent package. Fix stable largest-remainder behavior for ordinary equal exact remainders without binary-float misordering. Use a clear exact representation for numeric weights, retain stable input-order ties, and add `allocate(10, [1, 1, 4]) == [2, 2, 6]` beside the prior discriminating cases. Review the behavior and test before intentional record mode, regenerate genuine red, diff, and green evidence, run all relevant canonical tests including `test_golden.py`, reconcile the actual agent record and evidence limits, and leave canonical Chapter 8 files unchanged. Do not add a second workflow.

## 2. Agent inspection

The agent read the governing instructions, polished-outcome memory, capture standard, every staged package file, the session ledger, and canonical Chapter 8 source, behavior tests, golden tests, and prose as read-only context.

The staged after-state used binary-float ideal shares. A direct run produced:

```text
[2, 1, 7]
[1.6666666666666667, 1.6666666666666667, 6.666666666666667]
[0.6666666666666667, 0.6666666666666667, 0.666666666666667]
```

The mathematical remainders are equal, but the third binary-float residue is slightly larger. Reverse stable sorting therefore ranks index 2 before the tied earlier indices. The existing conservation and unequal-remainder cases do not expose that failure.

## 3. Genuine focused red

Before record mode, the agent copied the reviewed float source and focused test into disposable space and ran the new case. After the code and test review, the recorder reproduced the same red command from the byte-checked fixture:

```text
python3 -m pytest -q -p no:cacheprovider test_lost_cent.py::test_equal_exact_remainders_keep_input_order
```

Raw recorded output:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
_________________ test_equal_exact_remainders_keep_input_order _________________

    def test_equal_exact_remainders_keep_input_order():
>       assert allocate(10, [1, 1, 4]) == [2, 2, 6]
E       assert [2, 1, 7] == [2, 2, 6]
E         
E         At index 1 diff: 1 != 2
E         Use -v to get more diff

test_lost_cent.py:13: AssertionError
=========================== short test summary info ============================
FAILED test_lost_cent.py::test_equal_exact_remainders_keep_input_order - asse...
1 failed in 0.01s
```

Exit status: `1`.

Agent observation: binary-float arithmetic makes the third two-thirds residue slightly larger than the first two, so stable sorting cannot preserve a mathematical tie that the representation has already broken.

## 4. One-sentence plan

Convert each stated numeric weight to an exact rational with `Fraction(str(weight))`, preserve the existing named largest-remainder stages and stable sort, and pin the equal-remainder case beside the earlier conservation and shortcut-discriminating cases.

## 5. Approval basis and selected policy

The direct task instruction authorized this bounded implementation without another approval checkpoint. The agent selected exact rationalization through each numeric weight's decimal string while retaining stable input order for equal remainders.

The rationale was bounded: decimal-string conversion preserves the value an ordinary integer or float states instead of its hidden binary approximation, `Fraction` compares residues exactly, and the existing stable sort then keeps equal claims in input order. Domain owners still decide which numeric types and tie policy the production interface accepts.

## 6. Actual agent action record

1. Read `AGENTS.md`, the polished-outcome memory, the capture standard, the full staged package, the session ledger, and canonical Chapter 8 source, `test_allocation.py`, `test_golden.py`, and prose as read-only context.
2. Ran the staged float implementation directly and observed `[2, 1, 7]` plus the unequal binary-float residues shown above.
3. Promoted that reviewed float implementation to the before fixture, added `test_equal_exact_remainders_keep_input_order`, retained the prior conservation and four neighboring tests, and drafted an exact-rational after-state.
4. Ran the focused case against the before-state in disposable space and observed the genuine red. Ran all six staged tests against the after-state and observed six passes. Ran both canonical test files read-only and observed nine passes.
5. Reviewed the diff and removed a documentation-only difference so the patch contained only the arithmetic representation change.
6. The first patch-generation shell wrapper wrote the diff but then failed because zsh reserves `status` as read-only. Reran the same `diff -u` command using `rc`, verified exit `1` as the expected non-empty-diff result, and retained the mechanically generated patch.
7. Updated the runner to checksum the new fixtures and patch, focus on the exact-tie test, run both canonical test files, verify the golden-test checksum, and require the new parity entries.
8. Ran intentional record mode once after the code, test, and diff review. It reproduced focused red, applied the exact patch in disposable space, recorded focused and six-test broader green, recorded the nine-test canonical green, and confirmed canonical checksums were unchanged.
9. Updated metadata, README, patch rationale, session, publication excerpt, parity, and session-ledger surfaces from the stored evidence.
10. Ran default replay to compare the commands, raw evidence, patch, fixture checksums, metadata, records, parity, and canonical immutability without rewriting evidence.

## 7. Exact applied production diff

The runner regenerated and compared this diff, then applied it only in disposable space:

```diff
--- a/allocation.py
+++ b/allocation.py
@@ -1,9 +1,18 @@
 """Proportional allocation with stable input-order ties."""
 
+from fractions import Fraction
 
+
 def allocate(total, weights):
-    total_weight = sum(weights)
-    ideal = [total * weight / total_weight for weight in weights]
+    exact_weights = [
+        Fraction(str(weight))
+        for weight in weights
+    ]
+    total_weight = sum(exact_weights)
+    ideal = [
+        total * weight / total_weight
+        for weight in exact_weights
+    ]
     shares = [int(value) for value in ideal]
     leftover = total - sum(shares)
     order = sorted(
```

Minimality record: the patch adds one standard-library import and one named conversion stage, then reuses the existing `ideal`, `shares`, `leftover`, `order`, and mutation steps. It changes no public interface and adds no helper, validation branch, feature flag, second workflow, or canonical edit. Converting in place with dense expressions would remove names, not behavior.

## 8. Genuine focused green

Command:

```text
python3 -m pytest -q -p no:cacheprovider test_lost_cent.py::test_equal_exact_remainders_keep_input_order
```

Raw output:

```text
.                                                                        [100%]
1 passed in 0.00s
```

Exit status: `0`.

## 9. Genuine broader and canonical green

Staged command:

```text
python3 -m pytest -q -p no:cacheprovider
```

Raw output:

```text
......                                                                   [100%]
6 passed in 0.01s
```

Exit status: `0`.

The six staged tests cover the new exact tie, the original tied lost-cent case, an even split, an already-integral weighted split, an unequal largest remainder, and `allocate(1, [1, 1, 2]) == [0, 0, 1]` to reject round-then-force-index-zero.

The separate canonical command ran read-only:

```text
python3 -m pytest -q -p no:cacheprovider test_allocation.py test_golden.py
```

Raw output:

```text
.........                                                                [100%]
9 passed in 0.00s
```

Exit status: `0`.

## 10. Agent evidence-boundary statement

The focused red and green prove that the reviewed float implementation misorders the covered mathematical tie and that the exact-rational patch returns `[2, 2, 6]`. The staged broader green protects the previous conservation and policy-discriminating cases. The canonical green shows that all existing behavior and golden tests still pass while canonical files remain unchanged.

The checks do not prove every numeric type or value, non-finite inputs, extreme magnitudes, staged validation behavior, or business fairness. They do not show that decimal-string interpretation is correct for custom numeric classes, and they do not repair or strengthen the read-only canonical implementation.

## 11. Authorial inspection and human-owned policy decision

Inspect the representation boundary before the familiar algorithm. `Fraction(str(weight))` turns each ordinary stated numeric weight into an exact rational before any ideal share is calculated. From there, `ideal`, `leftover`, and `order` retain the chapter's visible largest-remainder stages. The new case matters because conservation alone was green while the tie policy was wrong: `[2, 1, 7]` still totals ten.

For this capture, stable input order applies only after exact rational comparison makes the tie real in the representation. The evidence establishes that behavior for the covered cases. The accepted numeric types, their conversion semantics, and the fairness rule for equal claims remain product decisions for the domain owners.
