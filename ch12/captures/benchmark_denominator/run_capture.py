#!/usr/bin/env python3
"""Record or replay the benchmark denominator capture."""

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

CAPTURE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = CAPTURE_DIR.parents[1]
WORK_DIR = CAPTURE_DIR / ".work-replay"
BEFORE_SOURCE = CAPTURE_DIR / "before" / "workflow_metrics.py"
FOCUSED_TEST = CAPTURE_DIR / "tests" / "test_workflow_metrics.py"
PATCH_PATH = CAPTURE_DIR / "patches" / "production.diff"
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
METADATA_PATH = CAPTURE_DIR / "metadata.json"
REVIEW_ARTIFACT = EVIDENCE_DIR / "independent-review.md"
PACKAGE_SOURCE = PACKAGE_DIR / "workflow_metrics.py"
PACKAGE_TEST = PACKAGE_DIR / "test_workflow_metrics.py"
PACKAGE_PYTEST_CONFIG = PACKAGE_DIR / "pytest.ini"
COMPLETED_REVIEW_STAGE = "complete_independently_reviewed"
DOCUMENT_PATHS = {
    "README.md": CAPTURE_DIR / "README.md",
    "parity.md": CAPTURE_DIR / "parity.md",
    "session.md": CAPTURE_DIR / "session.md",
}
FOCUSED_TARGET = (
    "test_workflow_metrics.QualitySuccessRateTests."
    "test_failed_attempts_remain_in_denominator"
)
EXPECTED_AFTER_SHA256 = (
    "e76cb6640d3e2081fc75604779b1c548416edc6d1247e5eed08666a1af84ef0c"
)
EXPECTED_SHA256 = {
    BEFORE_SOURCE: (
        "42d9a1372ecdaedfa7283509018d7c38be5576d27eb36b3cb453105ab5198fbd"
    ),
    FOCUSED_TEST: (
        "330a35b8120cb44b5859db467ba578cb557e8d163d9df361dc36dcbf7d582736"
    ),
    PATCH_PATH: (
        "afdf96e67644b9a2db08e695aae3bfb49032f2b431ae445819653545827b8ba6"
    ),
    PACKAGE_SOURCE: (
        "e76cb6640d3e2081fc75604779b1c548416edc6d1247e5eed08666a1af84ef0c"
    ),
    PACKAGE_TEST: (
        "330a35b8120cb44b5859db467ba578cb557e8d163d9df361dc36dcbf7d582736"
    ),
    PACKAGE_PYTEST_CONFIG: (
        "b3425014fccceb11334322a4c9fbcf5b26a4faa5933caeaeb259c408a2648861"
    ),
}
EXPECTED_EVIDENCE_SHA256 = {
    EVIDENCE_DIR / "focused-red.txt": (
        "67e135094679a2b6b2cf721f64b8a8dbb0015e71461c8f7297807f6f4de4dea4"
    ),
    EVIDENCE_DIR / "focused-red.exit-status": (
        "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865"
    ),
    EVIDENCE_DIR / "patch-apply.txt": (
        "94eecf5ae0852539a1603b84f1ee713b802f93274a51d6bd52c311df68d42e13"
    ),
    EVIDENCE_DIR / "patch-apply.exit-status": (
        "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"
    ),
    EVIDENCE_DIR / "focused-green.txt": (
        "877b2815511d87520bdb52b9daf2fd6bde6c2f97154ae54602f3dc03d0715928"
    ),
    EVIDENCE_DIR / "focused-green.exit-status": (
        "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"
    ),
    EVIDENCE_DIR / "broader-green.txt": (
        "434b1baf383d85b8173af1ee3cade53120ac37b550707174ba014101149a216f"
    ),
    EVIDENCE_DIR / "broader-green.exit-status": (
        "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"
    ),
    REVIEW_ARTIFACT: (
        "9d968a34a370ec0b516121ea585d5fd5cd1de668e568f6d54ccc5cf471b9a8a3"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checksum_value(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"missing checksum field: {field}")
    return value.removeprefix("sha256:")


def load_metadata() -> dict[str, object]:
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def verify_hashes(expected_hashes: dict[Path, str]) -> None:
    for path, expected in expected_hashes.items():
        if not path.exists():
            raise RuntimeError(f"required file is missing: {path}")
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(
                f"checksum drift: {path}\n"
                f"expected {expected}\nactual   {actual}"
            )


def verify_active_review(metadata: dict[str, object]) -> None:
    if metadata.get("capture_stage") != COMPLETED_REVIEW_STAGE:
        return

    required = {
        "independent_review_status": "completed",
        "status": "Pass",
    }
    for field, expected in required.items():
        observed = metadata.get(field)
        if observed != expected:
            raise RuntimeError(
                f"completed review stage requires {field}={expected!r}; "
                f"observed {observed!r}"
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
    if artifact.strip().lower() == "pending":
        raise RuntimeError("completed review artifact cannot be pending")
    relative_artifact = Path(artifact)
    if relative_artifact.is_absolute() or ".." in relative_artifact.parts:
        raise RuntimeError("review artifact path must be package-local")
    artifact_path = (CAPTURE_DIR / relative_artifact).resolve()
    if not artifact_path.is_relative_to(EVIDENCE_DIR.resolve()):
        raise RuntimeError("review artifact must be under evidence/")
    if not artifact_path.is_file():
        raise RuntimeError(
            f"completed review artifact is missing: {artifact_path}"
        )

    expected = checksum_value(
        review.get("artifact_checksum"),
        "independent_review.artifact_checksum",
    )
    observed = sha256(artifact_path)
    if observed != expected:
        raise RuntimeError(
            "independent review artifact checksum drift\n"
            f"expected: {expected}\nobserved: {observed}"
        )


def verify_record_checksums(metadata: dict[str, object]) -> None:
    runner = metadata.get("runner")
    if not isinstance(runner, dict):
        raise RuntimeError("missing runner metadata")
    runner_checksum = checksum_value(
        runner.get("checksum_sha256"),
        "runner.checksum_sha256",
    )
    verify_hashes({Path(__file__).resolve(): runner_checksum})

    document_checksums = metadata.get("document_checksums_sha256")
    if not isinstance(document_checksums, dict):
        raise RuntimeError("missing document_checksums_sha256 metadata")
    for relative, path in DOCUMENT_PATHS.items():
        expected = checksum_value(
            document_checksums.get(relative),
            f"document_checksums_sha256.{relative}",
        )
        verify_hashes({path: expected})


def verify_inputs(check_evidence: bool) -> None:
    metadata = load_metadata()
    verify_active_review(metadata)
    verify_record_checksums(metadata)
    verify_hashes(EXPECTED_SHA256)
    if check_evidence:
        verify_hashes(EXPECTED_EVIDENCE_SHA256)
    if sha256(PACKAGE_SOURCE) != EXPECTED_AFTER_SHA256:
        raise RuntimeError("package source is not the reviewed after-state")
    if BEFORE_SOURCE.read_bytes() == PACKAGE_SOURCE.read_bytes():
        raise RuntimeError("package source still contains the red before-state")
    if FOCUSED_TEST.read_bytes() != PACKAGE_TEST.read_bytes():
        raise RuntimeError("capture test and package test drifted")


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({
        "FORCE_COLOR": "0",
        "NO_COLOR": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def sanitize_paths(text: str) -> str:
    return re.sub(
        r'File "[^"]*/\.work-replay/test_workflow_metrics\.py"',
        'File "<WORK>/test_workflow_metrics.py"',
        text,
    )


def stable_output(text: str) -> str:
    return re.sub(
        r"Ran (\d+) tests? in \d+(?:\.\d+)?s",
        r"Ran \1 test(s) in <TIME>s",
        sanitize_paths(text),
    )


def verify_red(result: subprocess.CompletedProcess[str]) -> None:
    required = (
        "test_failed_attempts_remain_in_denominator",
        "AssertionError: 1.0 != 0.5",
        "FAILED (failures=1)",
    )
    if result.returncode == 0 or any(
        marker not in result.stdout for marker in required
    ):
        raise RuntimeError(
            "focused test did not produce the required denominator red state"
        )
    if "ImportError" in result.stdout or "_FailedTest" in result.stdout:
        raise RuntimeError("focused test failed during setup, not behavior")


def verify_green(
    name: str,
    result: subprocess.CompletedProcess[str],
    expected_count: int,
) -> None:
    expected = f"Ran {expected_count} test"
    if result.returncode != 0 or expected not in result.stdout:
        raise RuntimeError(
            f"{name} did not pass the expected {expected_count} test(s)"
        )


def evidence_paths(name: str) -> tuple[Path, Path]:
    return (
        EVIDENCE_DIR / f"{name}.txt",
        EVIDENCE_DIR / f"{name}.exit-status",
    )


def record_result(
    name: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    output_path, status_path = evidence_paths(name)
    output_path.write_text(
        sanitize_paths(result.stdout),
        encoding="utf-8",
    )
    status_path.write_text(f"{result.returncode}\n", encoding="utf-8")


def compare_result(
    name: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    output_path, status_path = evidence_paths(name)
    if not output_path.exists() or not status_path.exists():
        raise RuntimeError(
            f"{name} evidence is missing; run --record after review"
        )
    expected_output = output_path.read_text(encoding="utf-8")
    expected_status = status_path.read_text(encoding="utf-8")
    if stable_output(result.stdout) != stable_output(expected_output):
        raise RuntimeError(f"stored {name} output drifted")
    if expected_status != f"{result.returncode}\n":
        raise RuntimeError(f"stored {name} exit status drifted")


def generate_diff(after_source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "diff",
            "-u",
            "--label",
            "a/workflow_metrics.py",
            "--label",
            "b/workflow_metrics.py",
            str(BEFORE_SOURCE),
            str(after_source),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="intentionally refresh verified evidence",
    )
    args = parser.parse_args()

    shutil.rmtree(WORK_DIR, ignore_errors=True)
    try:
        verify_inputs(check_evidence=not args.record)
        WORK_DIR.mkdir()
        work_source = WORK_DIR / "workflow_metrics.py"
        shutil.copy2(BEFORE_SOURCE, work_source)
        shutil.copy2(FOCUSED_TEST, WORK_DIR / "test_workflow_metrics.py")

        focused_command = [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            FOCUSED_TARGET,
        ]
        red = run(focused_command, cwd=WORK_DIR)
        verify_red(red)

        patch = run(
            ["patch", "-p1", "-i", str(PATCH_PATH)],
            cwd=WORK_DIR,
        )
        if patch.returncode != 0:
            raise RuntimeError("production patch did not apply cleanly")
        if sha256(work_source) != EXPECTED_AFTER_SHA256:
            raise RuntimeError("patched after-state checksum drifted")

        generated = generate_diff(work_source)
        if generated.returncode != 1:
            raise RuntimeError("machine diff did not report one change")
        if generated.stdout != PATCH_PATH.read_text(encoding="utf-8"):
            raise RuntimeError("stored patch is not the exact machine diff")

        focused_green = run(focused_command, cwd=WORK_DIR)
        verify_green("focused green", focused_green, 1)

        broader_green = run(
            [
                sys.executable,
                "-m",
                "unittest",
                "-v",
                "test_workflow_metrics",
            ],
            cwd=WORK_DIR,
        )
        verify_green("broader green", broader_green, 4)

        package_green = run(
            [
                sys.executable,
                "-m",
                "unittest",
                "-v",
                "test_workflow_metrics",
            ],
            cwd=PACKAGE_DIR,
        )
        verify_green("package green", package_green, 4)
        verify_inputs(check_evidence=not args.record)

        results = {
            "focused-red": red,
            "patch-apply": patch,
            "focused-green": focused_green,
            "broader-green": broader_green,
        }
        if args.record:
            EVIDENCE_DIR.mkdir(exist_ok=True)
            for name, result in results.items():
                record_result(name, result)
            mode = "RECORDED"
        else:
            for name, result in results.items():
                compare_result(name, result)
            mode = "VERIFIED"

        print(f"RED {mode}: exit {red.returncode}")
        sys.stdout.write(red.stdout)
        print(f"PATCH {mode}: exit {patch.returncode}")
        sys.stdout.write(patch.stdout)
        print(
            f"FOCUSED GREEN {mode}: exit {focused_green.returncode}"
        )
        sys.stdout.write(focused_green.stdout)
        print(
            f"BROADER GREEN {mode}: exit {broader_green.returncode}"
        )
        sys.stdout.write(broader_green.stdout)
        print(f"PACKAGE GREEN: exit {package_green.returncode}")
        sys.stdout.write(package_green.stdout)
        print("INDEPENDENT REVIEW: PASS")
        print("PARITY: PATCH, EVIDENCE, AND PACKAGE HASHES MATCH")
        return 0
    finally:
        shutil.rmtree(WORK_DIR, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
