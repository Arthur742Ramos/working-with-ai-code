"""Coordinate workers and integrate their adapters under a fixed contract.

Workers return JSON data only. The host generates the Python adapters from
validated values in a temporary workspace; it never executes model-written code.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
from tempfile import TemporaryDirectory
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

MAX_WORKERS = 3
MAX_DELAY_MS = 2_147_483_647

SYSTEM_PROMPT = (
    "You are one worker converting one notification adapter's retry delay. "
    "Return only a JSON object with exactly two fields: channel and "
    "retry_after_ms. Preserve the supplied channel and convert the integer "
    "retry_after_seconds to integer milliseconds. Do not add other fields."
)


def parse_candidate(assignment, response):
    """Accept data with the right shape without assuming its units are right."""
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
    if type(delay) is not int or not 0 <= delay <= MAX_DELAY_MS:
        return None, "retry_after_ms must be a nonnegative integer."
    return candidate, None


def validate(assignment, response):
    """Check a worker's data against the shared integration contract."""
    candidate, reason = parse_candidate(assignment, response)
    if reason:
        return None, reason
    expected = assignment.retry_after_seconds * 1000
    if candidate["retry_after_ms"] != expected:
        return None, f"retry_after_ms must be the integer {expected}."
    return candidate, None


def write_adapter(workspace, candidate):
    """Render a scoped adapter from data; no worker-supplied code is used."""
    if not isinstance(candidate, dict):
        raise ValueError("adapter values must be validated data")
    channel = candidate.get("channel")
    delay = candidate.get("retry_after_ms")
    if (set(candidate) != {"channel", "retry_after_ms"}
            or not isinstance(channel, str)
            or re.fullmatch(r"[a-z][a-z0-9_]{0,30}", channel) is None
            or type(delay) is not int or not 0 <= delay <= MAX_DELAY_MS):
        raise ValueError("adapter values must be validated data")
    path = workspace / f"{channel}.py"
    source = (
        '"""Adapter generated from a validated worker handoff."""\n\n'
        "def retry_settings():\n"
        "    return {\n"
        f'        "channel": {channel!r},\n'
        f'        "retry_after_ms": {delay},\n'
        "    }\n"
    )
    path.write_text(source, encoding="utf-8")
    return path


def local_check(path, assignment):
    """Execute the host-generated adapter and check its local interface."""
    try:
        result = runpy.run_path(str(path))["retry_settings"]()
        response = json.dumps(result)
    except Exception as error:
        return None, f"Local adapter check failed: {type(error).__name__}."
    return parse_candidate(assignment, response)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integration_check(workspace, assignments, expected_digests):
    """Run the combined adapter set against the frozen interface contract."""
    observed = {}
    failures = {}
    for item in assignments:
        path = workspace / f"{item.channel}.py"
        if item.channel not in expected_digests or not path.is_file():
            failures[item.channel] = "No adapter to integrate."
            continue
        if digest(path) != expected_digests[item.channel]:
            failures[item.channel] = "Adapter changed after its local check."
            continue
        result, reason = local_check(path, item)
        if reason is None:
            _, reason = validate(item, json.dumps(result))
        if reason:
            failures[item.channel] = reason
        else:
            observed[item.channel] = result
    return observed, failures


def coordinate(ask_worker, assignments=ASSIGNMENTS):
    """Run one independent call per worker and at most one correction."""
    if not 1 <= len(assignments) <= MAX_WORKERS:
        raise ValueError("one to three workers are required")
    if any(
        not isinstance(item, Assignment)
        or not isinstance(item.channel, str)
        or re.fullmatch(r"[a-z][a-z0-9_]{0,30}", item.channel) is None
        or type(item.retry_after_seconds) is not int
        or not 0 <= item.retry_after_seconds <= MAX_DELAY_MS // 1000
        for item in assignments
    ):
        raise ValueError("assignments need a channel and nonnegative seconds")
    if len({item.channel for item in assignments}) != len(assignments):
        raise ValueError("worker channels must be distinct")

    # Each worker receives its own assignment, not another worker's output.
    with ThreadPoolExecutor(max_workers=len(assignments)) as pool:
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

    with TemporaryDirectory(prefix="adapter-orchestration-") as directory:
        workspace = Path(directory)
        accepted = {}
        rejections = {}
        initial_local = {}
        accepted_digests = {}
        generated_digests = {}

        def materialize_and_check(item, response):
            candidate, reason = parse_candidate(item, response)
            if reason:
                return None, reason, "not run"
            path = write_adapter(workspace, candidate)
            original = digest(path)
            observed, reason = local_check(path, item)
            if reason:
                return None, reason, "failed"
            if digest(path) != original:
                return None, "Adapter changed during its local check.", "failed"
            generated_digests[item.channel] = original
            return observed, None, "passed"

        for item in assignments:
            _, reason, local = materialize_and_check(
                item, responses[item.channel]
            )
            initial_local[item.channel] = local
            if reason:
                rejections[item.channel] = reason

        # Integration reads the assembled files, rather than worker claims.
        observed, failures = integration_check(
            workspace, assignments, generated_digests
        )
        for item in assignments:
            if item.channel in rejections:
                continue
            reason = failures.get(item.channel)
            if reason:
                rejections[item.channel] = reason
            else:
                accepted[item.channel] = observed[item.channel]
                accepted_digests[item.channel] = digest(
                    workspace / f"{item.channel}.py"
                )

        # Keep accepted files and retry only a rejected assignment once.
        unresolved = {}
        for item in assignments:
            if item.channel not in rejections:
                continue
            try:
                response = ask_worker(item, rejections[item.channel])
            except Exception:
                response = None
            _, reason, _ = materialize_and_check(item, response)
            if reason:
                unresolved[item.channel] = reason

        # Re-execute the assembled adapters from the integrated workspace.
        observed, failures = integration_check(
            workspace, assignments, generated_digests
        )
        final_checks = {}
        for item in assignments:
            if item.channel in unresolved:
                final_checks[item.channel] = "not accepted"
                continue
            reason = failures.get(item.channel)
            final_checks[item.channel] = reason or "passed"
            if reason:
                unresolved[item.channel] = reason
                accepted.pop(item.channel, None)
            else:
                accepted[item.channel] = observed[item.channel]

        preserved = True
        for channel, original in accepted_digests.items():
            path = workspace / f"{channel}.py"
            if not path.is_file() or digest(path) != original:
                preserved = False
                unresolved[channel] = "Previously accepted adapter changed."
                final_checks[channel] = unresolved[channel]
                accepted.pop(channel, None)
        return {
            "accepted": accepted,
            "first_rejections": rejections,
            "initial_local_checks": initial_local,
            "final_integration_checks": final_checks,
            "checked_files": sorted(
                path.name for path in workspace.glob("*.py")
            ),
            "accepted_files_unchanged": preserved,
            "unresolved": unresolved,
            "complete": (
                len(accepted) == len(assignments)
                and not unresolved
                and preserved
            ),
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
