"""Coordinate independent workers under a fixed adapter contract.

The model produces JSON data only. The integration check never executes model
output, writes to an external system, or treats a worker's claim as proof.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import json
import os
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Assignment:
    channel: str
    retry_after_seconds: int


ASSIGNMENTS = (
    Assignment("email", 1),
    Assignment("sms", 3),
    Assignment("push", 2),
)

SYSTEM_PROMPT = (
    "You are one worker converting one notification adapter's retry delay. "
    "Return only a JSON object with exactly two fields: channel and "
    "retry_after_ms. Preserve the supplied channel and convert the integer "
    "retry_after_seconds to integer milliseconds. Do not add other fields."
)


def validate(assignment, response):
    """Return the accepted data, or a reason suitable for redispatch."""
    if response is None:
        return None, "The worker request failed or returned no content."
    if not isinstance(response, str) or len(response) > 4096:
        return None, "Return a short JSON object."

    def unique_keys(pairs):
        result = dict(pairs)
        if len(result) != len(pairs):
            raise ValueError("duplicate JSON keys")
        return result

    try:
        candidate = json.loads(response, object_pairs_hook=unique_keys)
    except (TypeError, ValueError):
        return None, "Return one JSON object."
    if not isinstance(candidate, dict) or set(candidate) != {
        "channel", "retry_after_ms"
    }:
        return None, "Use only channel and retry_after_ms."
    if candidate["channel"] != assignment.channel:
        return None, "Keep the assigned channel."
    delay = candidate["retry_after_ms"]
    expected = assignment.retry_after_seconds * 1000
    if type(delay) is not int or delay != expected:
        return None, f"retry_after_ms must be the integer {expected}."
    return candidate, None


def coordinate(ask_worker, assignments=ASSIGNMENTS):
    """Run one independent call per worker and at most one correction."""
    if not assignments:
        raise ValueError("at least one worker is required")
    if any(
        not isinstance(item, Assignment)
        or not isinstance(item.channel, str)
        or not item.channel
        or type(item.retry_after_seconds) is not int
        or item.retry_after_seconds < 0
        for item in assignments
    ):
        raise ValueError("assignments need a channel and nonnegative seconds")
    if len({item.channel for item in assignments}) != len(assignments):
        raise ValueError("worker channels must be distinct")

    # Each worker receives its own assignment, not another worker's output.
    with ThreadPoolExecutor(max_workers=len(assignments) or 1) as pool:
        futures = {
            item.channel: pool.submit(ask_worker, item, None)
            for item in assignments
        }
        responses = {}
        for item in assignments:
            try:
                responses[item.channel] = futures[item.channel].result()
            except Exception:
                responses[item.channel] = None

    accepted = {}
    rejections = {}
    for item in assignments:
        candidate, reason = validate(item, responses[item.channel])
        if reason is None:
            accepted[item.channel] = candidate
        else:
            rejections[item.channel] = reason

    # Keep accepted work and redispatch only the rejected assignment.
    unresolved = {}
    for item in assignments:
        if item.channel not in rejections:
            continue
        try:
            response = ask_worker(item, rejections[item.channel])
        except Exception:
            response = None
        candidate, reason = validate(item, response)
        if reason is None:
            accepted[item.channel] = candidate
        else:
            unresolved[item.channel] = reason

    return {
        "accepted": accepted,
        "first_rejections": rejections,
        "unresolved": unresolved,
        "complete": len(accepted) == len(assignments),
    }


def scripted_worker(assignment, feedback):
    """A deterministic demonstration; the push worker first uses seconds."""
    delay = assignment.retry_after_seconds * 1000
    if assignment.channel == "push" and feedback is None:
        delay = assignment.retry_after_seconds
    return json.dumps({
        "channel": assignment.channel,
        "retry_after_ms": delay,
    })


def make_chat_worker(api_url, api_key, model):
    """Create a worker for a chat-completions-compatible endpoint."""
    parsed = urlparse(api_url)
    local = parsed.hostname in {"localhost", "127.0.0.1", "::1"}
    if (not parsed.hostname or parsed.username or parsed.password
            or parsed.scheme not in {"http", "https"}
            or (parsed.scheme != "https" and not local)):
        raise ValueError("use HTTPS, or HTTP only for a local test server")

    def ask(assignment, feedback):
        task = {
            "channel": assignment.channel,
            "retry_after_seconds": assignment.retry_after_seconds,
        }
        if feedback is not None:
            task["integration_feedback"] = feedback
        body = json.dumps({
            "model": model,
            "max_tokens": 128,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(task)},
            ],
        }).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        request = Request(api_url, data=body, headers=headers, method="POST")
        with urlopen(request, timeout=30) as response:
            content = response.read(65537)
        if len(content) > 65536:
            raise ValueError("worker response exceeds 64 KiB")
        data = json.loads(content)
        return data["choices"][0]["message"]["content"]

    return ask


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true")
    mode.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if args.demo:
        ask_worker = scripted_worker
    else:
        api_url = os.environ.get("AI_API_URL")
        model = os.environ.get("AI_MODEL")
        if not api_url or not model:
            parser.error("--live requires AI_API_URL and AI_MODEL")
        try:
            ask_worker = make_chat_worker(
                api_url, os.environ.get("AI_API_KEY", ""), model
            )
        except ValueError as error:
            parser.error(str(error))

    report = coordinate(ask_worker)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
