# Chapter 3 — Code Listings

Conversations that converge: an iterative production-readiness review of a
starting event processor, then a single bounded, reviewable repair — a
missing-`events` validation guard — applied through inspect, red, approve,
and green.

- **`listing_3_1_event_processor_start.py`** — Listing 3.1: Starting event processor
- **`listing_3_2_missing_events_guard.diff`** — Listing 3.2: Missing-events validation guard
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listing 3.2 is the exact applied diff against `event_processor.py`
(Listing 3.1); it changes only the selected missing-key behavior.

See the [main README](../README.md) for setup instructions.
