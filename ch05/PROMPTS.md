# CH05 Prompts

Prompt blocks extracted from the current manuscript source.

## Role-driven code review

````text
You are a senior software engineer reviewing code for production readiness. Focus on:
- Error handling completeness
- Edge cases and failure modes
- Performance implications at scale
- Security considerations

Review this function: [code]
````

## Constrained code generation

````text
Write a Python function to validate email addresses.

Constraints:
- Python 3.11, standard library only (no external dependencies)
- Return a dataclass with fields: is_valid, reason, normalized_address
- Maximum 30 lines including docstring
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

## Explain pattern — stack trace analysis

````text
Explain this stack trace to a developer who is not familiar with this codebase. Focus on the root cause, not every frame:

```
Traceback (most recent call last):
  File "app/api/handlers.py", line 42, in handle_request
    result = await service.process(payload)
  File "app/services/processor.py", line 87, in process
    validated = self.schema.load(data)
  File "venv/lib/marshmallow/schema.py", line 722, in load
    return self._do_load(data, many=many, partial=partial)
marshmallow.exceptions.ValidationError: {'email': ['Not a valid email address.']}
```
````

## Critique pattern — targeted code review

````text
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
````

## Explain the existing code (pattern chaining step 1)

````text
What does this function do? Walk me through the logic step by step.

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
````

## Critique for the specific failure (pattern chaining step 2)

````text
Users report duplicates despite this function running. What could cause deduplication to fail? Consider: case sensitivity, whitespace, unicode normalization, and timing issues.
````

## Generate a fixed version (pattern chaining step 3)

````text
Write a corrected version that normalizes emails before comparison. Lowercase the entire address and strip whitespace. Keep the same interface.
````

## Transform tests to cover the fix (pattern chaining step 4)

````text
Convert these unittest test cases to pytest. Add cases for mixed-case emails and whitespace.
````

## Data migration with full building blocks

````text
Role: Database engineer who prioritizes data integrity over speed. This migration runs on production data that cannot be recovered if corrupted.

Task: Migrate user records from legacy schema to new schema.

Constraints:
- Python 3.11 with psycopg2
- Must be idempotent (safe to run multiple times)
- Log every transformation for audit
- Validate data before writing
- Batch size of 1000 rows maximum

Example transformation (one row):
Old: {"created": "03/15/2024", "name": "Jane Doe", "type": "1"}
New: {"created_at": "2024-03-15T00:00:00Z", "full_name": "Jane Doe", "account_type": "individual"}

Steps:
1. Read and validate source data
2. Transform each field
3. Validate against new schema
4. Write with transaction rollback on error
5. Log summary statistics
````
