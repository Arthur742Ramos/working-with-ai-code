"""Listing 2.6: Diff capture, prompt, and validated generation.

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

import json
import subprocess

from jsonschema import ValidationError, validate

from llm_client import chat
from listing_2_5_constants import SCHEMA, SYSTEM_PROMPT


def get_git_diff() -> str:
    """Get the staged git diff."""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def build_prompt(diff: str) -> str:
    """Build the contract-based prompt."""
    return f"""Task: produce JSON with fields title, summary, tests, risks.

Constraints:
- Use only the provided diff
- Do not invent tests not evident in code
- Keep each list item under 12 words
- summary, tests, risks: 2+ items each

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
            {"role": "user", "content": build_prompt(diff)},
        ],
        max_tokens=1024,
    )

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    try:
        validate(instance=data, schema=SCHEMA)
    except ValidationError as exc:
        raise ValueError(
            f"Schema validation failed: {exc.message}"
        ) from exc

    return data
