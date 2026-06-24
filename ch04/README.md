# Chapter 4 — Code Listings

Verifying AI output: the failure modes that survive a green test suite,
the self-critique and second-opinion patterns that surface them, the
five-step verification pipeline (run it, lint it, test behavior, verify
docs, check existence), a production-incident hands-on, and a tiny eval
that freezes the cases that broke.

- **`listing_4_1_timestamp_parser.py`** — Listing 4.1: AI-generated timestamp parser: looks correct, misses edge cases
- **`listing_4_2_test_proves_nothing.py`** — Listing 4.2: A test that passes but proves nothing useful
- **`listing_4_3_test_verifies_behavior.py`** — Listing 4.3: A test that verifies behavior
- **`listing_4_4_money_handling.py`** — Listing 4.4: A flawed money-handling function for two models to review
- **`listing_4_5_smoke_test.py`** — Listing 4.5: A quick smoke test function for AI-generated code
- **`listing_4_6_property_based_testing.py`** — Listing 4.6: Property-based testing for AI-generated code
- **`listing_4_7_existence_check.py`** — Listing 4.7: Quick existence check for recommended packages
- **`listing_4_8_validation_module.py`** — Listing 4.8: AI-generated validation module to be verified
- **`listing_4_9_validator_tests.py`** — Listing 4.9: Behavior-focused tests the agent generated for the validator
- **`listing_4_10_reproduce_incident.txt`** — Listing 4.10: The agent reproduces the incident before forming a theory
- **`listing_4_11_nplus1_loop.py`** — Listing 4.11: The N+1 loop at the heart of `build_summary` (`code/ch04/incident_demo/server.py`)
- **`listing_4_12_orphaned_rows.txt`** — Listing 4.12: The orphaned rows the overnight import left behind
- **`listing_4_13_explain_query_plan.txt`** — Listing 4.13: EXPLAIN QUERY PLAN exposes a full scan per item
- **`listing_4_14_left_join_fix.diff`** — Listing 4.14: The fix: one LEFT JOIN with a None-guard (excerpt from `fix.diff`)
- **`listing_4_15_before_after_load.txt`** — Listing 4.15: Before and after, the same 300-request load at cold cache
- **`listing_4_16_tiny_eval.py`** — Listing 4.16: A tiny eval: the cases that broke, scored on every run
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 4.10, 4.12, 4.13, and 4.15 are captured terminal/tool output, so
they are kept as `.txt`. Listing 4.11 is the original buggy loop excerpted
from the incident-demo service (`code/ch04/incident_demo/server.py`), and
Listing 4.14 is the printed excerpt of `code/ch04/incident_demo/fix.diff`
(the full, applyable patch lives with the runnable demo in the book repo).
Listing 4.16 is the full runnable `tiny_eval.py`: run it to watch the
Listing 4.1 regex parser score `2/5 passed` and the spec-handling parser
score `5/5 passed`.

See the [main README](../README.md) for setup instructions.
