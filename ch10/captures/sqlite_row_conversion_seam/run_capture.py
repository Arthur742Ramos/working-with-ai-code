#!/usr/bin/env python3
"""Replay the public Chapter 10 SQLite row-conversion capture."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


CAPTURE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = CAPTURE_DIR.parents[1]
BEFORE_PACKAGE = CAPTURE_DIR / "before" / "reminders"
CAPTURE_TESTS = CAPTURE_DIR / "tests"
PATCH_PATH = CAPTURE_DIR / "patches" / "sqlite_row_conversion.diff"
WORK_DIR = CAPTURE_DIR / ".work"
FOCUSED_TARGET = (
    "tests/test_sqlite_repository.py::"
    "test_get_for_user_maps_unsnoozed_reminder"
)


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
        "--tb=short",
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


def stage_before_state() -> None:
    clean_work_directories()
    WORK_DIR.mkdir()
    shutil.copytree(BEFORE_PACKAGE, WORK_DIR / "reminders")
    shutil.copytree(CAPTURE_TESTS, WORK_DIR / "tests")
    maintained_tests = PACKAGE_DIR / "tests" / "test_sqlite_repository.py"
    shutil.copy2(
        maintained_tests,
        WORK_DIR / "tests" / "test_sqlite_repository.py",
    )


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
        stage_before_state()
        red = run_pytest(FOCUSED_TARGET)
        print("focused_red")
        print(red.stdout, end="")
        if red.returncode != 1:
            raise RuntimeError(
                "before state did not produce the expected focused red"
            )

        apply_patch()
        focused = run_pytest(FOCUSED_TARGET)
        print("focused_green")
        print(focused.stdout, end="")
        if focused.returncode != 0:
            raise RuntimeError("focused after-state check failed")

        broader = run_pytest("tests/test_sqlite_repository.py")
        print("broader_green")
        print(broader.stdout, end="")
        if broader.returncode != 0:
            raise RuntimeError("broader after-state check failed")
    finally:
        clean_work_directories()
        require_work_cleanup()


if __name__ == "__main__":
    replay()
