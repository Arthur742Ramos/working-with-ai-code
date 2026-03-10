"""Minimal provider-neutral chat helper for the book listings."""
import os
from typing import Any

import httpx


def chat(
    messages: list[dict[str, str]],
    max_tokens: int = 1024,
    system: str | None = None,
    model: str | None = None,
    api_url: str | None = None,
    api_key: str | None = None,
) -> str:
    """Call a chat-completions-compatible API."""
    api_url = api_url or os.environ["AI_API_URL"]
    api_key = api_key or os.environ.get("AI_API_KEY", "")
    model = model or os.environ["AI_MODEL"]

    payload_messages = messages
    if system:
        payload_messages = [
            {"role": "system", "content": system},
            *messages,
        ]

    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = httpx.post(
        api_url,
        headers=headers,
        json={
            "model": model,
            "max_tokens": max_tokens,
            "messages": payload_messages,
        },
        timeout=30.0,
    )
    response.raise_for_status()
    body: dict[str, Any] = response.json()
    return body["choices"][0]["message"]["content"]
