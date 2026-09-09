#!/usr/bin/env python3
"""Record or replay the complete idempotent 409 capture."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

RUNNER_PATH = Path(__file__).resolve()
CAPTURE_DIR = RUNNER_PATH.parent
PACKAGE_ROOT = CAPTURE_DIR.parents[1]
METADATA_PATH = CAPTURE_DIR / "metadata.json"
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
REVIEW_ARTIFACT = EVIDENCE_DIR / "independent-review.md"
BEFORE_PATH = CAPTURE_DIR / "before" / "importer.py"
TEST_PATH = CAPTURE_DIR / "tests" / "test_importer.py"
PATCH_PATH = (
    CAPTURE_DIR / "patches" / "idempotent_409_replay.patch"
)
WORK_DIR = CAPTURE_DIR / ".work"
WORK_PATH = WORK_DIR / "importer.py"
PACKAGE_SOURCE = PACKAGE_ROOT / "importer.py"
PACKAGE_TEST = PACKAGE_ROOT / "test_importer_package.py"
PACKAGE_CERTIFICATION_TEST = (
    PACKAGE_ROOT / "test_capture_certification.py"
)
FOCUSED_TEST_ID = (
    "tests/test_importer.py::"
    "test_conflict_is_idempotent_replay"
)
BROADER_TEST_ID = "tests/test_importer.py"
PACKAGE_TEST_ID = "test_importer_package.py"

EVIDENCE_NAMES = {
    "red": "focused-red",
    "focused_green": "focused-green",
    "broader_green": "broader-green",
    "package_support_green": "package-support-green",
}
DOCUMENT_PATHS = {
    "README.md": CAPTURE_DIR / "README.md",
    "session.md": CAPTURE_DIR / "session.md",
    "parity.md": CAPTURE_DIR / "parity.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(output: str) -> str:
    output = re.sub(
        r"0x[0-9a-fA-F]+",
        "0x<address>",
        output,
    )
    return re.sub(
        r"in [0-9]+(?:\.[0-9]+)?s",
        "in <time>s",
        output,
    )


def verify_hash(path: Path, expected: str) -> None:
    observed = sha256(path)
    if observed != expected:
        raise RuntimeError(
            f"checksum drift: {path}\n"
            f"expected: {expected}\n"
            f"observed: {observed}"
        )


def verify_review_state(metadata: dict) -> None:
    required = {
        "stage": "complete_independently_reviewed",
        "review_status": "completed",
        "verdict": "Pass",
    }
    for field, expected in required.items():
        observed = metadata.get(field)
        if observed != expected:
            raise RuntimeError(
                "completed review stage requires "
                f"{field}={expected!r}; observed {observed!r}"
            )

    review = metadata.get("independent_review")
    if not isinstance(review, dict):
        raise RuntimeError(
            "completed review stage requires independent_review metadata"
        )
    if review.get("status") != "completed":
        raise RuntimeError(
            "completed review stage requires active review status "
            "'completed'"
        )
    if review.get("verdict") != "Pass":
        raise RuntimeError(
            "completed review stage requires active verdict 'Pass'"
        )

    artifact = review.get("artifact")
    if not isinstance(artifact, str) or not artifact.strip():
        raise RuntimeError(
            "completed review stage requires a review artifact"
        )
    relative = Path(artifact)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError("review artifact path must be package-local")
    artifact_path = (CAPTURE_DIR / relative).resolve()
    if not artifact_path.is_relative_to(EVIDENCE_DIR.resolve()):
        raise RuntimeError("review artifact must be under evidence/")
    if not artifact_path.is_file():
        raise RuntimeError(
            f"completed review artifact is missing: {artifact}"
        )

    expected = review.get("artifact_sha256")
    if not isinstance(expected, str) or not expected.strip():
        raise RuntimeError(
            "completed review stage requires a review artifact checksum"
        )
    verify_hash(artifact_path, expected)


def verify_inputs(metadata: dict) -> None:
    checks = {
        RUNNER_PATH: metadata["runner_sha256"],
        BEFORE_PATH: metadata["before_fixture_checksums"][
            "before/importer.py"
        ],
        TEST_PATH: metadata["focused_test_checksums"][
            "tests/test_importer.py"
        ],
        PATCH_PATH: metadata["patch"]["sha256"],
        PACKAGE_SOURCE: metadata[
            "package_support_checksums"
        ]["importer.py"],
        PACKAGE_TEST: metadata[
            "package_support_checksums"
        ]["test_importer_package.py"],
        PACKAGE_CERTIFICATION_TEST: metadata[
            "package_support_checksums"
        ]["test_capture_certification.py"],
    }
    for path, expected in checks.items():
        verify_hash(path, expected)
    for relative_path, expected in metadata[
        "supplemental_artifact_checksums"
    ].items():
        verify_hash(CAPTURE_DIR / relative_path, expected)


def verify_documents(metadata: dict) -> None:
    for name, path in DOCUMENT_PATHS.items():
        verify_hash(path, metadata["document_checksums"][name])


def evidence_paths(name: str) -> tuple[Path, Path, Path]:
    evidence_dir = CAPTURE_DIR / "evidence"
    return (
        evidence_dir / f"{name}.txt",
        evidence_dir / f"{name}.normalized.txt",
        evidence_dir / f"{name}.exit-status",
    )


def verify_evidence_hashes(metadata: dict) -> None:
    for relative_path, expected in metadata[
        "evidence_checksums"
    ].items():
        verify_hash(CAPTURE_DIR / relative_path, expected)


def prepare_before_state() -> None:
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    WORK_DIR.mkdir()
    shutil.copyfile(BEFORE_PATH, WORK_PATH)


def run_pytest(
    test_id: str,
    *,
    cwd: Path,
    python_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if python_path is not None:
        env["PYTHONPATH"] = str(python_path)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--color=no",
            "-p",
            "no:cacheprovider",
            test_id,
        ],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def require_red(result: subprocess.CompletedProcess[str]) -> None:
    required = (
        "test_conflict_is_idempotent_replay",
        ".work/importer.py:83: RuntimeError",
        "1 failed in ",
    )
    if result.returncode != 1:
        raise RuntimeError(
            "focused command did not produce exit status 1\n"
            f"output:\n{result.stdout}"
        )
    if any(item not in result.stdout for item in required):
        raise RuntimeError(
            "focused command no longer discriminates the selected "
            f"behavior\noutput:\n{result.stdout}"
        )


def apply_and_verify_patch(metadata: dict) -> None:
    completed = subprocess.run(
        ["patch", "-s", "-p1", "-i", str(PATCH_PATH)],
        cwd=WORK_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"stored patch did not apply\n{completed.stdout}"
        )

    generated = subprocess.run(
        [
            "diff",
            "-u",
            "--label",
            "a/importer.py",
            "--label",
            "b/importer.py",
            str(BEFORE_PATH),
            str(WORK_PATH),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if generated.returncode != 1:
        raise RuntimeError(
            "patched state did not produce one ordinary diff\n"
            f"exit: {generated.returncode}\n{generated.stdout}"
        )
    if generated.stdout != PATCH_PATH.read_text(encoding="utf-8"):
        raise RuntimeError("machine-generated diff does not match patch")
    verify_hash(WORK_PATH, metadata["patch"]["after_sha256"])

    removed = [
        line for line in generated.stdout.splitlines()
        if line.startswith("-") and not line.startswith("---")
    ]
    added = [
        line for line in generated.stdout.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    if removed != ["-        if result.status < 400:"]:
        raise RuntimeError("patch removes more than the success condition")
    if added != [
        "+        if result.status < 400 or result.status == 409:"
    ]:
        raise RuntimeError("patch is not the approved exact-status change")


def write_evidence(
    key: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    raw_path, normalized_path, exit_path = evidence_paths(
        EVIDENCE_NAMES[key]
    )
    raw_path.write_text(result.stdout, encoding="utf-8")
    normalized_path.write_text(
        normalize(result.stdout),
        encoding="utf-8",
    )
    exit_path.write_text(
        f"{result.returncode}\n",
        encoding="utf-8",
    )


def verify_evidence(
    key: str,
    result: subprocess.CompletedProcess[str],
    metadata: dict,
) -> None:
    raw_path, normalized_path, exit_path = evidence_paths(
        EVIDENCE_NAMES[key]
    )
    expected_status = metadata[key]["exit_status"]
    stored_status = int(exit_path.read_text(encoding="utf-8"))
    if stored_status != expected_status:
        raise RuntimeError(
            f"stored {key} status disagrees with metadata"
        )
    if result.returncode != expected_status:
        raise RuntimeError(
            f"{key} exit drift: expected {expected_status}, "
            f"observed {result.returncode}\n{result.stdout}"
        )
    stored_raw = raw_path.read_text(encoding="utf-8")
    stored_normalized = normalized_path.read_text(encoding="utf-8")
    if normalize(stored_raw) != stored_normalized:
        raise RuntimeError(f"stored {key} normalization is stale")
    if normalize(result.stdout) != stored_normalized:
        raise RuntimeError(
            f"{key} output drift\nobserved:\n{result.stdout}"
        )


def update_evidence_checksums(metadata: dict) -> None:
    paths = [REVIEW_ARTIFACT]
    for name in EVIDENCE_NAMES.values():
        paths.extend(evidence_paths(name))
    metadata["evidence_checksums"] = {
        str(path.relative_to(CAPTURE_DIR)): sha256(path)
        for path in sorted(paths)
    }
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )


def display_result(
    label: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    print(f"{label} EXIT STATUS: {result.returncode}")
    print(result.stdout, end="")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help=(
            "refresh raw and normalized evidence after intentional "
            "review"
        ),
    )

    try:
        args = parser.parse_args()
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

        verify_review_state(metadata)
        verify_inputs(metadata)
        verify_documents(metadata)
        if not args.record:
            verify_evidence_hashes(metadata)

        prepare_before_state()
        red = run_pytest(
            FOCUSED_TEST_ID,
            cwd=CAPTURE_DIR,
            python_path=WORK_DIR,
        )
        require_red(red)

        apply_and_verify_patch(metadata)
        focused_green = run_pytest(
            FOCUSED_TEST_ID,
            cwd=CAPTURE_DIR,
            python_path=WORK_DIR,
        )
        broader_green = run_pytest(
            BROADER_TEST_ID,
            cwd=CAPTURE_DIR,
            python_path=WORK_DIR,
        )
        package_green = run_pytest(
            PACKAGE_TEST_ID,
            cwd=PACKAGE_ROOT,
        )
        results = {
            "red": red,
            "focused_green": focused_green,
            "broader_green": broader_green,
            "package_support_green": package_green,
        }

        if args.record:
            for key, result in results.items():
                expected = metadata[key]["exit_status"]
                if result.returncode != expected:
                    raise RuntimeError(
                        f"refusing to record {key}: expected exit "
                        f"{expected}, observed {result.returncode}"
                    )
                write_evidence(key, result)
            update_evidence_checksums(metadata)
            mode = "RECORDED"
        else:
            for key, result in results.items():
                verify_evidence(key, result, metadata)
            mode = "VERIFIED"

        display_result("RED", red)
        print(f"PATCH {mode}: one removed line, one added line")
        display_result("FOCUSED GREEN", focused_green)
        display_result("BROADER GREEN", broader_green)
        display_result("PACKAGE SUPPORT GREEN", package_green)
        print(f"PARITY {mode}: capture and package-local support match")
        return 0
    finally:
        shutil.rmtree(WORK_DIR, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
