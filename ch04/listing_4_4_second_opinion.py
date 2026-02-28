"""Listing 4.4 Getting a second opinion from a different model."""
import json
from anthropic import Anthropic
from openai import OpenAI

def get_second_opinion(
    code: str, concern: str
) -> dict:
    """Ask two models to review code."""
    review_prompt = f"""Review this code for:
{concern}

Code:
{code}

Respond with JSON:
{{
    "issues": ["list of concerns"],
    "safe": true/false,
    "reasoning": "brief explanation"
}}"""

    claude = Anthropic()                    # First opinion from Claude
    claude_resp = claude.messages.create(
        model="claude-sonnet-4",
        max_tokens=1024,
        messages=[
            {"role": "user",
             "content": review_prompt}
        ]
    )

    gpt = OpenAI()                          # Second opinion from GPT-4o
    gpt_resp = gpt.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {"role": "user",
             "content": review_prompt}
        ]
    )

    return {
        "claude": json.loads(
            claude_resp.content[0].text
        ),
        "gpt": json.loads(
            gpt_resp.choices[0]
            .message.content
        )
        # Production code should add
        # validation here
    }
