# Chapter 4 — Code Listings

Spotting uncertainty and hallucinations: Surfacing hidden errors with
self-critique and second-opinion patterns.

| File | Listing | Description |
|------|---------|-------------|
| `listing_4_1_timestamp_parser.py` | 4.1 | AI-generated timestamp parser — looks correct, misses edge cases |
| `listing_4_2_test_proves_nothing.py` | 4.2 | A test that passes but proves nothing useful |
| `listing_4_3_test_verifies_behavior.py` | 4.3 | A test that verifies behavior |
| `listing_4_4_call_model.py` | 4.4 | A reusable helper for querying any chat-completions API |
| `listing_4_5_second_opinion.py` | 4.5 | Collecting two independent code reviews from different models |
| `listing_4_6_smoke_test.py` | 4.6 | A quick smoke test function for AI-generated code |
| `listing_4_7_static_analysis.py` | 4.7 | Running mypy and ruff on AI-generated code |
| `listing_4_8_property_based_testing.py` | 4.8 | Property-based testing for AI-generated code |
| `listing_4_9_existence_check.py` | 4.9 | Quick existence check for recommended packages |
| `listing_4_10_validation_module.py` | 4.10 | AI-generated validation: data model, email, and password checks |
| `listing_4_11_validation_module_part2.py` | 4.11 | AI-generated validation: username check and combined registration validator |
| `listing_4_12_validation_tests.py` | 4.12 | Behavior-focused tests for the validation module |
| `PROMPTS.md` | — | Prompt blocks from the current manuscript draft |

Listing 4.5 uses provider-neutral environment variables for two
chat-completions-compatible endpoints:

- `MODEL_A_API_URL`, `MODEL_A_API_KEY`, `MODEL_A_NAME`
- `MODEL_B_API_URL`, `MODEL_B_API_KEY`, `MODEL_B_NAME`

See the [main README](../README.md) for setup instructions.
