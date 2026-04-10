"""Listing 2.5: Complete PR generator with validation and formatting

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

import json
import subprocess

from jsonschema import ValidationError, validate

from llm_client import chat

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "maxLength": 72,
        },
        "summary": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
        },
        "tests": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
        },
        "risks": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
        },
    },
    "required": ["title", "summary", "tests", "risks"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """You are a senior software engineer writing pull \
request descriptions.
You ALWAYS respond with valid JSON matching the requested schema. \
No markdown, no explanation, just the JSON object."""


def get_git_diff() -> str:                         # Get staged changes from git
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


def generate_pr_description(diff: str) -> dict:    # Generate, parse, and validate in one function
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


def format_for_github(pr: dict) -> str:            # Transform JSON to GitHub-flavored markdown
    """Format the PR description for GitHub."""
    lines = [
        f"## {pr['title']}",
        "",
        *pr["summary"],
        "",
        "### Test Checklist",
        *[f"- [ ] {test}" for test in pr["tests"]],
        "",
        "### Risk Assessment",
        *[f"- {risk}" for risk in pr["risks"]],
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    diff = get_git_diff()
    if not diff:
        print("No staged changes found.")
    else:
        try:
            pr = generate_pr_description(diff)
            print(format_for_github(pr))

            with open("pr_description.json", "w") as handle:  # Save structured data for automation pipelines
                json.dump(pr, handle, indent=2)
            print("\n(JSON saved to pr_description.json)")
        except ValueError as exc:
            print(f"Error: {exc}")
