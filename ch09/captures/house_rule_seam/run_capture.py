#!/usr/bin/env python3
"""Replay the public Chapter 9 house-rule seam capture."""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


CAPTURE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = CAPTURE_DIR.parents[1]
BEFORE_DIR = CAPTURE_DIR / "before"
AFTER_DIR = CAPTURE_DIR / "after"
TESTS_DIR = CAPTURE_DIR / "tests"
PATCH_PATH = CAPTURE_DIR / "patches" / "house_rule_seam.patch"
WORK_DIR = CAPTURE_DIR / ".work"


def clean_work_directories(root: Path = CAPTURE_DIR) -> None:
    for path in root.glob(".work*"):
        if path.is_dir():
            shutil.rmtree(path)


def require_work_cleanup(root: Path = CAPTURE_DIR) -> None:
    remaining = [
        path for path in root.glob(".work*") if path.is_dir()
    ]
    if remaining:
        raise RuntimeError(
            "capture cleanup failed: "
            + ", ".join(path.name for path in remaining)
        )


def run_pytest(
    target: str | None = None, root: Path = WORK_DIR,
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "--basetemp",
        str(WORK_DIR / ".pytest-tmp"),
    ]
    if target is not None:
        command.append(target)
    environment = os.environ.copy()
    environment.update({
        "PY_COLORS": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTEST_ADDOPTS": "",
        "HOUSE_RULE_ROOT": str(root),
        "PYTHONPATH": str(root),
    })
    return subprocess.run(
        command,
        cwd=root,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def stage(state: Path) -> None:
    clean_work_directories()
    WORK_DIR.mkdir()
    for filename in ("alerts.py", "http_client.py"):
        shutil.copy2(state / filename, WORK_DIR / filename)
    optional_transport = state / "requests.py"
    if optional_transport.exists():
        shutil.copy2(optional_transport, WORK_DIR / "requests.py")
    shutil.copytree(TESTS_DIR, WORK_DIR / "tests")


def apply_patch() -> None:
    result = subprocess.run(
        [
            "patch",
            "-p1",
            "--batch",
            "--forward",
            "-i",
            str(PATCH_PATH),
        ],
        cwd=WORK_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "capture patch failed:\n" + result.stdout
        )
    verify_after_state()


def verify_after_state() -> None:
    for filename in ("alerts.py", "http_client.py"):
        if (WORK_DIR / filename).read_bytes() != (
            AFTER_DIR / filename
        ).read_bytes():
            raise RuntimeError(f"recreated after state drifted: {filename}")


def require_result(result, status: int, summary: str, diagnostic="") -> None:
    if (
        result.returncode != status
        or re.search(rf"(?m)^{re.escape(summary)}(?: in .+)?$", result.stdout)
        is None
        or diagnostic not in result.stdout
    ):
        raise RuntimeError(f"capture result did not match {summary}:\n{result.stdout}")


def replay() -> None:
    try:
        stage(BEFORE_DIR)
        red = run_pytest(
            "tests/test_alerts.py::"
            "test_send_alert_routes_through_house_client"
        )
        print("focused_red")
        print(red.stdout, end="")
        require_result(
            red, 1, "1 failed",
            "send_alert must route method, URL, and JSON through http_client.call",
        )

        apply_patch()
        focused = run_pytest(
            "tests/test_alerts.py::"
            "test_send_alert_routes_through_house_client"
        )
        print("focused_green")
        print(focused.stdout, end="")
        require_result(focused, 0, "1 passed")

        broader = run_pytest()
        print("broader_green")
        print(broader.stdout, end="")
        require_result(broader, 0, "10 passed")

        package = run_pytest(root=PACKAGE_DIR)
        print("package_green")
        print(package.stdout, end="")
        if package.returncode != 0:
            raise RuntimeError("maintained package check failed")
    finally:
        clean_work_directories()
        require_work_cleanup()


if __name__ == "__main__":
    replay()
