"""Listing 2.1: Simple PR generator: no contract, no validation

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

import subprocess
from llm_client import chat


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
    prompt = (
        "Write a PR description for this diff:\n\n"
        f"{diff}"
    )

    return chat(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )


if __name__ == "__main__":
    diff = get_git_diff()
    if not diff:
        print("No staged changes found.")
    else:
        description = generate_pr_description(diff)
        print(description)
