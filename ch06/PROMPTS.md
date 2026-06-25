# CH06 Prompts

Prompt blocks extracted from the current manuscript source.

## Single-shot import request

````text
Write a Python script that imports customers from a CSV file
into our API. Add retries, idempotency, validation, logging,
and a dry-run mode.
````

## Clarify before import planning

````text
I need help building a Python script that imports customers
from a CSV file into an internal API. Before proposing a
design or writing code, ask up to four clarifying questions
that would most change the implementation.

Focus on:
- CSV schema and row identity
- API behavior and retry safety
- Validation and failure policy
- Operational concerns such as logs and dry runs
````

## Plan the importer

````text
Based on those answers, propose a staged implementation
plan. Do not write code yet.

Include:
- The main components
- The order of implementation
- The checks after each stage
- Risks or assumptions I should confirm before coding
````

## Execute the first slice

````text
Implement only step 1 and step 2: parse one CSV row into
a validated `CustomerRow` and derive the idempotency key
from `source_id`. Keep it small. Do not implement API calls.
````

## Execute the retry slice

````text
Good. Now implement the API request builder and retry loop.
Use dependency injection for the sender so I can test retry
behavior without making network calls. Retry only 429 and
5xx responses. Do not add file reading or CLI parsing yet.
````

## Scaffold before filling

````text
Create the module structure for the importer without making
real API calls. Include:
- Data structures for parsed rows and API results
- Function signatures for parse, send, and run
- A dry-run path that can be tested now

For behavior that is not implemented yet, raise
`NotImplementedError` with a specific message. Do not hide
missing behavior behind dummy success values.
````

## One slice: handle the 409 replay

````text
The importer is in `importer.py` with tests in
`test_importer.py`. A new fact from staging: the API returns
`409 Conflict` for a duplicate `source_id` and means "already
created," not an error. Run the tests, then propose a one-line
plan to make a 409 count as a successful replay. Do not edit yet.
````

## Approved

````text
Do it, then run the tests.
````

## Local correction

````text
Keep the current design. Change only the retry function so
`400` responses are not retried. Do not modify parsing,
dry-run behavior, or the request format.
````

## Replan after new evidence

````text
New information: the API does not support idempotency keys.
Stop implementation. Revise the plan for safe retries and
duplicate prevention. Give me two options with tradeoffs.
Do not write code yet.
````

## Reset with clean contract

````text
We are building a Python CSV importer. Current decisions:

- source_id is stable
- API does not support idempotency keys
- invalid rows are skipped and counted
- dry run must send no API calls

Task: propose a duplicate-prevention strategy. Do not code.
````
