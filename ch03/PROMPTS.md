# CH03 Prompts

Prompt blocks extracted from the current manuscript source.

## Requesting production review

````text
Review this Python module for production readiness. Focus on: (1) resource management, (2) error handling, (3) data integrity, and (4) edge cases. Rank the findings as critical, major, or minor. Do not edit yet.
````

## Human contract

````text
Work only on the missing `events` behavior in `event_processor.py`. First run `python3 focused_test.py event_processor.py` and report the result. Then give a one-sentence plan for the smallest reviewable change that fits the surrounding style. Do not edit yet. A missing collection must raise `ValueError` with the stable message `input must be an object with an 'events' key`. An explicit empty list must remain distinct and reach the later empty-result arithmetic, while a valid non-empty input must still work.
````

## Approving the bounded repair

````text
Apply only that guard. Show the exact diff, then rerun the focused check and `python3 full_capture_check.py event_processor.py`.
````

## Illustrative checkpoint for the next turn

````text
Checkpoint this review. Separate what the captured checks verified from the remaining source-inspection concerns. Then identify the unresolved decision that should shape the next bounded ask.
````

## Inspecting timestamp policy

````text
Our emitters run in multiple timezones. Before changing parsing, explain what a timestamp without an offset means, what can go wrong if we assume Coordinated Universal Time (UTC), and which contract choices would make the next implementation request checkable. Do not edit yet.
````
