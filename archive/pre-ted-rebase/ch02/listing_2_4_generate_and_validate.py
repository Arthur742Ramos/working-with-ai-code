"""Listing 2.4: Generate, parse, and validate the result

From "Working with AI as a Real Teammate" (Manning)
Chapter 2

The imports mirror the printed listing: `FIXED_DIFF` and `chat` come from
Listing 2.2 (`listing_2_2_local_fixture.py`) and `SCHEMA` from Listing 2.3
(`listing_2_3_schema.py`).
"""

import json
import sys

from jsonschema import ValidationError, validate

from local_fixture import FIXED_DIFF, chat
from schema import SCHEMA

SYSTEM_PROMPT = """You are a senior software
engineer writing pull request descriptions.
Return valid JSON matching the requested
schema. Return no markdown or explanation."""


def get_git_diff() -> str:
    """Return the fixed diff for the offline run."""
    return FIXED_DIFF


def build_prompt(diff: str) -> str:
    """Build the contract-based prompt."""
    return f"""Task: produce JSON with fields
title, summary, tests, risks.

Constraints:
- Use only the provided diff
- Do not invent tests or behavior not in code
- Keep each list item under 12 words
- summary, tests, risks must each have 2+ items

Output format:
{{
    "title": "string (max 72 chars)",
    "summary": ["string", "string"],
    "tests": ["string", "string"],
    "risks": ["string", "string"]
}}

Diff:
{diff}"""


def generate_pr_description(diff: str) -> dict:
    """Generate and validate PR description."""
    response_text = chat(
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user",
             "content": build_prompt(diff)}
        ],
        max_tokens=1024
    )

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    try:
        validate(instance=data, schema=SCHEMA)
    except ValidationError as e:
        raise ValueError(
            f"Invalid schema: {e.message}")

    return data
