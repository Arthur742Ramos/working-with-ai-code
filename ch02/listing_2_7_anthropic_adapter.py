"""Listing 2.7: Optional live-provider adapter

From "Working with AI as a Real Teammate" (Manning)
Chapter 2

Optional. The printed path runs offline through Listing 2.2. To use a live
provider instead, install `anthropic`, configure credentials through a
supported SDK credential source, and import `chat` from this module in place
of the local one. Keep `FIXED_DIFF` from Listing 2.2 until you deliberately
choose a different input boundary.
"""

from anthropic import Anthropic


MODEL = "claude-opus-4-8"


class ProviderStopError(RuntimeError):
    def __init__(self, stop_reason):
        self.stop_reason = stop_reason
        super().__init__(
            f"Provider stopped with {stop_reason}")


def chat(messages,
         system=None,
         max_tokens=1024) -> str:
    client = Anthropic()
    request = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
    }
    if system is not None:
        request["system"] = system

    message = client.messages.create(**request)
    if message.stop_reason != "end_turn":
        raise ProviderStopError(message.stop_reason)

    for block in message.content:
        if block.type == "text":
            return block.text
    raise ValueError("Model returned no text")
