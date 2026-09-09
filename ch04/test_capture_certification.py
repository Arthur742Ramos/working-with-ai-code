"""Certification invariants for the Chapter 4 capture package."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


PACKAGE_ROOT = Path(__file__).resolve().parent
CAPTURE_RELATIVE = Path("captures/idempotent_409_replay")
COMPLETED_STAGE = "complete_independently_reviewed"
COMPLETED_REVIEW_STATUS = "completed"
COMPLETED_VERDICT = "Pass"
COMPLETED_PARITY_LINE = (
    "Stage: `complete_independently_reviewed`; independent review: "
    "`completed`; status: `Pass`."
)


def copy_package(tmp_path: Path) -> Path:
    destination = tmp_path / "ch04"
    shutil.copytree(
        PACKAGE_ROOT,
        destination,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            ".pytest_cache",
            ".work",
        ),
    )
    return destination


def run_capture(package_root: Path) -> subprocess.CompletedProcess[str]:
    runner = package_root / CAPTURE_RELATIVE / "run_capture.py"
    return subprocess.run(
        [sys.executable, str(runner)],
        cwd=package_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def make_before_fixture_green(package_root: Path) -> None:
    capture = package_root / CAPTURE_RELATIVE
    before = capture / "before" / "importer.py"
    before.write_text(
        before.read_text(encoding="utf-8").replace(
            "if result.status < 400:",
            "if result.status < 400 or result.status == 409:",
        ),
        encoding="utf-8",
    )
    metadata_path = capture / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["before_fixture_checksums"]["before/importer.py"] = (
        hashlib.sha256(before.read_bytes()).hexdigest()
    )
    metadata_path.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    ("mode", "expected_exit"),
    (
        ("success", 0),
        ("preflight-failure", 1),
        ("runtime-failure", 1),
    ),
)
def test_capture_removes_work_residue(
    tmp_path: Path,
    mode: str,
    expected_exit: int,
):
    package_root = copy_package(tmp_path)
    capture = package_root / CAPTURE_RELATIVE
    work = capture / ".work"
    work.mkdir()
    (work / "stale.txt").write_text("stale\n", encoding="utf-8")

    if mode == "preflight-failure":
        before = capture / "before" / "importer.py"
        before.write_text(
            before.read_text(encoding="utf-8") + "\n# drift\n",
            encoding="utf-8",
        )
    elif mode == "runtime-failure":
        make_before_fixture_green(package_root)

    result = run_capture(package_root)

    assert result.returncode == expected_exit, result.stdout
    assert not work.exists()


def test_active_review_state_is_completed_and_attributable():
    capture = PACKAGE_ROOT / CAPTURE_RELATIVE
    metadata = json.loads(
        (capture / "metadata.json").read_text(encoding="utf-8")
    )
    parity = (capture / "parity.md").read_text(encoding="utf-8")
    readme = (capture / "README.md").read_text(encoding="utf-8")
    session = (capture / "session.md").read_text(encoding="utf-8")
    review = metadata["independent_review"]
    artifact = capture / review["artifact"]

    assert metadata["stage"] == COMPLETED_STAGE
    assert metadata["review_status"] == COMPLETED_REVIEW_STATUS
    assert metadata["verdict"] == COMPLETED_VERDICT
    assert review["status"] == COMPLETED_REVIEW_STATUS
    assert review["verdict"] == COMPLETED_VERDICT
    assert artifact.is_file()
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == (
        review["artifact_sha256"]
    )
    assert COMPLETED_PARITY_LINE in parity
    assert review["artifact"] in parity
    assert review["artifact"] in readme
    assert "Independent review remains pending." in session
