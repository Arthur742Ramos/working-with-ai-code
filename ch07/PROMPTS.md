# CH07 Prompts

Prompt blocks extracted from the current manuscript source.

## Human contract

````text
Inspect only the staged validator and focused test. The validator lacks a strict `float` type. A built-in float must pass, while `int`, `bool`, and string values must be rejected with `expected float`. Run the focused test, report the failure and its cause, then give the strict smallest-change plan. Do not edit yet.
````
