"""Listing 2.6: Retry logic with conversational error feedback."""

import json
from jsonschema import validate, ValidationError
from anthropic import Anthropic

from listing_2_3_schema import SCHEMA
from listing_2_4_validation import SYSTEM_PROMPT, build_prompt


def generate_with_retry(diff: str,
                        max_retries: int = 2
                        ) -> dict:
    """Generate PR description with retry on validation failure."""
    client = Anthropic()
    messages = [
        {"role": "user",
         "content": build_prompt(diff)}
    ]

    for attempt in range(max_retries + 1):
        response = client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        response_text = response.content[0].text

        try:
            data = json.loads(response_text)
            validate(instance=data, schema=SCHEMA)
            return data
        except (json.JSONDecodeError,
                ValidationError) as e:
            if attempt < max_retries:
                messages.append({
                    "role": "assistant",
                    "content": response_text
                })
                messages.append({
                    "role": "user",
                    "content": f"That JSON was "
                               f"invalid: {e}. "
                               f"Fix it to match "
                               f"the schema."
                })
            else:
                raise ValueError(
                    f"Failed after "
                    f"{max_retries + 1} attempts: "
                    f"{e}"
                )
