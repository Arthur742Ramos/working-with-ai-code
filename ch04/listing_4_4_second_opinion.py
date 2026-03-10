"""Listing 4.4 Getting a second opinion from a different model."""
import json
import os

import httpx

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

    def call_model(
        api_url: str,
        api_key: str,
        model: str,
        prompt: str
    ) -> str:
        """Send a prompt to any
        chat-completions-compatible API."""
        resp = httpx.post(
            api_url,
            headers={
                "Authorization":
                    f"Bearer {api_key}"
            },
            json={
                "model": model,
                "max_tokens": 1024,
                "messages": [
                    {"role": "user",
                     "content": prompt}
                ]
            },
            timeout=30.0
        )
        resp.raise_for_status()
        return (
            resp.json()["choices"][0]
            ["message"]["content"]
        )

    model_a_resp = call_model(
        os.environ["MODEL_A_API_URL"],
        os.environ["MODEL_A_API_KEY"],
        os.environ["MODEL_A_NAME"],
        review_prompt
    )

    model_b_resp = call_model(
        os.environ["MODEL_B_API_URL"],
        os.environ["MODEL_B_API_KEY"],
        os.environ["MODEL_B_NAME"],
        review_prompt
    )

    return {
        "model_a": json.loads(model_a_resp),
        "model_b": json.loads(model_b_resp)
        # Production code should add
        # validation here
    }
