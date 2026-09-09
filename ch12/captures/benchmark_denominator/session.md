# Benchmark denominator session

Capture stage: complete red, patch, focused green, broader green, and replay package.

## 1. Human contract

The following bounded contract is retained from the current author direction and condensed without changing its substance. It is not presented as a vendor quotation.

> Work only inside the staged benchmark denominator package. Inspect the before source and focused test, run the genuine red before editing, include every terminal success and failure in the denominator, keep `0.80` provisional, and do not authorize rollout from this fixture alone. Choose the best implementation without another approval checkpoint. Apply the strict smallest production diff only to disposable or after-state material, preserve exact machine evidence and the actual action record, add non-recording replay, and keep canonical chapter and code files unchanged. Stop with an honest blocker if the red is missing, the patch is not strictly minimal, or green cannot be reproduced.

## 2. Inspection and pre-edit instruction

The agent read `AGENTS.md`, the real-session capture standard, and every staged package file before running a command. The before source filters attempts to `status == "succeeded"`, counts scores that meet the threshold in that filtered list, and divides by the same list length. The focused test supplies one qualifying success and one failure and requires `0.50`.

Before any edit, the agent ran only:

```text
python3 -m unittest -v test_workflow_metrics.QualitySuccessRateTests.test_failed_attempts_remain_in_denominator
```

The runner copied the checksum-verified source and test into disposable space. Canonical source and test checksums were recorded as:

```text
workflow_metrics.py      42d9a1372ecdaedfa7283509018d7c38be5576d27eb36b3cb453105ab5198fbd
test_workflow_metrics.py 330a35b8120cb44b5859db467ba578cb557e8d163d9df361dc36dcbf7d582736
```

## 3. Genuine focused red and agent observation

```text
test_failed_attempts_remain_in_denominator (test_workflow_metrics.QualitySuccessRateTests.test_failed_attempts_remain_in_denominator) ... FAIL

======================================================================
FAIL: test_failed_attempts_remain_in_denominator (test_workflow_metrics.QualitySuccessRateTests.test_failed_attempts_remain_in_denominator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<capture-workdir>/test_workflow_metrics.py", line 21, in test_failed_attempts_remain_in_denominator
    self.assertEqual(rate, 0.50)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: 1.0 != 0.5

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

Exit status: `1`.

Agent observation: the input contains two terminal attempts, but the implementation removes the failure before division and returns `1.0`; the contract requires one qualifying outcome over two terminal attempts, or `0.5`.

## 4. One-sentence plan and minimality revision

Initial plan, recorded before the first disposable edit: build one list containing only `succeeded` and `failed` attempts, return zero when that list is empty, count a pass only when a terminal attempt both succeeded and met the quality minimum, and divide by the terminal count without changing pending or threshold behavior.

That candidate passed the focused and broader checks, but the independent minimality challenge refuted it. The existing success filter already computes the correct numerator and its empty-success early return is correct for failed-only and nonterminal-only inputs. Changing those lines was unnecessary.

Revised strict-smallest-change plan: leave the existing successful-attempt list, passing count, and early return unchanged; replace only the final denominator with the count of attempts whose status is explicitly `succeeded` or `failed`.

## 5. Approval basis and agent-selected policy expression

The bounded edit proceeded under the author's standing direction to choose the best implementation without another approval checkpoint. The author specified the behavior and policy boundary, not a particular code option.

The final agent-selected expression counts only explicit `{ "succeeded", "failed" }` statuses in the denominator. This implements the supplied policy without treating every non-pending or unknown value as terminal. The quality threshold remains a function input; no code in this patch fixes `0.80` as a universal standard or authorizes rollout.

## 6. Actual agent action record

1. Read the governing repository instructions, capture standard, before source, focused test, red evidence, red-only runner, metadata, README, session record, parity ledger, and package ignore rules.
2. Snapshotted repository commit `38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6`, confirmed that the target chapter source was not yet present, and recorded the two support checksums.
3. Ran the existing default replay and reproduced the genuine focused red with `AssertionError: 1.0 != 0.5` and test exit status `1`.
4. Copied the before source and focused test into disposable space, applied the initial terminal-list candidate, generated a machine diff, and observed focused and broader green.
5. Replaced the red-only runner with full record and non-recording replay behavior and recorded the first complete evidence set.
6. Challenged patch minimality and found that changing the numerator path was unnecessary. The first candidate was rejected and is not the stored production patch.
7. Created a fresh disposable copy, changed only the final denominator, and reran the focused test plus all four broader tests. Both passed with exit status `0`.
8. Regenerated `patches/production.diff` mechanically from the immutable before source to the final disposable source. The final patch checksum is `afdf96e67644b9a2db08e695aae3bfb49032f2b431ae445819653545827b8ba6`.
9. Rerecorded red, patch-apply, focused-green, and broader-green evidence from a clean disposable state using the final patch.
10. Ran checksum-locked default replay from a clean state. It reproduced red, applied the exact final patch, reproduced both greens, confirmed canonical support parity, and removed disposable work.

## 7. Exact machine-generated final diff

```diff
--- a/workflow_metrics.py
+++ b/workflow_metrics.py
@@ -23,4 +23,7 @@
         attempt.quality_score >= minimum_quality
         for attempt in successful_attempts
     )
-    return passing_count / len(successful_attempts)
+    return passing_count / sum(
+        attempt.status in {"succeeded", "failed"}
+        for attempt in attempts
+    )
```

## 8. Genuine focused green

Command:

```text
python3 -m unittest -v test_workflow_metrics.QualitySuccessRateTests.test_failed_attempts_remain_in_denominator
```

Output:

```text
test_failed_attempts_remain_in_denominator (test_workflow_metrics.QualitySuccessRateTests.test_failed_attempts_remain_in_denominator) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Exit status: `0`.

## 9. Genuine broader green

Command:

```text
python3 -m unittest -v test_workflow_metrics
```

Output:

```text
test_failed_attempts_remain_in_denominator (test_workflow_metrics.QualitySuccessRateTests.test_failed_attempts_remain_in_denominator) ... ok
test_no_terminal_attempts_returns_zero (test_workflow_metrics.QualitySuccessRateTests.test_no_terminal_attempts_returns_zero) ... ok
test_pending_attempts_are_excluded (test_workflow_metrics.QualitySuccessRateTests.test_pending_attempts_are_excluded) ... ok
test_successes_are_checked_for_quality (test_workflow_metrics.QualitySuccessRateTests.test_successes_are_checked_for_quality) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

Exit status: `0`.

## 10. Agent evidence-boundary statement

The focused red and green discriminate whether a failed terminal attempt remains in the denominator. The broader suite protects three neighboring behaviors: a successful attempt below the quality minimum does not pass, pending attempts do not enter the denominator, and an input with no terminal attempts returns zero.

These checks do not validate `0.80` as a production threshold, benchmark representativeness, sample size, failure taxonomy, target-system behavior, or rollout safety. The exact final patch is sufficient for the staged behavior. It is not evidence that the workflow should be standardized or widened.

## 11. Author inspection and human-owned decision

No post-capture author inspection is claimed. Before chapter integration, the author or workflow owner must inspect the preserved final diff and evidence. The standing author decision for this slice is already explicit: include every terminal success and failure, keep `0.80` provisional, and do not authorize rollout from this fixture alone.

Any future rollout decision remains human-owned and requires representative benchmark scope plus operational evidence outside this package.
