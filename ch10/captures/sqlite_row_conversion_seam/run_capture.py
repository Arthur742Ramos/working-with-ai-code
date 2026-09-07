#!/usr/bin/env python3
"""Replay the public Chapter 10 SQLite row-conversion capture."""

from __future__ import annotations

import os
from pathlib import Path
import re
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


def run_pytest(
    target: str | None = None, root: Path = WORK_DIR,
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--tb=short",
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
    verify_after_state()


def verify_after_state() -> None:
    before = (BEFORE_PACKAGE / "repository.py").read_text(encoding="utf-8")
    old = 'row.get("snoozed_until")'
    if before.count(old) != 1:
        raise RuntimeError("before state must contain exactly one row.get call")
    expected = before.replace(old, 'row["snoozed_until"]')
    actual = (WORK_DIR / "reminders" / "repository.py").read_text(encoding="utf-8")
    if actual != expected:
        raise RuntimeError("capture patch must make only the one-line row repair")
    for filename in ("domain.py", "repository.py"):
        if (WORK_DIR / "reminders" / filename).read_bytes() != (
            PACKAGE_DIR / "reminders" / filename
        ).read_bytes():
            raise RuntimeError(f"maintained adapter drifted: {filename}")


def require_evidence(result, phase: str) -> None:
    expected_status = 1 if phase == "focused_red" else 0
    summary = {
        "focused_red": "1 failed",
        "focused_green": "1 passed",
        "broader_green": "12 passed",
    }[phase]
    diagnostic = "AttributeError: 'sqlite3.Row' object has no attribute 'get'"
    evidence = (CAPTURE_DIR / "evidence" / f"{phase}.txt").read_text(
        encoding="utf-8",
    )
    status = (CAPTURE_DIR / "evidence" / f"{phase}.exit_status").read_text(
        encoding="utf-8",
    )
    if (
        result.returncode != expected_status
        or status.strip() != str(expected_status)
        or evidence.splitlines()[-1] != summary
        or re.search(rf"(?m)^{re.escape(summary)}(?: in .+)?$", result.stdout)
        is None
        or (expected_status == 1 and (
            diagnostic not in result.stdout or diagnostic not in evidence
        ))
    ):
        raise RuntimeError(f"{phase} evidence mismatch:\n{result.stdout}")


def replay() -> None:
    try:
        stage_before_state()
        red = run_pytest(FOCUSED_TARGET)
        print("focused_red")
        print(red.stdout, end="")
        require_evidence(red, "focused_red")

        apply_patch()
        focused = run_pytest(FOCUSED_TARGET)
        print("focused_green")
        print(focused.stdout, end="")
        require_evidence(focused, "focused_green")

        broader = run_pytest("tests/test_sqlite_repository.py")
        print("broader_green")
        print(broader.stdout, end="")
        require_evidence(broader, "broader_green")

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
