# CH02 Prompts

Prompt blocks extracted from the current manuscript source.

## Ask for a PR description

````text
Write a PR description for this diff:

[a staged validation diff]
````

## Inspect the retry wiring

````text
The CLI appears to bypass the existing conversational retry path after malformed structured output. Inspect `pr_generator.py` and the focused test. Run a discriminating red check, state the strict smallest-change plan, and identify the retry policy a human must own. Do not edit production code yet.
````

## Apply the bounded repair

````text
Reuse the existing helper unchanged. Retry JSON and schema failures, allow two retries for three attempts total, and apply the strict smallest production diff. Then run the focused check and the broader neighboring checks.
````
