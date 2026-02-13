"""Listing 2.1: Naive PR generator -- no contract, no validation."""

import subprocess
from anthropic import Anthropic


def get_git_diff() -> str:
    """Get the staged git diff."""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True
    )
    return result.stdout


def generate_pr_description(diff: str) -> str:
    """Generate a PR description using AI."""
    client = Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Write a PR description for "
                           f"this diff:\n\n{diff}"
            }
        ]
    )

    return message.content[0].text


if __name__ == "__main__":
    diff = get_git_diff()
    if not diff:
        print("No staged changes found.")
    else:
        description = generate_pr_description(diff)
        print(description)
