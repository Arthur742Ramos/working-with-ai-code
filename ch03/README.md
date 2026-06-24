# Chapter 3 — Code Listings

Iterative conversation in practice: branching a rate-limiter design, then
transforming a flawed event-processor module into production-quality code
through ask-inspect-adjust, checkpointing, and micro-prompts.

- **`listing_3_1_rate_limiter_decorator.py`** — Listing 3.1: Branch A result: decorator-based rate limiter
- **`listing_3_2_rate_limit_script.py`** — Listing 3.2: Branch B result, part 1: Redis sliding-window script
- **`listing_3_3_rate_limit_middleware.py`** — Listing 3.3: Branch B result, part 2: Python wrapper and middleware
- **`listing_3_4_event_processor_start.py`** — Listing 3.4: The starting code: event processor with hidden issues
- **`listing_3_5_ai_review_response.txt`** — Listing 3.5: The production-readiness review the agent returned
- **`listing_3_6_event_processor_critical_fix.py`** — Listing 3.6: After fixing the three ship-blockers
- **`listing_3_7_timestamp_parsing.py`** — Listing 3.7: Robust timestamp parsing with an explicit UTC contract
- **`listing_3_8_validation_and_filtering.txt`** — Listing 3.8: Final version, part 1: validation and filtering
- **`listing_3_9_aggregation_and_output.txt`** — Listing 3.9: Final version, part 2: aggregation and output
- **`listing_3_10_test_cases_part1.py`** — Listing 3.10: Generated tests, part 1: harness and filtering
- **`listing_3_11_test_cases_part2.py`** — Listing 3.11: Generated tests, part 2: dedup, validation, timezones
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 3.8 and 3.9 are mid-function continuations of the final
`process_events`, so they are kept as `.txt` (they share one function body
and do not stand alone as runnable modules). Listings 3.10 and 3.11 are the
two halves of the generated `test_event_processor.py`.

See the [main README](../README.md) for setup instructions.
