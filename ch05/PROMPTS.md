# CH05 Prompts

Prompt blocks extracted from the current manuscript source.

## The perfect prompt missing the task

````text
You are a senior backend engineer.

Constraints:
- Python 3.11
- No external dependencies
- Maximum 50 lines
- Type hints required

Follow these examples for the output format:

Input: "alpha"
Output: {"valid": true, "value": "alpha", "errors": []}

Input: ""
Output: {"valid": false, "value": null, "errors": ["empty"]}

Input: "beta"
Output: {"valid": true, "value": "beta", "errors": []}

Steps:
1. Validate the input.
2. Transform it.
3. Return the result.
````

## Review as a security auditor

`````text
You are a senior security auditor. Review this function for security vulnerabilities only. List the top issues, each with a severity and a one-line fix.

```python
def list_active_users(conn, sort_field):
    query = (
        "SELECT id, email, created_at FROM users "
        f"WHERE active = 1 ORDER BY {sort_field}"
    )
    rows = conn.execute(query).fetchall()
    return [
        {"id": row[0], "email": row[1],
         "created_at": row[2]}
        for row in rows
    ]
```
`````

## Review as a performance engineer

````text
You are a senior performance engineer. Review the same `list_active_users` for performance and scalability issues only. List the top issues, each with a one-line fix.
````

## Constrained code generation

````text
Write a Python function to validate email addresses.

Constraints:
- Python 3.11, standard library only (no external dependencies)
- Return a dataclass with fields: is_valid, reason, normalized_address
- Normalize valid addresses: trim surrounding whitespace, lowercase the domain
- Handle edge cases: empty string, missing @, multiple @ symbols
- Raise ValueError for non-string input
````

## Few-shot user story conversion

````text
Convert informal descriptions to user stories.

Input: "Users need to reset their passwords"
Output: "As a registered user, I want to reset my password via email so that I can regain access to my account if I forget my credentials."

Input: "The app is slow when loading the dashboard"
Output: "As a user, I want the dashboard to load in under 2 seconds so that I can quickly access my daily metrics without waiting."

Now convert: "We need better error messages"
````

## Explain category: stack trace analysis

`````text
Explain this stack trace to a developer who is not familiar with this codebase. Focus on the root cause, not every frame:

```
Traceback (most recent call last):
  File "app/api/handlers.py", line 42, in handle_request
    result = await service.process(payload)
  File "app/services/processor.py", line 87, in process
    validated = self.schema.load(data)
  File "venv/lib/marshmallow/schema.py", line 722, in load
    return self._do_load(data, many=many, partial=partial)
marshmallow.exceptions.ValidationError:
    {'email': ['Not a valid email address.']}
```
`````

## Critique category: targeted code review

`````text
Review this function for bugs that would cause incorrect behavior at runtime. Focus on logic errors, not style.

```python
def calculate_discount(price, quantity):
    if quantity > 100:
        discount = 0.2
    elif quantity > 50:
        discount = 0.1
    elif quantity > 10:
        discount = 0.05
    return price * quantity * (1 - discount)
```
`````

## Explain the existing code

`````text
Explain what the deduplicate_users function in dedup.py does, step by step. Do not change anything yet.

```python
def deduplicate_users(users):
    seen = set()
    unique = []
    for user in users:
        if user['email'] not in seen:
            seen.add(user['email'])
            unique.append(user)
    return unique
```
`````

## Critique for the specific failure

````text
Users still report duplicates in production even though this runs on every import. What could make deduplication fail on real data? Consider case sensitivity, whitespace, and unicode normalization. Don't change code yet, just diagnose.
````

## Reproduce the bug as a failing test

````text
Before changing the function, reproduce the case-sensitivity bug as a test: add a pytest test asserting that `Bob@Example.com` and `bob@example.com` collapse to one user. Run pytest and show me the output. Do not modify dedup.py yet.
````

## Generate the fix

````text
Apply the fix for the in-batch case: normalize each email by stripping whitespace and lowercasing before the membership check. Keep the same signature and return shape. Edit dedup.py directly, then re-run pytest.
````

## Transform tests and run them

````text
Convert the remaining unittest test in test_dedup.py to pytest style, and add one test for surrounding whitespace. Then run pytest and show me the output.
````

## Bare migration prompt

````text
Write a Python script to migrate the legacy_users table into the new accounts schema. The two schemas are in schema_legacy.sql and schema_new.sql.
````

## Data migration with the full template

````text
Role: data engineer who prioritizes data integrity over speed. This runs on production data that cannot be recovered if corrupted.

Read schema_legacy.sql and schema_new.sql, then write migrate.py (Python 3, sqlite3) that migrates legacy_users into accounts.

Constraints:
- Idempotent: safe to run multiple times (upsert on id)
- Transform each field: created "MM/DD/YYYY" to ISO 8601; type "1" to individual, "2" to business; strip and lowercase email; strip name
- Validate every row; skip and report rows that fail
- Write one audit row for every field whose value changed shape
- Wrap the run in a transaction; roll back on any error
- Support a --dry-run flag that does all the work, then rolls back, printing a summary

Steps: read the schemas, write migrate.py, then run it with --dry-run and show me the summary plus three sample audit rows.
````
