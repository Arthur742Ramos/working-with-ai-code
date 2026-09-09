import os

from anthropic import Anthropic


MODEL_ENV = "ANTHROPIC_MODEL"


class ProviderStopError(RuntimeError):
    def __init__(self, stop_reason):
        self.stop_reason = stop_reason
        super().__init__(
            f"Provider stopped with {stop_reason}")


def chat(messages,
         system=None,
         max_tokens=1024) -> str:
    model = os.environ.get(MODEL_ENV)
    if not model:
        raise RuntimeError(
            f"Set {MODEL_ENV} to a supported model"
        )

    client = Anthropic()
    request = {
        "model": model,
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
