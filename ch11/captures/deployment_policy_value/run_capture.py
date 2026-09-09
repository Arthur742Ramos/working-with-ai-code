#!/usr/bin/env python3
"""Record or replay the isolated deployment-policy capture."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

CAPTURE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = CAPTURE_DIR.parents[1]
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
METADATA_PATH = CAPTURE_DIR / "metadata.json"
BEFORE_SOURCE = CAPTURE_DIR / "before" / "deployment_guard.py"
BEFORE_CONFIG = CAPTURE_DIR / "before" / "deployment.json"
BEFORE_TEST = CAPTURE_DIR / "before" / "test_deployment_guard.py"
FOCUSED_TEST = CAPTURE_DIR / "tests" / "test_deployment_policy.py"
PATCH_PATH = CAPTURE_DIR / "patches" / "deployment_policy_value.diff"
OLD_POLICY_LINE = '    "max_unavailable": 2\n'
NEW_POLICY_LINE = '    "max_unavailable": 1\n'
BROAD_TESTS = (
    "test_deployment_guard.py",
    "test_incident_triage.py",
    "test_pipeline.py",
)
PACKAGE_SUPPORT_FILES = (
    "README.md",
    "deployment_guard.py",
    "deployment.json",
    "incident_triage.py",
    "incident.jsonl",
    "listing_11_5.txt",
    "observation.json",
    "parity.md",
    "pipeline.py",
    "pytest.ini",
    "requirements.txt",
    "test_deployment_guard.py",
    "test_incident_triage.py",
    "test_listing_parity.py",
    "test_pipeline.py",
)
WORK_SUPPORT_FILES = (
    "deployment_guard.py",
    "deployment.json",
    "incident_triage.py",
    "incident.jsonl",
    "observation.json",
    "pipeline.py",
    *BROAD_TESTS,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_checksum(path: Path, expected: str) -> None:
    observed = sha256(path)
    if observed != expected:
        raise RuntimeError(
            f"checksum drift: {path}\n"
            f"expected: {expected}\n"
            f"observed: {observed}"
        )


def stable_pytest_output(output: str) -> str:
    return re.sub(
        r"in \d+(?:\.\d+)?s",
        "in <TIME>s",
        output,
    )


def run_command(
    command: list[str],
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({
        "PY_COLORS": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
    })
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def focused_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "test_deployment_policy.py::"
        "test_schema_valid_deployment_satisfies_policy",
    ]


def broader_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        *BROAD_TESTS,
    ]


def final_package_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
    ]


def prepare_work(work_dir: Path) -> None:
    for relative in WORK_SUPPORT_FILES:
        shutil.copy2(PACKAGE_DIR / relative, work_dir / relative)
    shutil.copy2(BEFORE_SOURCE, work_dir / "deployment_guard.py")
    shutil.copy2(BEFORE_CONFIG, work_dir / "deployment.json")
    shutil.copy2(BEFORE_TEST, work_dir / "test_deployment_guard.py")
    shutil.copy2(FOCUSED_TEST, work_dir / "test_deployment_policy.py")
    red_fixture = (
        work_dir
        / "captures"
        / "deployment_policy_value"
        / "before"
    )
    red_fixture.mkdir(parents=True)
    shutil.copy2(BEFORE_CONFIG, red_fixture / "deployment.json")


def apply_approved_change(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(OLD_POLICY_LINE) != 1:
        raise RuntimeError("approved policy value or location drifted")
    path.write_text(
        text.replace(OLD_POLICY_LINE, NEW_POLICY_LINE),
        encoding="utf-8",
    )


def generated_patch(before: Path, after: Path) -> str:
    before_lines = before.read_text(
        encoding="utf-8"
    ).splitlines(keepends=True)
    after_lines = after.read_text(
        encoding="utf-8"
    ).splitlines(keepends=True)
    return "".join(difflib.unified_diff(
        before_lines,
        after_lines,
        fromfile="a/deployment.json",
        tofile="b/deployment.json",
    ))


def verify_review_state(metadata: dict) -> None:
    if metadata.get("capture_stage") != (
        "complete_independently_reviewed"
    ):
        return

    required = {
        "independent_review_status": "completed",
        "status": "Pass",
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

    artifact = review.get("artifact_path")
    if not isinstance(artifact, str) or not artifact.strip():
        raise RuntimeError(
            "completed review stage requires a review artifact"
        )
    if artifact.strip().lower() == "pending":
        raise RuntimeError("completed review artifact cannot be pending")
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

    expected = review.get("artifact_checksum_sha256")
    if not isinstance(expected, str) or not expected.strip():
        raise RuntimeError(
            "completed review stage requires a review artifact checksum"
        )
    require_checksum(artifact_path, expected)


def verify_static_inputs(metadata: dict) -> None:
    for relative, expected in metadata[
        "before_fixture"
    ]["checksums_sha256"].items():
        require_checksum(CAPTURE_DIR / relative, expected)
    for relative, expected in metadata[
        "capture_input_checksums_sha256"
    ].items():
        require_checksum(CAPTURE_DIR / relative, expected)
    package_checksums = metadata[
        "final_package_support"
    ]["checksums_sha256"]
    if set(package_checksums) != set(PACKAGE_SUPPORT_FILES):
        raise RuntimeError("package checksum coverage drifted")
    for relative, expected in package_checksums.items():
        require_checksum(PACKAGE_DIR / relative, expected)


def verify_stored_artifacts(metadata: dict) -> None:
    for relative, expected in metadata[
        "artifact_checksums_sha256"
    ].items():
        require_checksum(CAPTURE_DIR / relative, expected)


def write_or_compare_result(
    result: subprocess.CompletedProcess[str],
    expected_status: int,
    output_path: Path,
    status_path: Path,
    record: bool,
) -> None:
    if result.returncode != expected_status:
        raise RuntimeError(
            f"exit status drift for {output_path.name}: "
            f"expected {expected_status}, "
            f"observed {result.returncode}\n"
            f"output:\n{result.stdout}"
        )
    normalized_output = stable_pytest_output(result.stdout)
    if record:
        output_path.write_text(normalized_output, encoding="utf-8")
        status_path.write_text(
            f"{result.returncode}\n",
            encoding="utf-8",
        )
        return
    expected_output = output_path.read_text(encoding="utf-8")
    if normalized_output != expected_output:
        raise RuntimeError(f"stored output drift: {output_path}")
    expected_status_text = status_path.read_text(encoding="utf-8")
    if expected_status_text != f"{result.returncode}\n":
        raise RuntimeError(f"stored exit status drift: {status_path}")


def write_or_compare_patch(patch: str, record: bool) -> None:
    if record:
        PATCH_PATH.write_text(patch, encoding="utf-8")
        return
    if PATCH_PATH.read_text(encoding="utf-8") != patch:
        raise RuntimeError("stored patch drift")


def verify_action_record(metadata: dict) -> None:
    record = metadata["agent_action_record"]
    path = CAPTURE_DIR / record["path"]
    require_checksum(path, record["sha256"])
    actions = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]
    sequences = [action["sequence"] for action in actions]
    if sequences != list(range(1, len(actions) + 1)):
        raise RuntimeError("agent action sequence drifted")


def verify_parity(metadata: dict) -> None:
    capture_parity = (CAPTURE_DIR / "parity.md").read_text()
    package_parity = (PACKAGE_DIR / "parity.md").read_text()
    required_capture = {
        metadata["red"]["output_path"],
        metadata["patch"]["path"],
        metadata["focused_green"]["output_path"],
        metadata["broader_green"]["output_path"],
        metadata["final_package_green"]["output_path"],
        metadata["agent_action_record"]["path"],
    }
    missing_capture = sorted(
        item for item in required_capture
        if item not in capture_parity
    )
    if missing_capture:
        raise RuntimeError(
            "capture parity ledger is missing: "
            + ", ".join(missing_capture)
        )
    required_package = {
        "Listing 11.1",
        "Listing 11.2",
        "Listing 11.3",
        "Listing 11.4",
        "Listing 11.5",
        "listing_11_5.txt",
        "test_listing_parity.py",
    }
    missing_package = sorted(
        item for item in required_package
        if item not in package_parity
    )
    if missing_package:
        raise RuntimeError(
            "package parity ledger is missing: "
            + ", ".join(missing_package)
        )


def result_paths(metadata: dict, stage: str) -> tuple[Path, Path]:
    entry = metadata[stage]
    return (
        CAPTURE_DIR / entry["output_path"],
        CAPTURE_DIR / entry["exit_status_path"],
    )


def handle_result(
    metadata: dict,
    stage: str,
    result: subprocess.CompletedProcess[str],
    record: bool,
) -> None:
    output_path, status_path = result_paths(metadata, stage)
    write_or_compare_result(
        result,
        metadata[stage]["exit_status"],
        output_path,
        status_path,
        record,
    )


def capture(record: bool) -> None:
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    verify_review_state(metadata)
    verify_static_inputs(metadata)
    verify_action_record(metadata)
    if not record:
        verify_stored_artifacts(metadata)

    package_before = {
        relative: sha256(PACKAGE_DIR / relative)
        for relative in PACKAGE_SUPPORT_FILES
    }

    with tempfile.TemporaryDirectory(
        dir=CAPTURE_DIR,
        prefix=".work-",
    ) as temp_dir:
        work_dir = Path(temp_dir)
        prepare_work(work_dir)

        red = run_command(focused_command(), work_dir)
        handle_result(metadata, "red", red, record)

        work_config = work_dir / "deployment.json"
        apply_approved_change(work_config)
        require_checksum(
            work_config,
            metadata["patch"]["after_state_sha256"],
        )
        patch = generated_patch(BEFORE_CONFIG, work_config)
        write_or_compare_patch(patch, record)

        focused_green = run_command(focused_command(), work_dir)
        handle_result(
            metadata,
            "focused_green",
            focused_green,
            record,
        )

        broader_green = run_command(broader_command(), work_dir)
        handle_result(
            metadata,
            "broader_green",
            broader_green,
            record,
        )

    final_green = run_command(
        final_package_command(),
        PACKAGE_DIR,
    )
    handle_result(
        metadata,
        "final_package_green",
        final_green,
        record,
    )

    for relative, before_hash in package_before.items():
        if sha256(PACKAGE_DIR / relative) != before_hash:
            raise RuntimeError(
                "final package changed during replay: "
                f"{relative}"
            )

    if not record:
        verify_stored_artifacts(metadata)
        verify_parity(metadata)

    status = "RECORDED" if record else "VERIFIED"
    print(f"RED {status}: exit {red.returncode}")
    print(f"PATCH {status}: strict one-line production diff")
    print(
        f"FOCUSED GREEN {status}: "
        f"exit {focused_green.returncode}"
    )
    print(
        f"BROADER GREEN {status}: "
        f"exit {broader_green.returncode}"
    )
    print(
        f"FINAL PACKAGE GREEN {status}: "
        f"exit {final_green.returncode}"
    )
    print("ORIGIN PROVENANCE VERIFIED: preserved, not executed")
    if not record:
        print("PARITY VERIFIED: package and capture ledgers complete")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="intentionally recreate reviewed capture evidence",
    )
    args = parser.parse_args()
    capture(args.record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
