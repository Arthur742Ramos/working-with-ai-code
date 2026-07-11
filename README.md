# Working with AI as a Real Teammate — Companion Code

Code listings from the Manning book by Arthur Ramos.

Each chapter directory mirrors that chapter's printed listings as
standalone, reader-facing files, alongside a `README.md` index, a
`PROMPTS.md` of the chapter's prompt blocks, and (where the code uses
third-party packages) a `requirements.txt`. Code is provider-neutral:
the listings import the shared [`llm_client.py`](llm_client.py) helper
rather than any vendor SDK.

## Chapters

### Chapter 1

Chapter 1 has no numbered code listings. See
[`ch01/PROMPTS.md`](ch01/PROMPTS.md) for the chapter's prompt and response
examples, and [`ch01/README.md`](ch01/README.md) for the index.

### Chapter 2

- [`listing_2_1_simple.py`](ch02/listing_2_1_simple.py) — Listing 2.1: Simple PR generator: no contract, no validation
- [`listing_2_2_contract.py`](ch02/listing_2_2_contract.py) — Listing 2.2: PR generator with system prompt and contract
- [`listing_2_3_schema.py`](ch02/listing_2_3_schema.py) — Listing 2.3: JSON schema for PR description validation
- [`listing_2_4_validation.py`](ch02/listing_2_4_validation.py) — Listing 2.4: Generation function with validation
- [`listing_2_5_github_formatting.py`](ch02/listing_2_5_github_formatting.py) — Listing 2.5: GitHub formatting and CLI entry point
- [`listing_2_6_retry.py`](ch02/listing_2_6_retry.py) — Listing 2.6: Retry logic with conversational error feedback
- [`listing_2_7_github_actions_ci.yml`](ch02/listing_2_7_github_actions_ci.yml) — Listing 2.7: GitHub Actions job that runs the generator in CI
- [`PROMPTS.md`](ch02/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 3

- [`listing_3_1_rate_limiter_decorator.py`](ch03/listing_3_1_rate_limiter_decorator.py) — Listing 3.1: Branch A result: decorator-based rate limiter
- [`listing_3_2_rate_limit_script.py`](ch03/listing_3_2_rate_limit_script.py) — Listing 3.2: Branch B result, part 1: Redis sliding-window script
- [`listing_3_3_rate_limit_middleware.py`](ch03/listing_3_3_rate_limit_middleware.py) — Listing 3.3: Branch B result, part 2: Python wrapper and middleware
- [`listing_3_4_event_processor_start.py`](ch03/listing_3_4_event_processor_start.py) — Listing 3.4: The starting code: event processor with hidden issues
- [`listing_3_5_ai_review_response.txt`](ch03/listing_3_5_ai_review_response.txt) — Listing 3.5: The production-readiness review the agent returned
- [`listing_3_6_event_processor_critical_fix.py`](ch03/listing_3_6_event_processor_critical_fix.py) — Listing 3.6: After fixing the three ship-blockers
- [`listing_3_7_timestamp_parsing.py`](ch03/listing_3_7_timestamp_parsing.py) — Listing 3.7: Robust timestamp parsing with an explicit UTC contract
- [`listing_3_8_validation_and_filtering.txt`](ch03/listing_3_8_validation_and_filtering.txt) — Listing 3.8: Final version, part 1: validation and filtering
- [`listing_3_9_aggregation_and_output.txt`](ch03/listing_3_9_aggregation_and_output.txt) — Listing 3.9: Final version, part 2: aggregation and output
- [`listing_3_10_test_cases_part1.py`](ch03/listing_3_10_test_cases_part1.py) — Listing 3.10: Generated tests, part 1: harness and filtering
- [`listing_3_11_test_cases_part2.py`](ch03/listing_3_11_test_cases_part2.py) — Listing 3.11: Generated tests, part 2: dedup, validation, timezones
- [`PROMPTS.md`](ch03/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 4

- [`listing_4_1_timestamp_parser.py`](ch04/listing_4_1_timestamp_parser.py) — Listing 4.1: AI-generated timestamp parser: looks correct, misses edge cases
- [`listing_4_2_test_proves_nothing.py`](ch04/listing_4_2_test_proves_nothing.py) — Listing 4.2: A test that passes but proves nothing useful
- [`listing_4_3_test_verifies_behavior.py`](ch04/listing_4_3_test_verifies_behavior.py) — Listing 4.3: A test that verifies behavior
- [`listing_4_4_money_handling.py`](ch04/listing_4_4_money_handling.py) — Listing 4.4: A flawed money-handling function for two models to review
- [`listing_4_5_smoke_test.py`](ch04/listing_4_5_smoke_test.py) — Listing 4.5: A quick smoke test function for AI-generated code
- [`listing_4_6_property_based_testing.py`](ch04/listing_4_6_property_based_testing.py) — Listing 4.6: Property-based testing for AI-generated code
- [`listing_4_7_existence_check.py`](ch04/listing_4_7_existence_check.py) — Listing 4.7: Quick existence check for recommended packages
- [`listing_4_8_validation_module.py`](ch04/listing_4_8_validation_module.py) — Listing 4.8: AI-generated validation module to be verified
- [`listing_4_9_validator_tests.py`](ch04/listing_4_9_validator_tests.py) — Listing 4.9: Behavior-focused tests the agent generated for the validator
- [`listing_4_10_reproduce_incident.txt`](ch04/listing_4_10_reproduce_incident.txt) — Listing 4.10: The agent reproduces the incident before forming a theory
- [`listing_4_11_nplus1_loop.py`](ch04/listing_4_11_nplus1_loop.py) — Listing 4.11: The N+1 loop at the heart of `build_summary`
- [`listing_4_12_orphaned_rows.txt`](ch04/listing_4_12_orphaned_rows.txt) — Listing 4.12: The orphaned rows the overnight import left behind
- [`listing_4_13_explain_query_plan.txt`](ch04/listing_4_13_explain_query_plan.txt) — Listing 4.13: EXPLAIN QUERY PLAN exposes a full scan per item
- [`listing_4_14_left_join_fix.diff`](ch04/listing_4_14_left_join_fix.diff) — Listing 4.14: The fix: one LEFT JOIN with a None-guard (excerpt from `fix.diff`)
- [`listing_4_15_before_after_load.txt`](ch04/listing_4_15_before_after_load.txt) — Listing 4.15: Before and after, the same 300-request load at cold cache
- [`listing_4_16_tiny_eval.py`](ch04/listing_4_16_tiny_eval.py) — Listing 4.16: A tiny eval: the cases that broke, scored on every run
- [`PROMPTS.md`](ch04/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 5

- [`listing_5_1_universal_task_template.md`](ch05/listing_5_1_universal_task_template.md) — Listing 5.1: The universal task template
- [`listing_5_2_test_cases.py`](ch05/listing_5_2_test_cases.py) — Listing 5.2: Using test cases to constrain a function
- [`listing_5_3_structured_json.md`](ch05/listing_5_3_structured_json.md) — Listing 5.3: Requesting structured JSON output
- [`listing_5_4_transform_sql_to_orm.md`](ch05/listing_5_4_transform_sql_to_orm.md) — Listing 5.4: Transform category: SQL to ORM
- [`listing_5_5_generate_api_endpoint.md`](ch05/listing_5_5_generate_api_endpoint.md) — Listing 5.5: Generate category: API endpoint with full contract
- [`listing_5_6_legacy_schema.sql`](ch05/listing_5_6_legacy_schema.sql) — Listing 5.6: Legacy source schema (`legacy_users`)
- [`listing_5_7_target_schema.sql`](ch05/listing_5_7_target_schema.sql) — Listing 5.7: Target schema (`accounts` and audit)
- [`PROMPTS.md`](ch05/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 6

- [`importer.py`](ch06/importer.py) — Listings 6.1–6.3: Parsing rows and deriving a stable idempotency key; Building requests and retrying transient failures; Running a dry import
- [`test_importer.py`](ch06/test_importer.py) — The chapter 6 pytest suite: one test per slice's inspection question
- [`PROMPTS.md`](ch06/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 7

- [`validator.py`](ch07/validator.py) — Listing 7.1: The coder's validator implementation
- [`test_validator.py`](ch07/test_validator.py) — Listings 7.2 and 7.3: Adversarial tests for the validator (core cases and boundary cases)
- [`cli.py`](ch07/cli.py) — Listing 7.4: A thin CLI runner for the validator
- [`listing_7_5_tool_use_loop.py`](ch07/listing_7_5_tool_use_loop.py) — Listing 7.5: A minimal tool-use loop
- [`PROMPTS.md`](ch07/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 8

- [`allocation.py`](ch08/allocation.py) — Listing 8.1: Proportional money allocation; floors each share, then hands the leftover cents to the largest fractional parts so the shares sum to exactly `total`
- [`sanity.py`](ch08/sanity.py) — Listing 8.2: Cheap, implementation-independent checks (`conserves` and `is_fair`)
- [`test_allocation.py`](ch08/test_allocation.py) — Listing 8.3: Adversarial tests, one per category the tester and red-team prompts named
- [`test_golden.py`](ch08/test_golden.py) — Listing 8.4: A frozen golden set, evaluation made executable
- [`PROMPTS.md`](ch08/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 9

- [`AGENTS.md`](ch09/AGENTS.md) - Repository-level instructions that define the approved outbound HTTP boundary
- [`alerts.py`](ch09/alerts.py) - The house-correct alert feature that uses `http_client.call`
- [`http_client.py`](ch09/http_client.py) - The injectable, fail-closed house HTTP client with auth and bounded retries
- [`test_alerts.py`](ch09/test_alerts.py) - Behavior checks for routing, auth, and failure responses
- [`test_house_rules.py`](ch09/test_house_rules.py) - Executable AST guard against direct HTTP transports
- [`test_http_client.py`](ch09/test_http_client.py) - Credential, retry, and no-network checks
- [`fixtures/direct_requests/alerts.py`](ch09/fixtures/direct_requests/alerts.py) - Deterministic red-state fixture for the coding-agent session
- [`PROMPTS.md`](ch09/PROMPTS.md) - The context-aware coding-agent prompt

Chapters 6, 7, 8, and 9 are runnable projects with passing pytest suites:
`cd ch06 && python3 -m pytest -q` prints `6 passed`,
`cd ch07 && python3 -m pytest -q` prints `8 passed`, and
`cd ch08 && python3 -m pytest -q` and
`cd ch09 && python3 -m pytest -q` each print `9 passed`. Chapter 9's
deterministic red-to-green commands are documented in
[`ch09/README.md`](ch09/README.md).

## Running the Code

```bash
pip install -r ch02/requirements.txt \
    -r ch03/requirements.txt \
    -r ch04/requirements.txt \
    -r ch06/requirements.txt \
    -r ch07/requirements.txt \
    -r ch08/requirements.txt \
    -r ch09/requirements.txt
```

Chapter 1 has no listings. Chapter 5 listings are mostly prompt templates
(Markdown files) and SQL schemas rather than runnable Python code, so that
chapter has no `requirements.txt`.

Chapters 6, 7, 8, and 9 are self-contained, runnable projects. Each needs
only `pytest`; from the chapter directory, run `python3 -m pytest -q`
(`6 passed` for ch06, `8 passed` for ch07, and `9 passed` for both ch08 and
ch09; see the chapter 9 README for its red-to-green exercise).

Chapter 2 listings share a small provider-neutral client in
[`llm_client.py`](llm_client.py). Set these environment variables:

```bash
export AI_API_URL="https://YOUR_ENDPOINT/v1/chat/completions"
export AI_MODEL="your-model-name"
export AI_API_KEY="your-key-if-needed"
```

## License

MIT
