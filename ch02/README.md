# Chapter 2 — Code Listings

Building your first AI-powered tool: a PR description generator that
evolves from a simple prompt to structured, validated output, then drops
into CI.

- **`listing_2_1_simple.py`** — Listing 2.1: Simple PR generator: no contract, no validation
- **`listing_2_2_contract.py`** — Listing 2.2: PR generator with system prompt and contract
- **`listing_2_3_schema.py`** — Listing 2.3: JSON schema for PR description validation
- **`listing_2_4_validation.py`** — Listing 2.4: Generation function with validation
- **`listing_2_5_github_formatting.py`** — Listing 2.5: GitHub formatting and CLI entry point
- **`listing_2_6_retry.py`** — Listing 2.6: Retry logic with conversational error feedback
- **`listing_2_7_github_actions_ci.yml`** — Listing 2.7: GitHub Actions job that runs the generator in CI
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Listings 2.1–2.6 build one tool incrementally: 2.5 reuses `get_git_diff`
from 2.1, `SCHEMA` from 2.3, and `SYSTEM_PROMPT` / `build_prompt` /
`generate_pr_description` from 2.4, so they mirror the printed listings
rather than each standing alone.

These listings use the shared [`llm_client.py`](../llm_client.py)
helper in the repository root.

See the [main README](../README.md) for setup instructions.
