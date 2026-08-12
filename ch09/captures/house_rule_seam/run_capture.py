#!/usr/bin/env python3
"""Replay the public Chapter 9 house-rule seam capture."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


CAPTURE_DIR = Path(__file__).resolve().parent
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


def run_pytest(target: str | None = None) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
    ]
    if target is not None:
        command.append(target)
    environment = os.environ.copy()
    environment.update({
        "PY_COLORS": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTHONPATH": str(WORK_DIR),
    })
    return subprocess.run(
        command,
        cwd=WORK_DIR,
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


def replay() -> None:
    try:
        stage(BEFORE_DIR)
        red = run_pytest(
            "tests/test_alerts.py::"
            "test_send_alert_routes_through_house_client"
        )
        print("focused_red")
        print(red.stdout, end="")
        if red.returncode != 1:
            raise RuntimeError(
                "before state did not produce the expected focused red"
            )

        apply_patch()
        focused = run_pytest(
            "tests/test_alerts.py::"
            "test_send_alert_routes_through_house_client"
        )
        print("focused_green")
        print(focused.stdout, end="")
        if focused.returncode != 0:
            raise RuntimeError("focused after-state check failed")

        broader = run_pytest()
        print("broader_green")
        print(broader.stdout, end="")
        if broader.returncode != 0:
            raise RuntimeError("broader after-state check failed")
    finally:
        clean_work_directories()
        require_work_cleanup()


if __name__ == "__main__":
    replay()
