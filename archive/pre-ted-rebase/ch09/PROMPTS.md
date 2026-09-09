# CH09 Prompts

Prompt blocks extracted from the current manuscript source.

## Complete the local repair within the boundary

````text
Repair `send_alert` through the approved shared client. Inspect the affected code and current rule, reproduce the focused failure, make the repair, and run the focused test plus the house-rule guard. The local tests use injected transports and make no live calls. Correct failures caused by this repair and rerun affected checks without asking again. Finish with the diff and check results. Do not send a live notification, weaken tests, change credentials, or expand the task. If progress requires one of those actions or an unresolved policy choice, report the blocker.
````

## Inspect the seam before editing

````text
Inspect `alerts.py`, the focused alert-routing test, the executable house-rule guard, and the shared client interface. Before editing, run the focused test against the staged before state. Require `send_alert` to route the existing method, URL, and JSON payload through `http_client.call`, while the broader guard still rejects `requests` and any other direct transport. Report genuine red and the smallest-reviewable-change plan. Preserve readable idiom; do not weaken tests, add dependencies, or edit canonical files.
````
