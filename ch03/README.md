# Chapter 3: Conversations, not single prompts

This chapter covers iterative, multi-turn conversations with AI — the ask-inspect-adjust loop, checkpoints, branch points, summarizing and resetting long sessions — and applies them in a conversation-driven code review that transforms flawed code into production-ready code.

## Setup

```bash
pip install -r requirements.txt
```

## Code Listings

| File | Description |
|------|-------------|
| `listing_3_1_rate_limiter_decorator.py` | Branch A: in-memory decorator-based rate limiter (FastAPI, single server) |
| `listing_3_2_rate_limiter_redis.py` | Branch B: Redis-backed rate limiter with Lua script (FastAPI, multi-server) |
| `listing_3_3_event_processor_start.py` | Starting code with hidden issues (file leaks, division by zero, rigid parsing) |
| `listing_3_5_event_processor_critical_fix.py` | After fixing critical issues only (context managers, division-by-zero guard) |
| `listing_3_6_timestamp_parsing.py` | Robust ISO 8601 timestamp parsing with graceful fallback |
| `listing_3_7_event_processor_final.py` | Final version with all issues resolved (validation, dedup, logging) |
| `listing_3_8_test_event_processor.py` | Test cases verifying each fix made during the review |

### Iterative improvement chain

Listings 3.3 → 3.5 → 3.6 → 3.7 show the same module evolving through conversation-driven code review:

1. **3.3** — Starting code with six hidden issues
2. **3.5** — Critical fixes only (file handles, division by zero)
3. **3.6** — Robust timestamp parsing extracted as a helper
4. **3.7** — Final version with input validation, deduplicated types, and logging

Listing 3.4 (the AI's review response) is prose, not runnable code. It identifies six issues with severity ratings:

```
1. [CRITICAL] File opened without context manager — handle leaks on error
2. [CRITICAL] Division by zero when no users match the date filter
3. [MAJOR]    Timestamp parsing assumes single format, no timezone support
4. [MAJOR]    Output file opened without context manager
5. [MAJOR]    Event types list grows without bound, includes duplicates
6. [MINOR]    No input validation on data structure
```

### Branching example

Listings 3.1 and 3.2 demonstrate exploring two approaches in separate conversations:

- **Branch A** (3.1): Simple, zero dependencies, single-server only
- **Branch B** (3.2): Redis dependency, works across multiple servers

## Key Prompts

### The ask-inspect-adjust loop

```
Review this Python module for production readiness. Focus on:
(1) resource management, (2) error handling, (3) data integrity,
(4) edge cases. List each issue with its line and severity
(critical / major / minor).
```

```
Fix only the two critical issues: the file handle leaks and the
division by zero. Keep all other code unchanged.
```

### Checkpoint prompt

```
Before we continue, summarize: what have we fixed, what remains,
and what order should we address the remaining issues?
```

### Branch point prompts

```
Let us explore the caching approach in depth. We will consider
the database optimization separately. For now, focus only on
caching: what are the tradeoffs and implementation details?
```

```
I am exploring options for improving query performance on a users
table with 10M rows. In a separate conversation, I am looking at
caching. In this conversation, I want to focus only on
database-level optimizations: indexes, query restructuring,
and partitioning.
```

### Reset prompt

```
We found that a slow query was caused by a missing WHERE clause
that triggered a full table scan. I want to audit three other
queries for the same pattern. Here are the queries: [paste].
For each one, check whether the WHERE clause adequately
constrains the scan.
```

### Micro-prompts table

| Micro-prompt | Sweet spot | Failure mode |
|-------------|-----------|--------------|
| Summarize progress | Drifting conversations past 5 exchanges | Short conversations where context is clear |
| Critique your answer | Code with hidden edge cases or concurrency | Domains where AI lacks knowledge to self-assess |
| Generate tests | Exploring verification for unfamiliar domains | Testing code the AI wrote (shared blind spots) |
| Harden for production | Working prototype that needs robustness | Broken logic that needs fixing, not hardening |
| Smallest safe change | Modifying working production systems | Fundamentally broken architecture needing redesign |

## Concepts Covered

- Why single-shot prompts break down on tasks with hidden complexity
- The ask-inspect-adjust loop as the core conversation rhythm
- Micro-prompts: summary checkpoint, self-critique, test generator, production hardener, minimal change
- Checkpoints every 5–10 exchanges to verify mutual understanding
- Branch points explored in separate conversations (like separate git branches)
- Summarizing and resetting long sessions — what to carry forward, what to leave behind
- Progressive disclosure and context refresh techniques
- Conversation-driven code review: review → fix critical → checkpoint → fix major → critique → test
