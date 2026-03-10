"""Listing 2.7: GitHub formatting and CLI entry point.

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

import json

from listing_2_6_generation import (
    generate_pr_description,
    get_git_diff,
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
        print("No staged changes found.")
    else:
        try:
            pr = generate_pr_description(diff)
            print(format_for_github(pr))

            with open("pr_description.json", "w") as handle:
                json.dump(pr, handle, indent=2)
            print("\n(JSON saved to pr_description.json)")
        except ValueError as exc:
            print(f"Error: {exc}")
