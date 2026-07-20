"""Listing 2.5: GitHub formatting and CLI entry point

From "Working with AI as a Real Teammate" (Manning)
Chapter 2

Continues the module from Listing 2.4, reusing `get_git_diff`,
`generate_pr_description`, `json`, and `sys`.
"""

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
            pr = generate_pr_description(diff)
            print(format_for_github(pr))

            with open("pr_description.json", "w") as f:
                json.dump(pr, f, indent=2)
            print("(JSON saved to pr_description.json)",
                  file=sys.stderr)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
