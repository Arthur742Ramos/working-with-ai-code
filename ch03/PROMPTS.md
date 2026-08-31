# CH03 Prompts

Prompt blocks extracted from the current manuscript source.

## Debugging a connection error

````text
My Python script crashes with "connection refused" when hitting the API.
````

## Reporting diagnostic results

````text
Service is running, I checked. URL looks right. It worked yesterday. I am not on a VPN.
````

## Sharing network findings

````text
Interesting. It shows the service listening on 127.0.0.1, not 0.0.0.0.
````

## Requesting progress summary

````text
Summarize in five to seven bullets what we have done so far, the assumptions you are currently working from, and the next two possible steps.
````

## Requesting self-critique

````text
Switch to reviewer mode and critique your previous answer. List three things that might be wrong or suboptimal, and three ways to make it more robust.
````

## Requesting test scenarios

````text
Given the solution above, propose unit tests or scenarios that would validate it, and any logging or queries that would confirm it behaves correctly in production.
````

## Requesting production hardening

````text
Take the draft above and refine it toward something usable in production. Focus on error handling, edge cases, logging, and comments where the logic is not obvious.
````

## Requesting minimal safe change

````text
Propose the smallest change that moves us toward the goal while minimizing risk. Explain why it is safer than a larger change.
````

## Checkpointing progress

````text
Before we continue, checkpoint the work. Summarize what we have decided, what we tried that did not work, and what we are currently investigating. I will confirm or correct it, then we continue.
````

## Confirming an implementation plan

````text
Before we implement, confirm my understanding. We are using Redis with a five-minute time to live, invalidating on writes to the users table, and falling back to the database on a cache miss. Is that right?
````

## Opening a branch

````text
I am improving query performance on a users table with ten million rows. I am exploring caching in a separate conversation. Here, consider only database-level options: indexes, query restructuring, and partitioning.
````

## Redirecting conversation focus

````text
Set aside the caching discussion. Here is where we are now. Goal: optimize the three slowest queries. Approach: database indexing only. Constraint: no schema changes, only new indexes. Here are the three queries.
````

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
