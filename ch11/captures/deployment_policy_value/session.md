# Deployment-policy value session

Capture status: coding-agent session complete; independent review pending.

## Provenance

This session started from the staged inspection, red, and plan package. The initial bounded contract is reconstructed and labeled because its standalone prompt was not retained. The current completion direction is retained. Inspection, the harness correction, the command sequence, the production action, the machine-generated diff, and the green runs come from the current Claude Code tool log. The transcript is condensed for readability without changing command results.

## 1. Human contract

**Reconstructed initial bounded contract:**

> Inspect `deployment_guard.py`, `deployment.json`, and the focused policy test before editing. Show that the six-replica proposal with `max_unavailable: 2` passes the structural check but fails the rollout policy. Run the focused test and report the failure, then give the strict smallest-change plan. Do not edit yet.

**Retained completion direction:** choose the best implementation without another approval checkpoint. Keep canonical chapter and code files unchanged. Use `max_unavailable: 1` for this fixture while stating that live capacity evidence still controls a real deployment. Preserve genuine red, exact diff, focused green, broader green, exit statuses, and the actual action sequence.

## 2. Inspection before editing

The agent read the staged source, configuration, focused test, capture standard, and maintained Chapter 11 tests.

- `before/deployment_guard.py` accepts only integer `max_unavailable` values `0` and `1` under the maintained rollout policy.
- `before/deployment.json` declares six replicas and sets `max_unavailable` to `2`.
- The narrow schema check accepts `2` because it is an integer between zero and the replica count.
- The maintained broader suite checks the safe configuration, the preserved unsafe fixture, command output, incident selection, and pipeline behavior.

The immutable source and configuration checksums match their recorded origin hashes. Original chapter and support checksums remain historical provenance; final-package replay verifies only package-local files.

## 3. Capture-harness correction before the final red

The first staged replay reproduced the intended policy failure, but inspection found that the focused test also asserted `plan.max_unavailable == 2`. That line made the test permanently red after a configuration-only repair.

The agent changed only that package-local assertion to compare the loaded value with the current configuration. This kept the loader check while allowing the same focused test to discriminate before and after states. The agent then reran the before state and reproduced the genuine red shown below. No production or canonical file changed during this correction.

## 4. Genuine focused red

Command:

```bash
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_policy.py::\
test_schema_valid_deployment_satisfies_policy
```

Working directory: disposable before-state copy.

Exit status: `1`

Stored output (elapsed time normalized only):

```text
F                                                                        [100%]
=================================== FAILURES ===================================
________________ test_schema_valid_deployment_satisfies_policy _________________

    def test_schema_valid_deployment_satisfies_policy() -> None:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
    
        assert _schema_accepts_max_unavailable(data)
        plan = load_plan(CONFIG)
        assert plan.max_unavailable == data["rollout"]["max_unavailable"]
>       assert policy_violations(plan) == []
E       AssertionError: assert ['max_unavail...st be 0 or 1'] == []
E         
E         Left contains one more item: 'max_unavailable must be 0 or 1'
E         Use -v to get more diff

test_deployment_policy.py:28: AssertionError
=========================== short test summary info ============================
FAILED test_deployment_policy.py::test_schema_valid_deployment_satisfies_policy
1 failed in <TIME>s
```

Agent observation: the value `2` is structurally valid and loads correctly, but the actual rollout guard returns exactly one policy violation. Structural acceptance does not establish operational approval.

## 5. One-sentence strict-smallest-change plan

Change only `rollout.max_unavailable` in `deployment.json` from `2` to `1`, then run the same focused test and the maintained Chapter 11 suite against the disposable after-state.

## 6. Approval basis and selected policy

The standing direction authorized the coding agent to choose the best bounded implementation without another checkpoint. Acting under that direction, the agent selected `max_unavailable: 1` for the six-replica fixture because it is the largest value accepted by the maintained policy and preserves five ready replicas if one becomes unavailable.

This record does not claim that the author named an option from a menu. It records the standing approval basis, the agent's bounded selection, and the stated operational limit: live capacity evidence still controls a real deployment.

## 7. Actual agent action record

The machine-readable sequence is preserved in `evidence/agent-actions.jsonl`. In order, the agent inspected the staged and original inputs, replayed the initial red-only package, diagnosed and corrected the package-local test seam, reran genuine red, stated the one-line plan, selected the fixture policy under standing direction, edited only `.work/deployment.json`, generated the unified diff, ran focused green, ran the broader suite against the disposable after-state, and ran the original canonical support suite read-only.

No original chapter or canonical code file changed during that session. `metadata.json` preserves their recorded hashes as historical provenance. Current replay does not resolve those paths; it checks the isolated final package before and after every disposable run.

## 8. Exact applied production diff

The agent generated this patch with `diff -u` from the immutable before fixture and the disposable after-state:

```diff
--- a/deployment.json
+++ b/deployment.json
@@ -6,7 +6,7 @@
   "replicas": 6,
   "rollout": {
     "batch_size": 2,
-    "max_unavailable": 2
+    "max_unavailable": 1
   },
   "health": {
     "readiness_path": "/ready",
```

The patch substitutes one production line and touches no second field. A zero-line production change leaves the focused violation intact. Changing the guard would broaden accepted rollout behavior instead of repairing the proposal. No smaller production patch satisfies the selected contract.

## 9. Genuine focused green

Command:

```bash
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_policy.py::\
test_schema_valid_deployment_satisfies_policy
```

Working directory: disposable after-state copy.

Exit status: `0`

Stored output (elapsed time normalized only):

```text
.                                                                        [100%]
1 passed in <TIME>s
```

## 10. Genuine broader green

The runner copied an explicit manifest of package-local operational files into disposable space, overlaid the byte-checked before source, applied the one-line configuration repair, and ran:

```bash
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_guard.py \
  test_incident_triage.py \
  test_pipeline.py
```

Exit status: `0`

Stored output (elapsed time normalized only):

```text
........................                                                 [100%]
24 passed in <TIME>s
```

During the original session, the same command also ran in the canonical support directory without editing it:

```text
........................                                                 [100%]
24 passed in <TIME>s
```

Exit status: `0`. That output remains checksum-preserved as origin provenance with replay status `preserved_not_executed`.

The isolated final package later added five listing-parity checks. Current replay runs its top-level suite separately:

```text
.............................                                            [100%]
29 passed in <TIME>s
```

Exit status: `0`.

## 11. Evidence boundary

The red result proves that `2` passes the narrow structural check and reaches the maintained policy boundary. Focused green proves that the one-line value substitution removes that violation. Broader green proves that 24 deployment, incident, and pipeline cases pass against the disposable after-state. The preserved canonical-support result proves only what ran during the original session. Final-package green proves that the 24 operational checks and five exact listing-parity checks pass together without repository-root support.

These checks do not prove that five ready replicas can serve peak traffic, that repository state matches a live target, that provider-side planning is safe, or that rollback will work. No credential, cloud API, production write, live health signal, or traffic observation appears in this session.

## 12. Author inspection and human-owned decision

The retained direction fixes the teaching fixture at `max_unavailable: 1` and requires the record to keep live capacity evidence in control of a real deployment. The fixture demonstrates how a repository policy can block and then accept a bounded proposal. It does not justify the policy from production facts.

The service owner or release team still owns the live decision. Before deployment, that team must verify that five ready replicas can carry current peak traffic, preserve service objectives, and leave enough rollback headroom. If the evidence does not support that floor, the deployment contract must change before any write.

## 13. Review gate

The coding-agent session and isolated replay package are complete. The capture standard still requires an independent reviewer to replay from clean state, try to refute patch minimality, compare the staged Chapter 11 excerpt with the top-level parity ledger, and confirm that the live capacity decision remains human-owned before marking the ledger `Pass`.
