"""Listing 2.2: PR generator with system prompt and contract."""

from anthropic import Anthropic


SYSTEM_PROMPT = """You are a senior software engineer writing pull request
descriptions. Your descriptions are thorough, specific, and help reviewers
understand exactly what changed and why. You always assess risks honestly."""


def generate_pr_description(diff: str) -> str:
    """Generate a structured PR description."""
    client = Anthropic()

    prompt = f"""Analyze the following git diff and produce a PR description
with these exact sections:

TITLE: A concise title (max 72 characters)

SUMMARY: 2-3 sentences explaining what and why

CHANGES:
- Bullet list of specific changes made

TEST CHECKLIST:
- Specific scenarios a reviewer should verify
- Include both happy path and edge cases

RISK ASSESSMENT:
- What could go wrong with this change?
- What areas might be affected?
- Suggested mitigation or monitoring

---
GIT DIFF:
{diff}
"""

    message = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text
