"""Listing 2.4: Generation function with validation

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

import json
from jsonschema import validate, ValidationError
from llm_client import chat

SYSTEM_PROMPT = """You are a senior software 
engineer writing pull request descriptions. 
You ALWAYS respond with valid JSON matching 
the requested schema. No markdown, no 
explanation, just the JSON object."""

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
            {"role": "user", "content": build_prompt(diff)}
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
        raise ValueError(f"Schema validation failed: {e.message}")

    return data
