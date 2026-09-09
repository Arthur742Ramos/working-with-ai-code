# Chapter 1 — Code Listings

Working with AI as engineering, not magic: a single worked repair on a
Flask rate limiter. You inspect the code, reproduce a focused red (the
in-memory fallback transition never reaches the application logger), apply
the accepted one-line repair, then show focused and broader green evidence.

- **`listing_1_1_rate_limiter_before.py`** — Listing 1.1: The rate limiter before the observability repair
- **`listing_1_2_focused_red.txt`** — Listing 1.2: Genuine focused red for the missing signal
- **`listing_1_3_accepted_repair.diff`** — Listing 1.3: The accepted one-line repair
- **`listing_1_4_green_evidence.txt`** — Listing 1.4: Focused and broader green evidence
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listing 1.1 is an excerpt of the application under repair. Listings 1.2 and
1.4 are captured test output, and Listing 1.3 is the printed one-line diff
fragment, so they mirror the printed listings rather than standing alone as
runnable modules.

See the [main README](../README.md) for setup instructions.
