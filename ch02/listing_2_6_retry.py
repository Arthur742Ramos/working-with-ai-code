"""Listing 2.6: Retry logic with conversational error feedback

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

def generate_with_retry(diff: str, 
                        max_retries: int = 2
                        ) -> dict:
    """Generate PR description with retry on 
    validation failure."""
    messages = [
        {"role": "user", 
         "content": build_prompt(diff)}
    ]

    for attempt in range(max_retries + 1):
        response_text = chat(
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=1024
        )
        
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
