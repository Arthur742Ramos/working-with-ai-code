# CH09 Prompts

Prompt blocks extracted from the current manuscript source.

## Inspect the seam before editing

````text
Inspect `alerts.py`, the focused alert-routing test, the executable house-rule guard, and the shared client interface. Before editing, run the focused test against the staged before state. Require `send_alert` to route the existing method, URL, and JSON payload through `http_client.call`, while the broader guard still rejects `requests` and any other direct transport. Report genuine red and the smallest-reviewable-change plan. Preserve readable idiom; do not weaken tests, add dependencies, or edit canonical files.
````
