"""Listing 2.5: Complete PR generator with validation and formatting."""

import subprocess
import json
from jsonschema import validate, ValidationError
from anthropic import Anthropic


SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2
        },
        "tests": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2
        },
        "risks": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2
        }
    },
    "required": ["title", "summary", "tests", "risks"],
    "additionalProperties": False
}

SYSTEM_PROMPT = """You are a senior software engineer writing pull request
descriptions. You ALWAYS respond with valid JSON matching the requested
schema. No markdown, no explanation, just the JSON object."""


def get_git_diff() -> str:
    """Get the staged git diff."""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True
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


def format_for_github(pr: dict) -> str:
    """Format the PR description for GitHub."""
    lines = [
        f"## {pr['title']}",
        "",
        *pr['summary'],
        "",
        "### Test Checklist",
        *[f"- [ ] {test}" for test in pr['tests']],
        "",
        "### Risk Assessment",
        *[f"- {risk}" for risk in pr['risks']],
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

            with open("pr_description.json", "w") as f:
                json.dump(pr, f, indent=2)
            print("\n(JSON saved to pr_description.json)")
        except ValueError as e:
            print(f"Error: {e}")
