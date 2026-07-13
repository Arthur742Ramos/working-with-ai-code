# CH11 Prompts

Prompt blocks extracted from the current manuscript source.

## Inspect the failed production-policy check

````text
Read the applicable repository instructions, `deployment.json`,
`deployment_guard.py`, and the focused production-config test. Do not edit.
Run only
`test_deployment_guard.py::test_production_config_is_safe`.
Report the observed configuration value, the checked policy, the exact red
result, the smallest possible fix, and the decision that the files cannot
justify. Do not run a provider command or use a credential.
````

## Approve the one-line configuration repair

````text
The service owner confirms that production requires five of six replicas
available during this rollout. Approved: change only
`rollout.max_unavailable` from `2` to `1`. Do not change the test or policy.
Show the exact diff, rerun the focused test, then run the full test
suite. Stop if any other path changes.
````
