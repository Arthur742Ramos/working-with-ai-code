# Chapter 5 — Code Listings

Diagnosing failure under uncertainty: a falsifiable hypothesis for a
repeatable order failure, a timestamp parser that passes common examples
but hides edge cases, structural versus behavioral assertions, the shipped
per-item lookup that dereferences a missing product, the exact fail-closed
policy repair, and the order and query-plan evidence for the repeated scan.

- **`listing_5_1_falsifiable_hypothesis.txt`** — Listing 5.1: A falsifiable hypothesis for a repeatable order failure
- **`listing_5_2_timestamp_parser.py`** — Listing 5.2: A timestamp parser that passes common examples
- **`listing_5_3_structural_vs_behavior.py`** — Listing 5.3: Structural assertions versus behavior assertions
- **`listing_5_4_per_item_lookup.py`** — Listing 5.4: The per-item lookup in the shipped summary path
- **`listing_5_5_missing_product_repair.diff`** — Listing 5.5: The exact missing-product policy repair
- **`listing_5_6_query_plan_evidence.txt`** — Listing 5.6: Order and query-plan evidence for the repeated scan
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 5.3 and 5.4 are excerpts of the order module under diagnosis
(`process_order`, `sample_order`, `lookup_product`, and the surrounding
loop variables are defined there), so they mirror the printed listings
rather than standing alone. Listing 5.5 is the exact applied diff against
`server.py`, and Listing 5.6 is captured SQLite session evidence.

See the [main README](../README.md) for setup instructions.
