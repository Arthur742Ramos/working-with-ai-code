# Chapter 4 — Code Listings

- **`listing_4_10_validation_tests.py`** — Listing 4.10 Behavior-focused tests for the validation module.
- **`listing_4_1_timestamp_parser.py`** — Listing 4.1 AI-generated timestamp parser — looks correct, misses edge cases.
- **`listing_4_2_test_proves_nothing.py`** — Listing 4.2 A test that passes but proves nothing useful.
- **`listing_4_3_test_verifies_behavior.py`** — Listing 4.3 A test that verifies behavior.
- **`listing_4_4_second_opinion.py`** — Listing 4.4 Getting a second opinion from a different model.
- **`listing_4_5_smoke_test.py`** — Listing 4.5 A quick smoke test function for AI-generated code.
- **`listing_4_6_static_analysis.py`** — Listing 4.6 Running mypy and ruff on AI-generated code.
- **`listing_4_7_property_based_testing.py`** — Listing 4.7 Property-based testing for AI-generated code.
- **`listing_4_8_existence_check.py`** — Listing 4.8 Quick existence check for recommended packages.
- **`listing_4_9_validation_module.py`** — Listing 4.9 AI-generated validation module to be verified.
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listing 4.4 uses provider-neutral environment variables for two
chat-completions-compatible endpoints:

- `MODEL_A_API_URL`, `MODEL_A_API_KEY`, `MODEL_A_NAME`
- `MODEL_B_API_URL`, `MODEL_B_API_KEY`, `MODEL_B_NAME`

See the [main README](../README.md) for setup instructions.
