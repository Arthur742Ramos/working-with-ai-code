"""Reject independent-review artifacts outside evidence/."""

import copy
import importlib.util
from pathlib import Path

import pytest

CAPTURE_DIR = Path(__file__).resolve().parents[1]
RUNNER_PATH = CAPTURE_DIR / "run_capture.py"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "chapter_6_capture_runner",
        RUNNER_PATH,
    )
    runner = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(runner)
    return runner


def test_evidence_root_must_resolve_under_capture(
    tmp_path,
    monkeypatch,
):
    runner = load_runner()
    package = tmp_path / "capture"
    package.mkdir()
    outside_evidence = tmp_path / "outside-evidence"
    outside_evidence.mkdir()
    review = outside_evidence / "independent-review.md"
    review.write_text("review receipt\n", encoding="utf-8")
    evidence = package / "evidence"
    evidence.symlink_to(outside_evidence, target_is_directory=True)

    metadata = copy.deepcopy(runner.load_metadata())
    metadata["independent_review"][
        "artifact_path"
    ] = "evidence/independent-review.md"
    metadata["independent_review"][
        "artifact_checksum"
    ] = f"sha256:{runner.checksum(review)}"
    monkeypatch.setattr(runner, "CAPTURE_DIR", package)
    monkeypatch.setattr(runner, "EVIDENCE_DIR", evidence)

    with pytest.raises(
        RuntimeError,
        match="evidence directory must resolve under capture package",
    ):
        runner.verify_review_state(metadata)


def test_review_artifact_must_resolve_under_evidence(
    tmp_path,
    monkeypatch,
):
    runner = load_runner()
    package = tmp_path / "capture"
    evidence = package / "evidence"
    evidence.mkdir(parents=True)
    outside = package / "outside-review.md"
    outside.write_text("review receipt\n", encoding="utf-8")
    (evidence / "escaped-review.md").symlink_to(outside)

    metadata = copy.deepcopy(runner.load_metadata())
    checksum = f"sha256:{runner.checksum(outside)}"
    monkeypatch.setattr(runner, "CAPTURE_DIR", package)
    monkeypatch.setattr(runner, "EVIDENCE_DIR", evidence)

    for artifact_path in (
        "outside-review.md",
        "evidence/escaped-review.md",
    ):
        metadata["independent_review"][
            "artifact_path"
        ] = artifact_path
        metadata["independent_review"][
            "artifact_checksum"
        ] = checksum
        with pytest.raises(
            RuntimeError,
            match="review artifact must be under evidence/",
        ):
            runner.verify_review_state(metadata)
