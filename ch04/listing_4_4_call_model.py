"""Listing 4.4 A reusable helper for querying any chat-completions API."""
import httpx


def call_model(
    api_url: str,
    api_key: str,
    model: str,
    prompt: str
) -> str:
    """Send a prompt to any
    chat-completions-compatible API."""
    resp = httpx.post(                    # Sends an HTTP POST to the chat-completions endpoint
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
