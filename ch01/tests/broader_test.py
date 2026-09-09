"""Protect the healthy limiter path and neighboring bounds."""
import json
import os
import subprocess
import sys
from pathlib import Path

from focused_test import EXPECTED_STATUSES

TEST_NAME = "test_healthy_storage_emits_no_fallback_warning"


def main():
    if len(sys.argv) > 2:
        raise SystemExit("usage: broader_test.py [APP_PATH]")
    package_app = Path(__file__).resolve().parents[1] / "app.py"
    app_path = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) == 2
        else package_app
    )

    environment = os.environ.copy()
    environment["REDIS_URL"] = "memory://"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    focused_test = Path(__file__).with_name("focused_test.py")
    completed = subprocess.run(
        [
            sys.executable,
            str(focused_test),
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
        return 1

    observed = json.loads(completed.stdout)
    statuses = observed["statuses"]
    second_user = observed["second_user"]
    warnings = observed["warnings"]
    if (
        statuses != EXPECTED_STATUSES
        or second_user != 200
        or warnings != 0
    ):
        print(f"FAIL: {TEST_NAME}")
        print(
            f"observed: user-1={statuses}; "
            f"user-2 first={second_user}; warnings={warnings}"
        )
        return 1

    print(f"PASS: {TEST_NAME}")
    print("observed: 0 fallback warnings on application logger")
    print(
        "neighbor retained: user-1 first 10=200, "
        "11th=429; user-2 first=200"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
