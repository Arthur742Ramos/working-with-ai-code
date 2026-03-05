# Working with AI as a Real Teammate — Companion Code

Code listings from the Manning book by Arthur Ramos.

## Chapters

### Chapter 1


### Chapter 2

- [`listing_2_1_naive.py`](ch02/listing_2_1_naive.py)
- [`listing_2_1_naive_pr_generator_no_contract_no_valida.py`](ch02/listing_2_1_naive_pr_generator_no_contract_no_valida.py)
- [`listing_2_2_contract.py`](ch02/listing_2_2_contract.py)
- [`listing_2_2_pr_generator_with_system_prompt_and_cont.py`](ch02/listing_2_2_pr_generator_with_system_prompt_and_cont.py)
- [`listing_2_3_json_schema_for_pr_description_validatio.py`](ch02/listing_2_3_json_schema_for_pr_description_validatio.py)
- [`listing_2_3_schema.py`](ch02/listing_2_3_schema.py)
- [`listing_2_4_generation_function_with_validation.py`](ch02/listing_2_4_generation_function_with_validation.py)
- [`listing_2_4_validation.py`](ch02/listing_2_4_validation.py)
- [`listing_2_5_complete.py`](ch02/listing_2_5_complete.py)
- [`listing_2_5_complete_pr_generator_with_validation_an.py`](ch02/listing_2_5_complete_pr_generator_with_validation_an.py)
- [`listing_2_6_retry.py`](ch02/listing_2_6_retry.py)
- [`listing_2_6_retry_logic_with_conversational_error_fe.py`](ch02/listing_2_6_retry_logic_with_conversational_error_fe.py)

### Chapter 3

- [`listing_3_1_branch_a_result_decorator_based_rate_lim.py`](ch03/listing_3_1_branch_a_result_decorator_based_rate_lim.py)
- [`listing_3_1_rate_limiter_decorator.py`](ch03/listing_3_1_rate_limiter_decorator.py)
- [`listing_3_2_branch_b_result_redis_backed_rate_limite.py`](ch03/listing_3_2_branch_b_result_redis_backed_rate_limite.py)
- [`listing_3_2_rate_limiter_redis.py`](ch03/listing_3_2_rate_limiter_redis.py)
- [`listing_3_3_event_processor_start.py`](ch03/listing_3_3_event_processor_start.py)
- [`listing_3_3_the_starting_code_event_processor_with_h.py`](ch03/listing_3_3_the_starting_code_event_processor_with_h.py)
- [`listing_3_5_after_fixing_critical_issues_only.py`](ch03/listing_3_5_after_fixing_critical_issues_only.py)
- [`listing_3_5_event_processor_critical_fix.py`](ch03/listing_3_5_event_processor_critical_fix.py)
- [`listing_3_6_robust_timestamp_parsing_with_fallback.py`](ch03/listing_3_6_robust_timestamp_parsing_with_fallback.py)
- [`listing_3_6_timestamp_parsing.py`](ch03/listing_3_6_timestamp_parsing.py)
- [`listing_3_7_event_processor_final.py`](ch03/listing_3_7_event_processor_final.py)
- [`listing_3_7_final_version_with_all_issues_resolved.py`](ch03/listing_3_7_final_version_with_all_issues_resolved.py)
- [`listing_3_8_test_cases_verifying_each_fix.py`](ch03/listing_3_8_test_cases_verifying_each_fix.py)
- [`listing_3_8_test_event_processor.py`](ch03/listing_3_8_test_event_processor.py)

### Chapter 4

- [`listing_4_10_validation_tests.py`](ch04/listing_4_10_validation_tests.py)
- [`listing_4_1_timestamp_parser.py`](ch04/listing_4_1_timestamp_parser.py)
- [`listing_4_2_test_proves_nothing.py`](ch04/listing_4_2_test_proves_nothing.py)
- [`listing_4_3_test_verifies_behavior.py`](ch04/listing_4_3_test_verifies_behavior.py)
- [`listing_4_4_second_opinion.py`](ch04/listing_4_4_second_opinion.py)
- [`listing_4_5_smoke_test.py`](ch04/listing_4_5_smoke_test.py)
- [`listing_4_6_static_analysis.py`](ch04/listing_4_6_static_analysis.py)
- [`listing_4_7_property_based_testing.py`](ch04/listing_4_7_property_based_testing.py)
- [`listing_4_8_existence_check.py`](ch04/listing_4_8_existence_check.py)
- [`listing_4_9_validation_module.py`](ch04/listing_4_9_validation_module.py)

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
