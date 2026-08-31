# CH01 Prompts

Prompt blocks extracted from the current manuscript source.

## Adding a check constraint

````text
This looks right. Add a check constraint so the stored JSON is always an object, never an array or a primitive.
````

## Inspect the fallback signal

````text
Inspect `app.py` and run the focused fallback-observability test before editing. Keep the existing bounded fail-open overload policy, per-user key, Redis storage, and ten-per-minute limit. Add one real application-visible fallback signal. Plan first and do not edit yet. Stop if the focused test does not reproduce the failure or if the repair cannot stay reviewable.
````

## Challenge the repair

````text
Challenge the implementation against the strict smallest production diff. Preserve the accepted fallback behavior and require the existing library warning to reach the application logger. Reject any extra mechanism the library already provides.
````
