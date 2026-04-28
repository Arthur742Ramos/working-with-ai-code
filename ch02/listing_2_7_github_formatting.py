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
        print("No staged changes found.")
    else:
        try:
            pr = generate_pr_description(diff)
            print(format_for_github(pr))

            with open("pr_description.json", "w") as f:   #C
                json.dump(pr, f, indent=2)
            print("\n(JSON saved to pr_description.json)")
        except ValueError as e:
            print(f"Error: {e}")
