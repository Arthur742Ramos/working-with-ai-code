import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

import orchestrate_adapters
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
    assert report["initial_local_checks"] == {
        "email": "passed", "sms": "passed", "push": "passed"
    }
    assert report["final_integration_checks"] == {
        "email": "passed", "sms": "passed", "push": "passed"
    }
    assert report["checked_files"] == ["email.py", "push.py", "sms.py"]
    assert report["accepted_files_unchanged"]


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
    with pytest.raises(ValueError):
        coordinate(scripted_worker, (Assignment("../outside", 2),))
    with pytest.raises(ValueError):
        coordinate(scripted_worker, ASSIGNMENTS + (Assignment("fax", 1),))


def test_integration_checks_the_files_instead_of_the_worker_claim(monkeypatch):
    original_write = orchestrate_adapters.write_adapter

    def corrupt_push(workspace, candidate):
        path = original_write(workspace, candidate)
        if candidate["channel"] == "push":
            path.write_text(path.read_text().replace("2000", "2"))
        return path

    monkeypatch.setattr(orchestrate_adapters, "write_adapter", corrupt_push)

    def correct_worker(assignment, feedback):
        return json.dumps({
            "channel": assignment.channel,
            "retry_after_ms": assignment.retry_after_seconds * 1000,
        })

    report = coordinate(correct_worker)
    assert not report["complete"]
    assert set(report["accepted"]) == {"email", "sms"}
    assert report["unresolved"]["push"] == (
        "retry_after_ms must be the integer 2000."
    )
    assert report["accepted_files_unchanged"]


def test_untrusted_worker_code_is_never_executed(tmp_path):
    marker = tmp_path / "unexpected-write"
    payload = f"__import__('pathlib').Path({str(marker)!r}).touch()"

    def worker(assignment, feedback):
        if assignment.channel == "push":
            return json.dumps({"channel": "push", "retry_after_ms": payload})
        return scripted_worker(assignment, feedback)

    report = coordinate(worker)
    assert not report["complete"]
    assert report["initial_local_checks"]["push"] == "not run"
    assert "push" in report["unresolved"]
    assert not marker.exists()


def test_adapter_writer_rejects_a_path_outside_its_workspace(tmp_path):
    with pytest.raises(ValueError):
        orchestrate_adapters.write_adapter(
            tmp_path, {"channel": "../escape", "retry_after_ms": 1}
        )
    assert not (tmp_path.parent / "escape.py").exists()


def test_integration_detects_an_accepted_file_changed_during_retry(
    monkeypatch, tmp_path
):
    original_write = orchestrate_adapters.write_adapter
    marker = tmp_path / "altered-file-ran"

    def modify_accepted_file(workspace, candidate):
        path = original_write(workspace, candidate)
        if candidate["channel"] == "push" and candidate["retry_after_ms"] == 2000:
            email = workspace / "email.py"
            email.write_text(
                "from pathlib import Path\n"
                f"Path({str(marker)!r}).touch()\n"
                "def retry_settings():\n"
                "    return {'channel': 'email', 'retry_after_ms': 1000}\n"
            )
        return path

    monkeypatch.setattr(orchestrate_adapters, "write_adapter", modify_accepted_file)
    report = coordinate(scripted_worker)
    assert not report["complete"]
    assert not report["accepted_files_unchanged"]
    assert "email" in report["unresolved"]
    assert "email" not in report["accepted"]
    assert not marker.exists()


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
