"""Listing 2.4 + 2.5 + 2.6 The complete PR description generator.

This is the finished tool the chapter builds. It assembles:

- get_git_diff()         from Listing 2.1 (staged-diff extraction)
- SCHEMA                 from Listing 2.3 (imported from schema.py)
- SYSTEM_PROMPT,
  build_prompt(),
  generate_pr_description()   from Listing 2.4 (generate + validate)
- format_for_github(),
  the CLI entry point         from Listing 2.5 (GitHub markdown + CLI)
- generate_with_retry()       from Listing 2.6 (conversational retry)

It is the 3C Loop embedded in code: the contract is the schema and
prompt, the conversation is the retry with error feedback, the checks
are JSON parsing and schema validation.

Requires ANTHROPIC_API_KEY (via the chat() adapter in llm_client.py)
and the `jsonschema` package. py_compile-clean; it needs the API key to
actually call the model.
"""

import json
import subprocess
import sys

from jsonschema import validate, ValidationError

from llm_client import chat
from schema import SCHEMA

SYSTEM_PROMPT = """You are a senior software
engineer writing pull request descriptions.
You ALWAYS respond with valid JSON matching
the requested schema. No markdown, no
explanation, just the JSON object."""              #A


def get_git_diff() -> str:
    """Get the staged git diff (from Listing 2.1)."""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True
    )
    return result.stdout


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

    try:                                            #B
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    try:
        validate(instance=data, schema=SCHEMA)      #C
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

    for attempt in range(max_retries + 1):          #A
        response_text = chat(
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=1024
        )

        try:
            data = json.loads(response_text)
            validate(instance=data, schema=SCHEMA)
            return data                             #B
        except (json.JSONDecodeError,
                ValidationError) as e:
            detail = getattr(e, "message", str(e))  #C
            if attempt < max_retries:
                messages.append({                   #D
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
                raise ValueError(                   #E
                    f"Failed after "
                    f"{max_retries + 1} attempts: "
                    f"{detail}"
                )


def format_for_github(pr: dict) -> str:                #A
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


if __name__ == "__main__":                             #B
    diff = get_git_diff()
    if not diff:
        print("No staged changes found.", file=sys.stderr)
    else:
        try:
            pr = generate_pr_description(diff)
            print(format_for_github(pr))

            with open("pr_description.json", "w") as f:   #C
                json.dump(pr, f, indent=2)
            print("(JSON saved to pr_description.json)",
                  file=sys.stderr)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
