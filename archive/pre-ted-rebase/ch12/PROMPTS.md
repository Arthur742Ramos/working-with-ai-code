# CH12 Prompts

Prompt blocks extracted from the current manuscript source.

## Inspecting the denominator defect

````text
Work only on the failed-attempt denominator behavior in `workflow_metrics.py`. Read the source and focused test. Run the genuine focused test before editing and report the result. Then give a one-sentence plan. Do not edit yet. Include every terminal success and failure in the denominator, leave pending attempts out, keep `0.80` provisional, and do not authorize rollout from this fixture alone.
````

## Requiring the strict smallest change

````text
Recheck minimality. Preserve the existing successful-attempt list, passing count, and early return if they already satisfy the contract. Revise the plan before editing.
````

## Applying and checking the bounded repair

````text
Apply only that denominator change. Show the exact diff, rerun the focused test, then run the full `test_workflow_metrics` module. Report both exit statuses and do not make a rollout decision.
````
