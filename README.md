# Working with AI as a Real Teammate — Companion Code

Code listings from the Manning book by Arthur Ramos.

## Chapters

### Chapter 1


### Chapter 2

- [`listing_2_1_naive.py`](ch02/listing_2_1_naive.py) — Listing 2.1: Naive PR generator: no contract, no validation
- [`listing_2_2_contract.py`](ch02/listing_2_2_contract.py) — Listing 2.2: PR generator with system prompt and contract
- [`listing_2_3_schema.py`](ch02/listing_2_3_schema.py) — Listing 2.3: JSON schema for PR description validation
- [`listing_2_4_validation.py`](ch02/listing_2_4_validation.py) — Listing 2.4: Generation function with validation
- [`listing_2_5_complete.py`](ch02/listing_2_5_complete.py) — Listing 2.5: Complete PR generator with validation and formatting
- [`listing_2_6_retry.py`](ch02/listing_2_6_retry.py) — Listing 2.6: Retry logic with conversational error feedback

### Chapter 3

- [`listing_3_1_rate_limiter_decorator.py`](ch03/listing_3_1_rate_limiter_decorator.py) — Listing 3.1: Branch A result: decorator-based rate limiter
- [`listing_3_2_rate_limiter_redis.py`](ch03/listing_3_2_rate_limiter_redis.py) — Listing 3.2: Branch B result: Redis-backed rate limiter
- [`listing_3_3_event_processor_start.py`](ch03/listing_3_3_event_processor_start.py) — Listing 3.3: The starting code: event processor with hidden issues
- [`listing_3_5_event_processor_critical_fix.py`](ch03/listing_3_5_event_processor_critical_fix.py) — Listing 3.5: After fixing critical issues only
- [`listing_3_6_timestamp_parsing.py`](ch03/listing_3_6_timestamp_parsing.py) — Listing 3.6: Robust timestamp parsing with fallback
- [`listing_3_7_event_processor_final.py`](ch03/listing_3_7_event_processor_final.py) — Listing 3.7: Final version with all issues resolved
- [`listing_3_8_test_event_processor.py`](ch03/listing_3_8_test_event_processor.py) — Listing 3.8: Test cases verifying each fix

### Chapter 4

- [`listing_4_10_validation_tests.py`](ch04/listing_4_10_validation_tests.py) — Listing 4.10 Behavior-focused tests for the validation module.
- [`listing_4_1_timestamp_parser.py`](ch04/listing_4_1_timestamp_parser.py) — Listing 4.1 AI-generated timestamp parser — looks correct, misses edge cases.
- [`listing_4_2_test_proves_nothing.py`](ch04/listing_4_2_test_proves_nothing.py) — Listing 4.2 A test that passes but proves nothing useful.
- [`listing_4_3_test_verifies_behavior.py`](ch04/listing_4_3_test_verifies_behavior.py) — Listing 4.3 A test that verifies behavior.
- [`listing_4_4_second_opinion.py`](ch04/listing_4_4_second_opinion.py) — Listing 4.4 Getting a second opinion from a different model.
- [`listing_4_5_smoke_test.py`](ch04/listing_4_5_smoke_test.py) — Listing 4.5 A quick smoke test function for AI-generated code.
- [`listing_4_6_static_analysis.py`](ch04/listing_4_6_static_analysis.py) — Listing 4.6 Running mypy and ruff on AI-generated code.
- [`listing_4_7_property_based_testing.py`](ch04/listing_4_7_property_based_testing.py) — Listing 4.7 Property-based testing for AI-generated code.
- [`listing_4_8_existence_check.py`](ch04/listing_4_8_existence_check.py) — Listing 4.8 Quick existence check for recommended packages.
- [`listing_4_9_validation_module.py`](ch04/listing_4_9_validation_module.py) — Listing 4.9 AI-generated validation module to be verified.

## Running the Code

```bash
pip install httpx jsonschema pytest
```

The code uses a provider-neutral HTTP adapter. Set these environment variables:

```bash
export AI_API_URL="https://YOUR_ENDPOINT/v1/chat/completions"
export AI_MODEL="your-model-name"
export AI_API_KEY="your-key-if-needed"
```

## License

MIT
