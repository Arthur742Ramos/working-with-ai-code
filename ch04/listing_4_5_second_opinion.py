"""Listing 4.5 Collecting two independent code reviews from different models."""
import json
import os

from listing_4_4_call_model import call_model


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

    model_a_resp = call_model(            # First opinion from MODEL_A_* environment variables
        os.environ["MODEL_A_API_URL"],
        os.environ["MODEL_A_API_KEY"],
        os.environ["MODEL_A_NAME"],
        review_prompt
    )

    model_b_resp = call_model(            # Second opinion from MODEL_B_* environment variables
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
