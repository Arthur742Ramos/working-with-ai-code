# CH04 Prompts

Prompt blocks extracted from the current manuscript source.

## Clarify the importer

````text
Before proposing a design or writing code, ask up to four
questions that would most change this importer. Focus on row
identity, retry safety, invalid rows, and dry-run behavior.
````

## Human contract

````text
The importer is in `importer.py` with tests in
`test_importer.py`. The supplied contract says this exact
endpoint returns `409 Conflict` for the same stable
`source_id` and idempotency key to mean "already created."
Inspect the files and run only
`test_conflict_is_idempotent_replay` before editing. Report
the red result and a one-sentence strict-smallest-change plan.
After approval, apply only the bounded edit, then run the
focused test and the full test file. Do not generalize other
conflicts.
````

## Apply the approved slice

````text
Apply only that bounded change. Run the focused test, then
run the full test file. Show the actual outputs.
````
