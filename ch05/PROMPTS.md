# CH05 Prompts

Prompt blocks extracted from the current manuscript source.

## Name the orphaned-product failure

````text
Inspect `seed.py`, `server.py`, and the focused check. Run
the focused check before editing, and do not edit until you
have observed the failure and stated a one-sentence plan.
When an order contains a product code absent from the
catalog, require a named `MissingProductError` that
identifies the order and missing code. Fail the summary
closed at the API boundary while upstream data is repaired.
Do not change valid summaries or invent a missing price.
````

## Apply the bounded repair

````text
Apply the one-sentence plan as the smallest reviewable diff.
Preserve valid summaries, do not repair upstream data, and
show the exact production diff before the focused and broader
checks.
````

## Show focused and broader evidence

````text
Run the focused check, then the broader check. Show the raw
output and state what these checks do not establish.
````
