# Chapter 3 — Code Listings

Conversations that converge: two isolated rate-limiting branches, then a full
illustrative production-readiness review of an event processor with one
retained, bounded repair.

- **`listing_3_1_rate_limit_decorator.py`** — Listing 3.1: Branch A result, decorator-based rate limiter
- **`listing_3_2_rate_limit_redis_script.py`** — Listing 3.2: Branch B result, Redis sliding-window script
- **`listing_3_3_rate_limit_middleware.py`** — Listing 3.3: Branch B result, Python wrapper and middleware
- **`listing_3_4_event_processor_start.py`** — Listing 3.4: Starting event processor
- **`listing_3_5_missing_events_guard.diff`** — Listing 3.5: Missing-events validation guard
- **`listing_3_6_event_processor_after_blockers.py`** — Listing 3.6: After fixing the three ship-blockers
- **`listing_3_7_timestamp_parser.py`** — Listing 3.7: Robust timestamp parsing with an explicit UTC contract
- **`listing_3_8_event_processor_validation.py`** — Listing 3.8: Final version, validation and filtering
- **`listing_3_9_event_processor_aggregation.py`** — Listing 3.9: Final version, aggregation and output
- **`listing_3_10_generated_tests.py`** — Listing 3.10: Generated tests, harness and filtering
- **`listing_3_11_generated_tests_timezone.py`** — Listing 3.11: Generated tests, deduplication and timezones
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 3.1 through 3.3 are the isolated rate-limiting branch results.
Listing 3.5 is the exact applied diff against `event_processor.py`
(Listing 3.4); it changes only the selected missing-key behavior.
Listings 3.6 through 3.9 are successive source excerpts from the
illustrative review path. Listings 3.10 and 3.11 are the corresponding
generated-test excerpts.

Listing 3.6 preserves the missing-events guard accepted in Listing 3.5.
Run `python3 -m pytest -q test_review_states.py` from this directory to
check that missing input still raises the selected error while empty and
non-empty batches retain their expected summaries. The later validation
listing retains the final implementation's warning text.

See the [main README](../README.md) for setup instructions.
