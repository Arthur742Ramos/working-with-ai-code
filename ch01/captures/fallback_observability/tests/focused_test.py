"""Route Flask-Limiter's fallback warning to the app logger."""
import argparse
import importlib.util
import io
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

OUTAGE_URI = "redis://127.0.0.1:1/0"
EXPECTED_STATUSES = [200] * 10 + [429]
EXPECTED_WARNING = (
    "Rate limit storage unreachable - falling back to in-memory storage"
)
TEST_NAME = "test_redis_outage_routes_fallback_warning_to_app_logger"


class RecordCollector(logging.Handler):
    """Collect application log messages for the assertion."""

    def __init__(self):
        super().__init__()
        self.messages = []

    def emit(self, record):
        self.messages.append(record.getMessage())


def load_app(app_path):
    spec = importlib.util.spec_from_file_location(
        "captured_rate_limiting_app",
        app_path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def post_file(client, name):
    return client.post(
        "/api/upload",
        data={
            "file": (
                io.BytesIO(b"payload"),
                name,
            )
        },
        content_type="multipart/form-data",
    )


def worker(app_path):
    module = load_app(app_path)
    module.app.config.update(
        LOGIN_DISABLED=True,
        TESTING=False,
    )
    module.save_upload = lambda user_id, file: "ignored"

    collector = RecordCollector()
    module.app.logger.addHandler(collector)
    module.app.logger.setLevel(logging.WARNING)
    client = module.app.test_client()

    module.current_user = SimpleNamespace(id="user-1")
    statuses = [
        post_file(client, f"upload-{index}.txt").status_code
        for index in range(11)
    ]

    module.current_user = SimpleNamespace(id="user-2")
    second_user = post_file(
        client,
        "second-user.txt",
    ).status_code

    print(json.dumps({
        "statuses": statuses,
        "second_user": second_user,
        "warnings": collector.messages.count(EXPECTED_WARNING),
    }))
    return 0


def exercise(app_path):
    environment = os.environ.copy()
    environment["REDIS_URL"] = OUTAGE_URI
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker",
            str(app_path),
        ],
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        print(f"FAIL: {TEST_NAME}")
        print(f"worker exit: {completed.returncode}")
        if completed.stdout:
            print(f"worker stdout: {completed.stdout.strip()}")
        if completed.stderr:
            print(f"worker stderr: {completed.stderr.strip()}")
        return None
    return json.loads(completed.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("app_path", nargs="?")
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()

    if args.worker:
        return worker(Path(args.app_path))
    if not args.app_path:
        parser.error("app_path is required")

    observed = exercise(Path(args.app_path).resolve())
    if observed is None:
        return 1

    statuses = observed["statuses"]
    second_user = observed["second_user"]
    if statuses != EXPECTED_STATUSES or second_user != 200:
        print(f"FAIL: {TEST_NAME}")
        print(
            "expected neighbor: user-1 first 10=200, "
            "11th=429; user-2 first=200"
        )
        print(
            f"observed neighbor: user-1={statuses}; "
            f"user-2 first={second_user}"
        )
        return 1

    warning_count = observed["warnings"]
    if warning_count != 1:
        print(f"FAIL: {TEST_NAME}")
        print("expected: 1 fallback warning on application logger")
        print(
            f"observed: {warning_count} fallback warnings "
            "on application logger"
        )
        print(
            "neighbor retained: user-1 first 10=200, "
            "11th=429; user-2 first=200"
        )
        return 1

    print(f"PASS: {TEST_NAME}")
    print("observed: 1 fallback warning on application logger")
    print(
        "neighbor retained: user-1 first 10=200, "
        "11th=429; user-2 first=200"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
