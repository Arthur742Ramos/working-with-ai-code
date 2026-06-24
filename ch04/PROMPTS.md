# CH04 Prompts

Prompt blocks extracted from the current manuscript source.

## Email validation library request

````text
I need a Python library to validate email addresses according to RFC 5321. What do you recommend?
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

## Regression check against known answers

`````text
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
`````

## Broad Django performance request

````text
My Django application is slow. How can I improve performance?
````

## Specific Django query follow-up

````text
You said to "optimize the database queries." Which specific queries in the code I shared would you optimize, and how? Show me the before and after for each one.
````

## Handing the agent the incident

````text
We have a SEV-2 on order-service. The `/orders/{id}/summary` endpoint is intermittently slow and throwing 500s since 14:30. No deploy went out; the only change was a bulk product-catalog import last night. The brief is in `code/ch04/incident_demo/incident.md`. Reproduce it locally and find the cause or causes before proposing anything.
````

## Chase the deterministic failure first

````text
Start with the 500s, since they are deterministic. Why does the same order fail every time?
````

## Now the latency tail

````text
That explains the 500s. Now the tail: why only large orders, and why does it seem to warm up after a restart?
````

## The smallest correct fix, as a diff

````text
Propose the minimal correct fix for both causes. Implement it as a diff against the original `server.py` without editing the shipped file, and prove the diff applies cleanly.
````

## Prove it on the numbers, and be honest

````text
Now verify it actually moves the numbers. Re-run the same load test against the fixed copy, show me before and after, and be honest if the tail did not move as much as you expected.
````
