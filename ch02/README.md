# Chapter 2: Understanding the machinery and your first AI tool

This chapter explains how large language models work (next-token prediction, context windows, temperature, hallucination) and builds a PR description generator that evolves through three iterations.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
```

## Code Listings

| File | Description |
|------|-------------|
| `listing_2_1_naive.py` | Naive PR generator: no contract, no validation |
| `listing_2_2_contract.py` | PR generator with system prompt and contract |
| `listing_2_3_schema.py` | JSON schema for PR description validation |
| `listing_2_4_validation.py` | Generation function with three-layer validation |
| `listing_2_5_complete.py` | Complete PR generator with validation and formatting |
| `listing_2_6_retry.py` | Retry logic with conversational error feedback |

## Usage

Stage some changes in a git repository, then run:

```bash
python listing_2_5_complete.py
```

The tool will generate a structured PR description from your staged diff and save it as `pr_description.json`.

## Concepts Covered

- Next-token prediction
- Context windows
- Temperature and output variation
- Hallucination as inherent risk
- Prompt engineering: when it helps, when it does not
- Risk matrix for verification calibration
- Schema validation for reliable AI output
- Retry with conversational error feedback (3C Loop in code)
