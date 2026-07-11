# CH10 Prompts

Prompt blocks extracted from the current manuscript source.

## Illustrative: expose decisions before code

````text
Inspect the reminder domain and the ticket "Let users snooze
reminders." Return unresolved decisions only, grouped under
behavior, identity, time, errors, and persistence.

For repeat behavior and identity, include one pair of concrete inputs
whose outputs differ between plausible interpretations. Do not choose
for the team. Do not propose an architecture. Do not write code.
````

## Controlled implementation: inspect instructions and workspace

````text
Work only in this controlled service-slice repository. Do not edit.
Read the applicable instruction files, `reminders/domain.py`,
`reminders/service.py`, and `tests/test_service.py`.

Report instruction conflicts, base revision, workspace status, runtime,
the focused red result, the only writable file you would need, a short
plan, the check you would rerun, and the stop condition. Do not use the
network, install packages, commit, push, or open a pull request.
````

## Illustrative approval gate: execute the service slice

````text
Approved. Implement the accepted snooze policy by editing only
`reminders/service.py`. Do not edit tests. Rerun the focused service
suite and `git diff --check`. Report changed paths and the result, then
create one local checkpoint commit. Return a handoff packet with the
base revision, checkpoint revision, changed paths, observed checks,
unresolved issues, and next allowed action. Do not push or publish.
````

## Diagnose the SQLite row failure

````text
The failing test is
`test_get_for_user_maps_unsnoozed_reminder` in
`tests/test_sqlite_repository.py`.
Read `reminders/repository.py` and that test, verify the interpreter,
and run only the failing test. Report the one-line cause and a one-line
fix plan. Do not edit yet.
````

## Approve the one-line repair

````text
Approved. Apply only that row-access fix. Run the targeted integration
test, then the full suite. Do not refactor yet and do not change tests.
Show the exact diff and genuine outputs.
````

## Illustrative read-only review contract

````text
Review the frozen hosted pull request at the recorded head commit in
read-only mode. Confirm and record the head commit before reviewing.
Stop and report if the head changes before you finish.
Check contract fidelity, module boundaries, test discrimination,
reader setup, and unsupported delivery claims. Do not edit files,
weaken tests, push, merge, or expand scope.

Report every concrete finding with a file and line. If none survive
verification, say so. Also report the hosted check status and whether
human approval exists. Do not infer either from local test output.
````
