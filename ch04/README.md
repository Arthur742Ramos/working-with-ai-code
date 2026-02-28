# Chapter 4: Working with uncertainty and hallucinations

This chapter covers why AI sounds confident even when wrong, how to recognize hallucinations and subtle mistakes, a catalog of common pitfalls, self-critique and second opinion patterns, and when to stop asking the model and switch to hard automated checks.

## Setup

```bash
pip install -r requirements.txt
```

## Code Listings

| File | Description |
|------|-------------|
| `listing_4_1_timestamp_parser.py` | AI-generated ISO 8601 timestamp parser — looks correct, misses edge cases (fractional seconds, offsets without colons, lowercase separator) |
| `listing_4_2_test_proves_nothing.py` | A test that passes but proves nothing useful — assertions accept almost any return value |
| `listing_4_3_test_verifies_behavior.py` | A test that verifies behavior — checks specific status, total, and item count |
| `listing_4_4_second_opinion.py` | Getting a second opinion from two models (Claude + GPT-4o) on the same code review |
| `listing_4_5_smoke_test.py` | Quick smoke test: runs AI-generated code in an isolated subprocess with timeout |
| `listing_4_6_static_analysis.py` | Runs mypy type checking and ruff linting on AI-generated code |
| `listing_4_7_property_based_testing.py` | Property-based testing with Hypothesis — generates hundreds of random inputs |
| `listing_4_8_existence_check.py` | Quick existence check for PyPI packages recommended by AI |
| `listing_4_9_validation_module.py` | AI-generated user registration validation module (email, password, username) — the subject of the verification pipeline walkthrough |
| `listing_4_10_validation_tests.py` | Behavior-focused tests for the validation module — exposes regex limitations with international domains |

### Verification pipeline chain

Listings 4.5 → 4.6 → 4.7 → 4.8 form a reusable verification toolkit, demonstrated as a five-step pipeline against Listing 4.9:

1. **Run it** (4.5) — Smoke test catches syntax errors, missing imports, wrong signatures
2. **Lint it** (4.6) — Static analysis catches type mismatches and style issues
3. **Test behavior** (4.7) — Property-based tests catch edge cases with random inputs
4. **Check docs** — Verify API claims against official documentation for your version
5. **Verify existence** (4.8) — Confirm recommended packages actually exist on PyPI

Listing 4.10 tests Listing 4.9 and reveals that `test_international_domain` fails — the email regex only allows ASCII characters in the domain.

### Test quality contrast

Listings 4.2 and 4.3 contrast two approaches to testing the same function:

- **4.2** — Checks structure only (`is not None`, `isinstance`, `"status" in result`) — passes for almost any dict
- **4.3** — Checks behavior (specific status, exact total, correct count) — fails when the code does the wrong thing

## Key Prompts

### Self-critique prompt (Pattern 1: Devil's advocate)

```
Before I implement the solution above, play devil's advocate:
- What could go wrong with this approach?
- What assumptions are we making that might be false?
- What edge cases might break this?
- If this fails in production, what would the most likely cause be?
```

### Targeted review prompt (Pattern 2)

```
Review the code above specifically for:
1. Race conditions or concurrency issues
2. Memory leaks or resource exhaustion
3. Inputs that would cause unexpected behavior
4. Security vulnerabilities (injection, auth bypass)

For each category, either identify a specific concern or explain
why it does not apply here.
```

### Reversal test prompt (Pattern 3)

```
You recommended using Redis for caching. Now argue the case for
NOT using Redis. What are the strongest reasons to choose a
different approach?
```

### Known-answer test prompt (Pattern 5)

```
Here is a working function that I know is correct:

    def calculate_tax(price, rate):
        return round(price * rate, 2)

Your proposed refactored version should produce identical results
for these inputs:
- calculate_tax(100.00, 0.0825) → 8.25
- calculate_tax(49.99, 0.07) → 3.50
- calculate_tax(0.01, 0.10) → 0.00

Walk through each case with your version and confirm the output matches.
```

### Specificity probe prompt (Pattern 6)

```
You said to "optimize the database queries." Which specific
queries in the code I shared would you optimize, and how? Show
me the before and after for each one.
```

### Multi-model comparison prompt (Pattern 4)

See `listing_4_4_second_opinion.py` for the programmatic approach. The review prompt template:

```
Review this code for: {concern}

Code:
{code}

Respond with JSON:
{
    "issues": ["list of concerns"],
    "safe": true/false,
    "reasoning": "brief explanation"
}
```

## Red Flags Checklist

Watch for these signals that AI output deserves extra scrutiny:

- **Suspiciously perfect APIs** — When the suggested library interface is exactly what you need, it may be invented. Real libraries have quirks.
- **Specific numbers without sources** — "PostgreSQL handles ~500 concurrent connections by default" or "reduces latency by 40%" — where did that number come from?
- **Confident claims about niche topics** — Reliability drops as topics get more obscure, but confidence does not.
- **Detailed version-specific behavior** — Check the version. The AI may describe behavior from a different version than yours.
- **Configuration parameters and default values** — These change across versions and are frequently hallucinated. Always verify against actual docs.

## When to Abandon AI Output

Stop patching and start fresh when:

- **Fixing outweighs the original** — If correcting requires rewriting more than half, write it yourself with the AI's approach as inspiration.
- **Understanding is missing** — If you cannot explain *why* the code works, you cannot maintain, debug, or extend it safely.
- **Something feels off** — Engineering intuition exists for a reason. Investigate before proceeding.
- **Evaluating correctness requires expertise you lack** — Cryptographic code, financial calculations, medical algorithms — find someone qualified. "The AI said it was right" is not acceptable.

## Common Pitfalls Catalog

| # | Pitfall | Example | Catch point in 3C Loop |
|---|---------|---------|----------------------|
| 1 | Phantom dependency | `import nonexistent_lib` | Checks — run the code, imports fail immediately |
| 2 | Silent assumption | In-memory state in multi-server deploy | Contract — state deployment context upfront |
| 3 | Test that tests nothing | `assert result is not None` | Checks — "what wrong behavior still passes?" |
| 4 | Outdated pattern | `datetime.utcnow()` (deprecated 3.12) | Conversation — "is this current best practice?" |
| 5 | Plausible but wrong explanation | Correct concept, wrong application | Checks — `EXPLAIN ANALYZE`, benchmarks |
| 6 | Copy-paste context contamination | Stale code, wrong file pasted | Contract — curate the code you paste |

## Trust Escalation Ladder

| Risk Level | Example | Verification Strategy |
|-----------|---------|----------------------|
| Exploratory | Brainstorming, learning a new API | Read and assess mentally |
| Personal | Script for your own use, one-off transform | Run it, check the output |
| Team | Code in a shared repo, internal docs | Testing + code review |
| Production | User-facing features, data pipelines | Testing + review + staging + monitoring |
| Critical | Auth, payments, migrations, infrastructure | Testing + review + staging + expert audit + rollback plan |

## Concepts Covered

- The confidence-correctness gap: AI sounds the same whether recalling well-documented patterns or generating plausible guesses
- The hypothesis mindset: treat every AI response as a starting point to test, not an answer to trust
- Hallucination types: fabricated APIs, blended knowledge (mixing libraries), confident extrapolation
- Six common pitfalls with predictable patterns and catch points
- Six self-critique and second opinion patterns, from low-effort (self-critique) to high-effort (multi-model comparison)
- The five-step verification pipeline: run, lint, test behavior, check docs, verify existence
- Trust escalation: matching verification rigor to risk level
- When to abandon AI output entirely rather than patching a flawed foundation
