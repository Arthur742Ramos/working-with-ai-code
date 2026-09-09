# CH10 Prompts

Prompt blocks extracted from the current manuscript source.

## Illustrative: expose the snooze decisions

````text
Inspect the accepted reminder states and the request "Let users
snooze reminders." Return unresolved behavior decisions only. For
each decision, give the smallest pair of concrete inputs whose
expected outputs would differ between plausible interpretations.
Include repeat snooze, trusted identity, completed state, time zone,
and storage. Do not choose a policy, design modules, or write code.
````

## Reconstructed contract: inspect the row seam

````text
Inspect `reminders/repository.py` and the focused SQLite test.
Run `test_get_for_user_maps_unsnoozed_reminder` against the before
state before editing. The adapter must convert a real `sqlite3.Row`
for an unsnoozed reminder without calling an unsupported mapping
method. Report the failing seam, one-line cause, and strict smallest
plan. Keep tests and all other production files unchanged.
````
