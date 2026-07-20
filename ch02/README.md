# Chapter 2 — Code Listings

Contracts that produce checkable work: a PR description generator built to
a compact contract, validated against a JSON Schema, exercised with a
deterministic offline fixture, and finished with a bounded conversational
retry after a validation failure.

- **`listing_2_1_contract_template.txt`** — Listing 2.1: A compact contract for checkable work
- **`listing_2_2_local_fixture.py`** — Listing 2.2: A fixed diff and deterministic local response
- **`listing_2_3_schema.py`** — Listing 2.3: JSON Schema for a PR description
- **`listing_2_4_generate_and_validate.py`** — Listing 2.4: Generate, parse, and validate the result
- **`listing_2_5_github_formatting.py`** — Listing 2.5: GitHub formatting and CLI entry point
- **`listing_2_6_retry.py`** — Listing 2.6: Conversational retry after validation failure
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 2.2–2.6 build one tool incrementally, so they mirror the printed
listings rather than each standing alone: Listing 2.4 imports `FIXED_DIFF`
and `chat` from Listing 2.2 and `SCHEMA` from Listing 2.3, and Listings 2.5
and 2.6 continue that same `pr_generator.py` module, reusing `build_prompt`,
`SYSTEM_PROMPT`, `generate_pr_description`, and `get_git_diff`.

The deterministic `chat` in Listing 2.2 lets the example run offline with no
model provider; only `jsonschema` is required (see `requirements.txt`).

See the [main README](../README.md) for setup instructions.
