# CH04 Prompts

Prompt blocks extracted from the current manuscript source.

## Email validation library request

````text
I need a Python library to validate email addresses according to RFC 5321. What do you recommend?
````

## HTTPX JSON POST request

````text
How do I make an HTTP POST request with a JSON body and a 10-second timeout in Python using httpx?
````

## SQLAlchemy pool default question

````text
What is the default maximum connection pool size for SQLAlchemy when using PostgreSQL?
````

## Current UTC time in Python

````text
How do I get the current UTC time in Python?
````

## Slow orders query explanation

````text
This query is slow on a table with 5 million rows:
```sql
SELECT * FROM orders
WHERE customer_id = 42 AND status = 'pending'
ORDER BY created_at DESC LIMIT 10;
```
I have an index on `(status, created_at)`. Why is it still doing a sequential scan?
````

## Devil's advocate critique

````text
Before I implement the solution above, play devil's advocate:
- What could go wrong with this approach?
- What assumptions does this approach make that might be false?
- What edge cases might break this?
- If this fails in production, what would the most likely cause be?
````

## Targeted risk review

````text
Review the code above specifically for:
1. Race conditions or concurrency issues
2. Memory leaks or resource exhaustion
3. Inputs that would cause unexpected behavior
4. Security vulnerabilities (injection, auth bypass)

For each category, either identify a specific concern or explain why it does not apply here.
````

## Arguing against Redis

````text
You recommended using Redis for caching. Now argue the case for NOT using Redis. What are the strongest reasons to choose a different approach?
````

## Known-answer regression check

````text
Here is a working function that I know is correct:

```python
def calculate_tax(price, rate):
    return round(price * rate, 2)
```

Your proposed refactored version should produce identical results for these inputs:
- calculate_tax(100.00, 0.0825) -> 8.25
- calculate_tax(49.99, 0.07) -> 3.5
- calculate_tax(0.01, 0.10) -> 0.0

Walk through each case with your version and confirm the output matches.
````

## Broad Django performance request

````text
My Django application is slow. How can I improve performance?
````

## Specific Django query follow-up

````text
You said to "optimize the database queries." Which specific queries in the code I shared would you optimize, and how? Show me the before and after for each one.
````

## Django QuerySet evaluation follow-up

````text
Can you explain exactly when the Django ORM evaluates a QuerySet? I'm using select_related with pagination and I'm not sure when the actual SQL runs.
````
