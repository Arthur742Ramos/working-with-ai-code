import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from orchestrate_adapters import (
    ASSIGNMENTS,
    Assignment,
    coordinate,
    make_chat_worker,
    scripted_worker,
    validate,
)


def test_integration_rejects_seconds_and_redispatches_only_push():
    calls = []
    lock = threading.Lock()

    def ask(assignment, feedback):
        with lock:
            calls.append((assignment.channel, feedback))
        return scripted_worker(assignment, feedback)

    report = coordinate(ask)
    assert report["complete"]
    assert report["accepted"]["push"]["retry_after_ms"] == 2000
    assert report["first_rejections"] == {
        "push": "retry_after_ms must be the integer 2000."
    }
    assert [channel for channel, _ in calls].count("email") == 1
    assert [channel for channel, _ in calls].count("sms") == 1
    assert [channel for channel, _ in calls].count("push") == 2
    assert not report["unresolved"]


@pytest.mark.parametrize("response", [
    "not json",
    '{"channel": "push", "retry_after_ms": true}',
    '{"channel": "push", "retry_after_ms": 2}',
    '{"channel": "email", "retry_after_ms": 2000}',
    '{"channel": "push", "retry_after_ms": 2000, "extra": 1}',
    '{"channel": "email", "channel": "push", "retry_after_ms": 2000}',
])
def test_check_rejects_malformed_or_incompatible_handoffs(response):
    result, reason = validate(Assignment("push", 2), response)
    assert result is None
    assert reason


def test_worker_failure_preserves_other_accepted_artifacts_and_stops():
    calls = []

    def ask(assignment, feedback):
        calls.append(assignment.channel)
        if assignment.channel == "push":
            raise RuntimeError("service unavailable")
        return scripted_worker(assignment, feedback)

    report = coordinate(ask)
    assert not report["complete"]
    assert set(report["accepted"]) == {"email", "sms"}
    assert set(report["unresolved"]) == {"push"}
    assert "request failed" in report["unresolved"]["push"]
    assert calls.count("push") == 2


def test_assignment_scopes_must_be_nonempty_and_distinct():
    with pytest.raises(ValueError):
        coordinate(scripted_worker, ())
    with pytest.raises(ValueError):
        coordinate(scripted_worker, (ASSIGNMENTS[0], ASSIGNMENTS[0]))
    with pytest.raises(ValueError):
        coordinate(scripted_worker, (Assignment("push", True),))
    with pytest.raises(ValueError):
        coordinate(scripted_worker, (Assignment([], 2),))


def test_http_workers_send_separate_assignments_to_a_local_stub():
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            size = int(self.headers["Content-Length"])
            body = json.loads(self.rfile.read(size))
            task = json.loads(body["messages"][1]["content"])
            requests.append(task)
            candidate = {
                "channel": task["channel"],
                "retry_after_ms": task["retry_after_seconds"] * 1000,
            }
            response = json.dumps({
                "choices": [{"message": {"content": json.dumps(candidate)}}]
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        worker = make_chat_worker(
            f"http://127.0.0.1:{server.server_port}/chat",
            "",
            "local-stub",
        )
        report = coordinate(worker)
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    assert report["complete"]
    assert len(requests) == 3
    assert {task["channel"] for task in requests} == {
        "email", "sms", "push"
    }
    assert all(set(task) == {
        "channel", "retry_after_seconds"
    } for task in requests)


def test_rejects_insecure_remote_endpoint():
    with pytest.raises(ValueError):
        make_chat_worker("http://example.com/chat", "secret", "model")
