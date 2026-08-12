"""Checks for the public SQLite seam capture and its cleanup boundary."""

import importlib.util
from pathlib import Path

import pytest


PACKAGE_DIR = Path(__file__).resolve().parents[1]
CAPTURE_DIR = (
    PACKAGE_DIR / "captures" / "sqlite_row_conversion_seam"
)
RUNNER_PATH = CAPTURE_DIR / "run_capture.py"
SPEC = importlib.util.spec_from_file_location(
    "sqlite_row_capture_runner",
    RUNNER_PATH,
)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def test_capture_preserves_the_focused_row_boundary():
    session = (
        CAPTURE_DIR / "session.md"
    ).read_text(encoding="utf-8")
    patch = (
        CAPTURE_DIR / "patches" / "sqlite_row_conversion.diff"
    ).read_text(encoding="utf-8")

    assert "test_get_for_user_maps_unsnoozed_reminder" in session
    assert "sqlite3.Row" in session
    assert 'row.get("snoozed_until")' in patch
    assert 'row["snoozed_until"]' in patch


def test_capture_runner_is_public_and_package_local():
    runner = RUNNER_PATH.read_text(encoding="utf-8")
    session = (
        CAPTURE_DIR / "session.md"
    ).read_text(encoding="utf-8")

    for forbidden in (
        "AI_Book_Official",
        "manuscripts/",
        "chapters/",
        "code/ch10",
    ):
        assert forbidden not in runner
        assert forbidden not in session


def test_capture_cleanup_removes_only_work_directories(tmp_path):
    (tmp_path / ".work").mkdir()
    (tmp_path / ".work-review").mkdir()
    retained = tmp_path / "evidence"
    retained.mkdir()

    RUNNER.clean_work_directories(tmp_path)
    RUNNER.require_work_cleanup(tmp_path)

    assert retained.is_dir()


def test_capture_runner_uses_the_real_adapter_suite():
    runner = RUNNER_PATH.read_text(encoding="utf-8")

    assert "tests/test_sqlite_repository.py" in runner
    assert "test_get_for_user_maps_unsnoozed_reminder" in runner
