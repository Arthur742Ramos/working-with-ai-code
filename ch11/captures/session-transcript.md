# Real agent capture: deployment policy repair

Capture date: 2026-07-13

Agent surface: GitHub Copilot CLI

Runtime: CPython 3.14.6

The capture started with `deployment.json` equal to
`deployment-before.json`. Before editing, the agent read the applicable
repository instructions, `deployment.json`, the policy function in
`deployment_guard.py`, and the focused test in
`test_deployment_guard.py`.

## Red

```text
$ python3 -m pytest test_deployment_guard.py::test_production_config_is_safe -q
F                                                                        [100%]
=================================== FAILURES ===================================
________________________ test_production_config_is_safe ________________________

    def test_production_config_is_safe() -> None:
        plan = load_plan(CONFIG)

>       assert policy_violations(plan) == []
E       AssertionError: assert ['max_unavail...st be 0 or 1'] == []
E
E         Left contains one more item: 'max_unavailable must be 0 or 1'
E         Use -v to get more diff

test_deployment_guard.py:21: AssertionError
=========================== short test summary info ============================
FAILED test_deployment_guard.py::test_production_config_is_safe - AssertionEr...
1 failed in 0.02s
```

The read-only diagnosis reported the observed value `2`, the checked values
`0` and `1`, and the unresolved human decision: whether five ready replicas
were the required capacity floor.

## Approved diff

After the service-owner decision in the chapter prompt, the agent changed one
value and no test or policy:

```diff
  "rollout": {
    "batch_size": 2,
-    "max_unavailable": 2
+    "max_unavailable": 1
  },
```

## Green

```text
$ python3 -m pytest test_deployment_guard.py::test_production_config_is_safe -q
.                                                                        [100%]
1 passed in 0.01s
```

The full suite at the captured point also passed:

```text
$ python3 -m pytest -q
..........                                                               [100%]
10 passed in 0.03s
```

Later manuscript hardening added separate tests for mixed-offset timeline
ordering and a representative post-change request. Those additions do not
change the captured one-line repair. The current suite count is therefore
higher than the count recorded above.
