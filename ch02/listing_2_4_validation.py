"""Listing 2.4: Generation function with three-layer validation."""

import json
from jsonschema import validate, ValidationError
from anthropic import Anthropic

from listing_2_3_schema import SCHEMA


SYSTEM_PROMPT = """You are a senior software engineer writing pull request
descriptions. You ALWAYS respond with valid JSON matching the requested
schema. No markdown, no explanation, just the JSON object."""


def build_prompt(diff: str) -> str:
    """Build the contract-based prompt."""
    return f"""Task: produce JSON with fields title, summary, tests, risks.

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
    client = Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user",
             "content": build_prompt(diff)}
        ]
    )

    response_text = message.content[0].text

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    validate(instance=data, schema=SCHEMA)

    if len(data["title"]) > 72:
        data["title"] = data["title"][:69] + "..."

    return data
