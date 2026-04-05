# Working with AI as a Real Teammate — Companion Code

Code listings from the Manning book by Arthur Ramos.

## Chapters

### Chapter 1


### Chapter 2

- [`listing_2_1_naive.py`](ch02/listing_2_1_naive.py) — Listing 2.1: Naive PR generator: no contract, no validation
- [`listing_2_2_contract.py`](ch02/listing_2_2_contract.py) — Listing 2.2: PR generator with system prompt and contract
- [`listing_2_3_schema.py`](ch02/listing_2_3_schema.py) — Listing 2.3: JSON schema for PR description validation
- [`listing_2_4_validation.py`](ch02/listing_2_4_validation.py) — Listing 2.4: Generation function with validation
- [`listing_2_5_constants.py`](ch02/listing_2_5_constants.py) — Listing 2.5: PR generator constants: schema and system prompt
- [`listing_2_6_generation.py`](ch02/listing_2_6_generation.py) — Listing 2.6: Diff capture, prompt, and validated generation
- [`listing_2_7_cli.py`](ch02/listing_2_7_cli.py) — Listing 2.7: GitHub formatting and CLI entry point
- [`listing_2_8_retry.py`](ch02/listing_2_8_retry.py) — Listing 2.8: Retry logic with conversational error feedback
- [`PROMPTS.md`](ch02/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 3

- [`listing_3_1_rate_limiter_decorator.py`](ch03/listing_3_1_rate_limiter_decorator.py) — Listing 3.1: Branch A result: decorator-based rate limiter
- [`listing_3_2_rate_limit_script.py`](ch03/listing_3_2_rate_limit_script.py) — Listing 3.2: Branch B result, part 1: Redis sliding-window script
- [`listing_3_3_rate_limit_middleware.py`](ch03/listing_3_3_rate_limit_middleware.py) — Listing 3.3: Branch B result, part 2: Python wrapper and middleware
- [`listing_3_4_event_processor_start.py`](ch03/listing_3_4_event_processor_start.py) — Listing 3.4: The starting code: event processor with hidden issues
- [`listing_3_5_ai_review_response.txt`](ch03/listing_3_5_ai_review_response.txt) — Listing 3.5: Typical AI review response
- [`listing_3_6_event_processor_critical_fix.py`](ch03/listing_3_6_event_processor_critical_fix.py) — Listing 3.6: After fixing the critical issues
- [`listing_3_7_timestamp_parsing.py`](ch03/listing_3_7_timestamp_parsing.py) — Listing 3.7: Robust timestamp parsing with safe fallback
- [`listing_3_8_validation_and_filtering.txt`](ch03/listing_3_8_validation_and_filtering.txt) — Listing 3.8: Final version, part 1: validation and filtering
- [`listing_3_9_aggregation_and_output.txt`](ch03/listing_3_9_aggregation_and_output.txt) — Listing 3.9: Final version, part 2: aggregation and output
- [`listing_3_10_test_cases_part1.py`](ch03/listing_3_10_test_cases_part1.py) — Listing 3.10: Test cases, part 1
- [`listing_3_11_test_cases_part2.py`](ch03/listing_3_11_test_cases_part2.py) — Listing 3.11: Test cases, part 2
- [`PROMPTS.md`](ch03/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 4

- [`listing_4_1_timestamp_parser.py`](ch04/listing_4_1_timestamp_parser.py) — Listing 4.1 AI-generated timestamp parser — looks correct, misses edge cases.
- [`listing_4_2_test_proves_nothing.py`](ch04/listing_4_2_test_proves_nothing.py) — Listing 4.2 A test that passes but proves nothing useful.
- [`listing_4_3_test_verifies_behavior.py`](ch04/listing_4_3_test_verifies_behavior.py) — Listing 4.3 A test that verifies behavior.
- [`listing_4_4_second_opinion.py`](ch04/listing_4_4_second_opinion.py) — Listing 4.4 Getting a second opinion from a different model.
- [`listing_4_5_smoke_test.py`](ch04/listing_4_5_smoke_test.py) — Listing 4.5 A quick smoke test function for AI-generated code.
- [`listing_4_6_static_analysis.py`](ch04/listing_4_6_static_analysis.py) — Listing 4.6 Running mypy and ruff on AI-generated code.
- [`listing_4_7_property_based_testing.py`](ch04/listing_4_7_property_based_testing.py) — Listing 4.7 Property-based testing for AI-generated code.
- [`listing_4_8_existence_check.py`](ch04/listing_4_8_existence_check.py) — Listing 4.8 Quick existence check for recommended packages.
- [`listing_4_9_validation_module.py`](ch04/listing_4_9_validation_module.py) — Listing 4.9 AI-generated validation module to be verified.
- [`listing_4_10_validation_tests.py`](ch04/listing_4_10_validation_tests.py) — Listing 4.10 Behavior-focused tests for the validation module.
- [`PROMPTS.md`](ch04/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 5

- [`listing_5_1_universal_task_template.md`](ch05/listing_5_1_universal_task_template.md) — Listing 5.1: The universal task template
- [`listing_5_2_test_cases.py`](ch05/listing_5_2_test_cases.py) — Listing 5.2: Using test cases to constrain a function
- [`listing_5_3_structured_json.md`](ch05/listing_5_3_structured_json.md) — Listing 5.3: Requesting structured JSON output
- [`listing_5_4_transform_sql_to_orm.md`](ch05/listing_5_4_transform_sql_to_orm.md) — Listing 5.4: Transform pattern — SQL to ORM
- [`listing_5_5_generate_api_endpoint.md`](ch05/listing_5_5_generate_api_endpoint.md) — Listing 5.5: Generate pattern — API endpoint with full contract
- [`PROMPTS.md`](ch05/PROMPTS.md) — Prompt blocks from the current manuscript draft

## Running the Code

```bash
pip install -r ch02/requirements.txt \
    -r ch03/requirements.txt \
    -r ch04/requirements.txt
```

Chapter 5 listings are mostly prompt templates (Markdown files) rather than
runnable Python code.

Chapter 2 listings share a small provider-neutral client in
[`llm_client.py`](llm_client.py). Set these environment variables:

```bash
export AI_API_URL="https://YOUR_ENDPOINT/v1/chat/completions"
export AI_MODEL="your-model-name"
export AI_API_KEY="your-key-if-needed"
```

Chapter 4 listing 4.4 compares two models through the same generic API
shape. Set these environment variables if you want to run it:

```bash
export MODEL_A_API_URL="https://ENDPOINT_A/v1/chat/completions"
export MODEL_A_API_KEY="key-a"
export MODEL_A_NAME="model-a"
export MODEL_B_API_URL="https://ENDPOINT_B/v1/chat/completions"
export MODEL_B_API_KEY="key-b"
export MODEL_B_NAME="model-b"
```

## License

MIT
