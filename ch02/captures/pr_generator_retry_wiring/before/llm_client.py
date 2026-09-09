"""Minimal `chat()` adapter used by every listing in chapter 2.

The chapter's listings call a tiny placeholder function, `chat()`,
that means "send these messages to your model and return its text
output." This module is that placeholder, wired to the Anthropic API
so the chapter's tool actually runs. In real code, `chat()` might call
a provider SDK, an internal gateway, or a local server (Ollama, LM
Studio); swapping the model is a one-function change, exactly as
section 2.7.8 describes.

Keep your model credentials in an environment variable
(`ANTHROPIC_API_KEY`), never hardcoded, because this code is meant to
run in CI where a leaked key has a wide blast radius.
"""

import os

from anthropic import Anthropic

MODEL = os.environ.get("LLM_MODEL", "claude-sonnet-4-20250514")


def chat(messages, system=None, max_tokens=1024) -> str:
    """Send messages to the model and return its text output.

    Mirrors the signature every chapter-2 listing assumes:
        chat(messages=[...], max_tokens=1024)
        chat(system=SYSTEM_PROMPT, messages=[...], max_tokens=1024)
    """
    client = Anthropic()
    kwargs = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system is not None:
        kwargs["system"] = system

    message = client.messages.create(**kwargs)
    return message.content[0].text
