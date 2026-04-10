"""Listing 2.6: Retry logic with conversational error feedback

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

import json

from jsonschema import ValidationError, validate

from llm_client import chat
from listing_2_5_complete_pr_generator import (
    SCHEMA,
    SYSTEM_PROMPT,
    build_prompt,
)


def generate_with_retry(
    diff: str,
    max_retries: int = 2,
) -> dict:
    """Generate PR description with retry on validation failure."""
    messages = [
        {"role": "user", "content": build_prompt(diff)},
    ]

    for attempt in range(max_retries + 1):          # Allow up to max_retries additional attempts
        response_text = chat(
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=1024,
        )

        try:
            data = json.loads(response_text)
            validate(instance=data, schema=SCHEMA)
            return data                             # Success: return validated data immediately
        except (json.JSONDecodeError, ValidationError) as exc:
            if attempt < max_retries:
                messages.append(                    # Add failed response and error to conversation context
                    {
                        "role": "assistant",
                        "content": response_text,
                    }
                )
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"That JSON was invalid: {exc}. "
                            "Fix it to match the schema."
                        ),
                    }
                )
            else:
                raise ValueError(                   # Give up after exhausting retries
                    f"Failed after {max_retries + 1} attempts: {exc}"
                ) from exc
