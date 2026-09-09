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
- Propose test scenarios; do not claim they ran
- Do not invent behavior absent from the diff
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


def generate_with_retry(diff: str,
                        max_retries: int = 2
                        ) -> dict:
    """Generate PR description with retry on
    validation failure."""
    messages = [
        {"role": "user",
         "content": build_prompt(diff)}
    ]

    for attempt in range(max_retries + 1):
        response_text = chat(
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=1024
        )

        try:
            data = json.loads(response_text)
            validate(instance=data, schema=SCHEMA)
            return data
        except (json.JSONDecodeError,
                ValidationError) as e:
            detail = getattr(e, "message", str(e))
            if attempt < max_retries:
                messages.append({
                    "role": "assistant",
                    "content": response_text
                })
                messages.append({
                    "role": "user",
                    "content": f"That JSON was "
                               f"invalid: {detail}. "
                               f"Fix it to match "
                               f"the schema."
                })
            else:
                raise ValueError(
                    f"Failed after "
                    f"{max_retries + 1} attempts: "
                    f"{detail}"
                )


def format_for_github(pr: dict) -> str:
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
        print("No staged changes found.", file=sys.stderr)
    else:
        try:
            pr = generate_with_retry(diff)
            print(format_for_github(pr))

            with open("pr_description.json", "w") as f:
                json.dump(pr, f, indent=2)
            print("(JSON saved to pr_description.json)",
                  file=sys.stderr)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
