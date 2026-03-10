# CH03 Prompts

Prompt blocks extracted from the current manuscript source.

## Debugging a connection error

````text
My Python script crashes with "connection refused" when hitting the API.
````

## Reporting diagnostic results

````text
Service is running, I checked. URL looks right. It worked yesterday. I am not on VPN.
````

## Sharing network findings

````text
Interesting. It shows the service listening on 127.0.0.1, not 0.0.0.0.
````

## Requesting retry function

````text
I need a Python function that retries failed HTTP requests with exponential backoff. Start with the simplest version.
````

## Refining retry logic

````text
Good start. But this retries on client errors like 400 and 404, which will never succeed on retry. Only retry on transient errors: timeouts, 429, and 5xx status codes.
````

## Adding retry logging

````text
Now add logging so I can see each retry attempt with the error details and which attempt number it is.
````

## Requesting progress summary

````text
Summarize in five to seven bullet points what we have done so far, what assumptions you are using, and what the next two possible steps are.
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
Take the draft above and refine it toward something I could use in production. Focus on error handling, edge cases, logging, and clear comments where logic is not obvious.
````

## Requesting minimal safe change

````text
Propose the smallest change that moves us toward the goal while minimizing risk. Explain why it is safer than a bigger change.
````

## Checkpointing progress

````text
Before we continue, let us checkpoint our progress. Summarize:
1. What we have decided
2. What we have tried that did not work
3. What we are currently investigating

I will confirm or correct, then we continue.
````

## Confirming implementation plan

````text
We are about to implement the caching approach. Before we start, confirm my understanding: we are using Redis with a five-minute TTL, invalidating on writes to the users table, and falling back to the database on cache miss. Correct?
````

## Exploring caching tradeoffs

````text
Let us explore the caching approach in depth. We will consider the database optimization separately. For now, focus only on caching: what are the tradeoffs and implementation details?
````

## Exploring database optimization

````text
I am exploring options for improving query performance on a users table with 10M rows. In a separate conversation, I am looking at caching. In this conversation, I want to focus only on database-level optimizations: indexes, query restructuring, and partitioning.
````

## Decorator-based rate limiting

````text
I need per-user rate limiting on a FastAPI endpoint. Explore a decorator-based approach using an in-memory store. Single server for now. Target: 100 requests per minute per user.
````

## Identifying the current user

````text
How does the decorator know who the current user is?
````

## Handling stale timestamps

````text
How do we stop old timestamps from piling up?
````

## Probing design limitations

````text
What is the real limitation of this design?
````

## Redis-backed rate limiting

````text
I need per-user rate limiting on a FastAPI endpoint. Explore a Redis-backed approach. The system runs on three servers behind a load balancer. Target: 100 requests per minute per user.
````

## Choosing a window strategy

````text
Fixed window or sliding window?
````

## Ensuring atomic operations

````text
How do we keep the check and the write together?
````

## Handling Redis downtime

````text
What if Redis is unavailable?
````

## Comparing both approaches

````text
I explored two approaches for rate limiting:

Branch A (in-memory decorator): 30 lines, zero dependencies, works on a single server. Loses state on restart. No cross-server coordination.

Branch B (Redis-backed): 50 lines, requires Redis, works across servers. Atomic operations via Lua. Persists across restarts.

We currently run one server but plan to scale to three within six months. Which approach and why?
````

## Fresh start on failing test

````text
I am debugging a failing test. Here is what I know so far: the test_user_login test fails with status 401. The endpoint expects an Authorization header with a Bearer token. The test is sending the token, but the header format might be wrong. Here is the test code and the endpoint code: [paste relevant code]
````

## Resetting stalled debugging

````text
We spent 20 messages discussing slow queries. We looked at indexes on columns user_id, created_at, and status. We ran EXPLAIN ANALYZE on multiple query variants. We discussed connection pooling with pgbouncer. We considered Redis caching. We found that the real issue was a missing WHERE clause in the user activity query. Now I need to apply a similar fix to three other queries that might have the same problem.
````

## Auditing similar queries

````text
We found that a slow query was caused by a missing WHERE clause that triggered a full table scan. I want to audit three other queries for the same pattern. Here are the queries: [paste the three queries]. For each one, check whether the WHERE clause adequately constrains the scan.
````

## Asking what context is needed

````text
I need to add rate limiting to an API endpoint. Before I share code, what information would help you give good advice?
````

## Providing full stack details

````text
I have a FastAPI app on Python 3.11 with three servers behind an AWS ALB. We use Redis 7 for caching, PostgreSQL 15 for persistence, and Celery for background tasks. The API handles 2,000 RPS at peak. I need rate limiting — per-user, 100 requests per minute, with a 429 response. Here is our middleware stack, our auth flow, and the deployment config: [200 lines of code]
````

## Letting the AI ask first

````text
I need to add rate limiting to an API endpoint. Before I share code, what information would help you give good advice?
````

## Restating key constraints

````text
We have been working for a while. Let me restate the key constraints:
- Python 3.11, Django 4.2
- Must maintain backward compatibility with existing API
- Target: 1000 requests per second

Given these constraints, let us continue with the caching implementation.
````

## Redirecting conversation focus

````text
Let us set aside the caching discussion. Here is where we are now:
- Goal: optimize the three slowest queries
- Approach: database-level indexing only
- Constraint: no schema changes, only CREATE INDEX

Here are the three queries: [paste them]
````

## Requesting production review

````text
Review this Python module for production readiness. Focus on: (1) resource management, (2) error handling, (3) data integrity, (4) edge cases. List each issue with its line and severity (critical / major / minor).
````

## Fixing critical issues only

````text
Fix only the two critical issues: the file handle leaks and the division by zero. Keep all other code unchanged. Show the complete updated function.
````

## Checkpointing before deeper changes

````text
Before we continue, summarize: what have we fixed, what remains, and what order should we address the remaining issues?
````

## Hardening timestamp parsing

````text
Fix the timestamp parsing. Support ISO 8601 formats including the T separator and timezone offsets. Use `datetime.fromisoformat` (Python 3.11+). If a timestamp cannot be parsed, skip the event and log a warning instead of crashing.
````

## Questioning timezone defaults

````text
Is treating naive timestamps as UTC the right default? Our event data comes from servers in multiple timezones.
````

## Fixing duplicates and validation

````text
Two more changes: (1) Store unique event types per user using a set, converting to a sorted list for the JSON output. (2) Add input validation — if the "events" key is missing or not a list, raise a ValueError with a clear message.
````

## Requesting self-critique and tests

````text
Critique the final version. What edge cases or failure modes remain? Then propose five test cases that would verify the fixes we made.
````
