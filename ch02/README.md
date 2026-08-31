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
- **`listing_2_7_anthropic_adapter.py`** — Listing 2.7: Optional live-provider adapter
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 2.2–2.6 build one tool incrementally, so they mirror the printed
listings rather than each standing alone: Listing 2.4 imports `FIXED_DIFF`
and `chat` from Listing 2.2 and `SCHEMA` from Listing 2.3, and Listings 2.5
and 2.6 continue that same `pr_generator.py` module, reusing `build_prompt`,
`SYSTEM_PROMPT`, `generate_pr_description`, and `get_git_diff`.

The command-line entry point in Listing 2.5 deliberately calls the
single-attempt `generate_pr_description(diff)`, so the deterministic malformed
first response produces a visible baseline failure (`Error: Invalid JSON`).
The chapter's captured session repairs that with a one-line change to
`generate_with_retry(diff)`, after which the second response validates and the
command prints the description and writes `pr_description.json`.

The deterministic `chat` in Listing 2.2 lets the example run offline with no
model provider; only `jsonschema` is required (see `requirements.txt`).

Listing 2.7 is optional and is not part of the offline path. It replaces the
deterministic `chat` from Listing 2.2 with Anthropic's official Python SDK and
rejects any stop reason other than `end_turn` before reading text, so a refusal
or a truncated reply cannot consume a JSON-validation retry. It needs a
separate install and credentials from a supported SDK credential source:

```bash
pip install anthropic
```

See the [main README](../README.md) for setup instructions.
