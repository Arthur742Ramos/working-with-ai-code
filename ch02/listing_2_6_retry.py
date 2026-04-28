def get_git_diff() -> str:                             #A
    """Get the staged git diff."""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True
    )
    return result.stdout


def build_prompt(diff: str) -> str:                    #B
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


def generate_pr_description(diff: str) -> dict:        #C
    """Generate and validate PR description."""
    response_text = chat(
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_prompt(diff)}
        ],
        max_tokens=1024
    )

    try:                                               #D
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    try:                                               #E
        validate(instance=data, schema=SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Schema validation failed: {e.message}")

    return data
