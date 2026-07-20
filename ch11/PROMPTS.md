# CH11 Prompts

Prompt blocks extracted from the current manuscript source.

## Reconstructed contract: inspect and reproduce

````text
Inspect `deployment_guard.py`, `deployment.json`, and the focused policy test.
Verify that six replicas with `max_unavailable: 2` pass structural validation
but fail rollout policy. Run the focused test, report the failure, and give the
strict smallest-change plan. Do not edit.
````

## Retained completion direction

````text
Choose the best bounded implementation without another approval checkpoint.
Use `max_unavailable: 1` for this fixture while stating that live capacity
evidence still controls a real deployment. Preserve the exact diff, focused
green, broader green, exit statuses, and actual action sequence.
````
