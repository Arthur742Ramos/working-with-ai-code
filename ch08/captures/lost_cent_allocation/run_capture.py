#!/usr/bin/env python3
"""Record or replay the isolated lost-cent allocation capture."""

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
import tempfile

RUNNER_FILE = Path(__file__).resolve()
CAPTURE_DIR = RUNNER_FILE.parent
PACKAGE_DIR = CAPTURE_DIR.parents[1]
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
REVIEW_ARTIFACT = "evidence/independent-review.md"
REVIEW_FILE = CAPTURE_DIR / REVIEW_ARTIFACT
CAPTURE_README = CAPTURE_DIR / "README.md"
PACKAGE_README = PACKAGE_DIR / "README.md"
BEFORE_SOURCE = CAPTURE_DIR / "before" / "allocation.py"
AFTER_SOURCE = CAPTURE_DIR / "after" / "allocation.py"
FOCUSED_TEST = CAPTURE_DIR / "tests" / "test_lost_cent.py"
BROADER_TEST = CAPTURE_DIR / "tests" / "test_neighboring_behavior.py"
PATCH_FILE = CAPTURE_DIR / "patches" / "allocation.patch"
METADATA_FILE = CAPTURE_DIR / "metadata.json"
SESSION_FILE = CAPTURE_DIR / "session.md"
CHAPTER_SESSION_FILE = CAPTURE_DIR / "chapter-session.md"
PARITY_FILE = CAPTURE_DIR / "parity.md"
PACKAGE_SOURCE = PACKAGE_DIR / "allocation.py"
PACKAGE_TEST = PACKAGE_DIR / "test_allocation.py"
PACKAGE_GOLDEN = PACKAGE_DIR / "test_golden.py"
PACKAGE_PYTEST_CONFIG = PACKAGE_DIR / "pytest.ini"
ORIGIN_OUTPUT = CAPTURE_DIR / "evidence" / "canonical_support_green.txt"
ORIGIN_STATUS = (
    CAPTURE_DIR / "evidence" / "canonical_support_green.exit_status"
)

EXPECTED_SHA256 = {
    BEFORE_SOURCE: "0a2b1eca73f5e7dd639efc7b2ee807689715d0fb28b124ea8b5b82e00ee4d6d1",
    AFTER_SOURCE: "c47c8d22519ad1aa398f8aea5f4eddbe2f6a36f43737cd8a5274933fa8785050",
    FOCUSED_TEST: "d09b09807def03b448edce5754465dced142c359c77c88d812d8696e913116f3",
    BROADER_TEST: "55aee8afceb8be3e3df3bae1232186659753837bfdf2ad59b5bfe8dcb984e817",
    PATCH_FILE: "3632939cdfc57a4bec1979c4b34e1a93ac23ceabc791eccab0d7a8cef8234c4c",
    PACKAGE_SOURCE: "ef91e6ff73c506cc1b429e5559b160eee807461ff6b8ab16d34c32cfa39bb3d5",
    PACKAGE_TEST: "a971ac36680096a059de2739ba61509b41463de7df38b456a800f7981b2089a3",
    PACKAGE_GOLDEN: "00185f0dff41b46d79410ebd5fe648f74962648fc4c06763e5ac21468bc54323",
    PACKAGE_PYTEST_CONFIG: "e1b4e3128564596f36beb28c931208b8626875aeb097b5130558d2be995ae544",
    ORIGIN_OUTPUT: "656c85820780a51906a1a3fc1b3935c8fe46427b8370c0a25df20ad51968da95",
    ORIGIN_STATUS: "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    REVIEW_FILE: "ad5f3c4f93bc6f49ae23e8a146aeae99d43a52e9a0a54fb2ed558f54283f8795",
}

COMMANDS = {
    "focused_red": (
        "python3 -m pytest -q -p no:cacheprovider "
        "test_lost_cent.py::test_equal_exact_remainders_keep_input_order"
    ),
    "focused_green": (
        "python3 -m pytest -q -p no:cacheprovider "
        "test_lost_cent.py::test_equal_exact_remainders_keep_input_order"
    ),
    "broader_green": "python3 -m pytest -q -p no:cacheprovider",
    "final_package_green": (
        "python3 -m pytest -q -p no:cacheprovider "
        "test_allocation.py test_golden.py"
    ),
}
ORIGIN_COMMAND = (
    "python3 -m pytest -q -p no:cacheprovider "
    "test_allocation.py test_golden.py"
)
PACKAGE_FILES = (
    PACKAGE_SOURCE,
    PACKAGE_TEST,
    PACKAGE_GOLDEN,
    PACKAGE_PYTEST_CONFIG,
)
CERTIFICATION_FILES = (
    REVIEW_FILE,
    METADATA_FILE,
    RUNNER_FILE,
    CAPTURE_README,
    PACKAGE_README,
    PARITY_FILE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_static_inputs() -> None:
    for path, expected in EXPECTED_SHA256.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(
                f"checksum drift: {path}\n"
                f"expected {expected}\nactual   {actual}"
            )


def work_directories() -> tuple[Path, ...]:
    return tuple(sorted(CAPTURE_DIR.glob(".work-*")))


def verify_no_work_directories(stage: str) -> None:
    leftovers = work_directories()
    if leftovers:
        names = ", ".join(path.name for path in leftovers)
        raise SystemExit(f"{stage} left replay work directories: {names}")


def verify_failure_cleanup() -> None:
    probe_path: Path | None = None
    try:
        with tempfile.TemporaryDirectory(
            dir=CAPTURE_DIR,
            prefix=".work-cleanup-probe-",
        ) as temp_dir:
            probe_path = Path(temp_dir)
            raise RuntimeError("intentional cleanup probe")
    except RuntimeError as error:
        if str(error) != "intentional cleanup probe":
            raise
    if probe_path is None or probe_path.exists():
        raise SystemExit("exception-path cleanup invariant failed")
    verify_no_work_directories("exception-path cleanup probe")


def verify_review_state(metadata: dict[str, object]) -> None:
    required = {
        "capture_stage": "complete_independently_reviewed",
        "independent_review_status": "completed",
        "status": "Pass",
    }
    for field, expected in required.items():
        observed = metadata.get(field)
        if observed != expected:
            raise SystemExit(
                "completed review state requires "
                f"{field}={expected!r}; observed {observed!r}"
            )

    review = metadata.get("independent_review")
    if not isinstance(review, dict):
        raise SystemExit(
            "completed review state requires independent_review metadata"
        )

    expected_review = {
        "status": "completed",
        "verdict": "Pass",
        "reviewer_role": (
            "Independent canonical capture reviewer, read-only"
        ),
        "reviewer_tool": "Claude Code 2.1.210.bee",
        "reviewer_model": "gpt-5.6-sol[1m]",
        "review_date": "2026-07-15",
        "runtime": {
            "python": "3.14.6",
            "pytest": "9.1.1",
            "patch": "Apple patch 2.0",
        },
        "repository_modified_by_reviewer": False,
        "artifact_path": REVIEW_ARTIFACT,
        "metadata_checksum_claims_matched": 20,
        "historical_hashes_matched": 4,
        "canonical_mirror_files_matched": 28,
        "minimality_verdict": "Pass, narrowly",
        "blocking_findings": [],
    }
    for field, expected in expected_review.items():
        observed = review.get(field)
        if observed != expected:
            raise SystemExit(
                "independent review metadata requires "
                f"{field}={expected!r}; observed {observed!r}"
            )

    expected_checksum = EXPECTED_SHA256[REVIEW_FILE]
    recorded_checksum = review.get("artifact_checksum_sha256")
    if recorded_checksum != expected_checksum:
        raise SystemExit(
            "independent review metadata checksum does not match "
            "the active receipt"
        )
    actual_checksum = sha256(REVIEW_FILE)
    if actual_checksum != expected_checksum:
        raise SystemExit(
            "independent review artifact checksum drift\n"
            f"expected {expected_checksum}\n"
            f"actual   {actual_checksum}"
        )

    receipt = REVIEW_FILE.read_text()
    receipt_markers = (
        "Verdict: **PASS**",
        "Reviewer tool: Claude Code 2.1.210.bee",
        "Reviewer model: `gpt-5.6-sol[1m]`",
        "Runtime: Python 3.14.6, pytest 9.1.1, "
        "Apple `patch` 2.0",
        "Metadata checksum claims: 20 of 20 matched",
        "Canonical and mirror non-cache files: "
        "28 of 28 byte-identical",
        "Minimality verdict: **PASS, narrowly**.",
        "intentional `Pending` publication state",
    )
    missing = [item for item in receipt_markers if item not in receipt]
    if missing:
        raise SystemExit(
            "independent review receipt is incomplete: "
            + ", ".join(missing)
        )


def stable_output(text: str) -> str:
    return re.sub(r"in \d+(?:\.\d+)?s", "in <TIME>s", text)


def pytest_environment() -> dict[str, str]:
    env = os.environ.copy()
    env.update({
        "PY_COLORS": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    return env


def run_command(
    command: list[str],
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=pytest_environment(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def focused_result(work: Path) -> subprocess.CompletedProcess[str]:
    return run_command([
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "test_lost_cent.py::test_equal_exact_remainders_keep_input_order",
    ], work)


def broader_result(work: Path) -> subprocess.CompletedProcess[str]:
    return run_command([
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
    ], work)


def final_package_result() -> subprocess.CompletedProcess[str]:
    return run_command([
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "test_allocation.py",
        "test_golden.py",
    ], PACKAGE_DIR)


def evidence_paths(stage: str) -> tuple[Path, Path]:
    evidence_dir = CAPTURE_DIR / "evidence"
    return (
        evidence_dir / f"{stage}.txt",
        evidence_dir / f"{stage}.exit_status",
    )


def record_evidence(
    stage: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    output_path, status_path = evidence_paths(stage)
    output_path.write_text(result.stdout)
    status_path.write_text(f"{result.returncode}\n")


def verify_evidence(
    stage: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    output_path, status_path = evidence_paths(stage)
    if not output_path.exists() or not status_path.exists():
        raise SystemExit(
            f"{stage} evidence is missing; run --record after review"
        )
    expected_output = output_path.read_text()
    expected_status = int(status_path.read_text().strip())
    if result.returncode != expected_status:
        raise SystemExit(
            f"{stage} exit status drift: expected {expected_status}, "
            f"got {result.returncode}"
        )
    if stable_output(result.stdout) != stable_output(expected_output):
        raise SystemExit(f"{stage} output drift")


def handle_evidence(
    stage: str,
    result: subprocess.CompletedProcess[str],
    should_record: bool,
) -> None:
    if should_record:
        record_evidence(stage, result)
        action = "RECORDED"
    else:
        verify_evidence(stage, result)
        action = "VERIFIED"
    print(f"\n[{stage}] {COMMANDS[stage]}")
    sys.stdout.write(result.stdout)
    print(f"{stage.upper()} {action}: exit {result.returncode}")


def machine_generated_patch() -> bytes:
    result = subprocess.run(
        [
            "diff",
            "-u",
            "--label",
            "a/allocation.py",
            "--label",
            "b/allocation.py",
            str(BEFORE_SOURCE),
            str(AFTER_SOURCE),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 1:
        raise SystemExit(
            "could not regenerate the expected non-empty unified diff: "
            f"exit {result.returncode}\n{result.stderr.decode()}"
        )
    return result.stdout


def verify_machine_generated_patch() -> None:
    if machine_generated_patch() != PATCH_FILE.read_bytes():
        raise SystemExit("stored patch is not the exact machine-generated diff")


def apply_patch(work: Path) -> None:
    result = subprocess.run(
        ["patch", "-p1", "-i", str(PATCH_FILE)],
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"patch application failed: exit {result.returncode}\n"
            f"{result.stdout}"
        )
    if sha256(work / "allocation.py") != sha256(AFTER_SOURCE):
        raise SystemExit("patched source does not match the reviewed after-state")
    print("\n[patch]")
    sys.stdout.write(PATCH_FILE.read_text())
    print("PATCH VERIFIED: exact diff applied in disposable space")


def evidence_metadata(stage: str) -> tuple[str, str, int]:
    output_path, status_path = evidence_paths(stage)
    return (
        sha256(output_path),
        sha256(status_path),
        int(status_path.read_text().strip()),
    )


def verify_metadata(metadata: dict[str, object]) -> None:
    verify_review_state(metadata)
    if metadata["coding_agent"] != {
        "tool": "Claude Code",
        "version": "2.1.210",
    }:
        raise SystemExit("metadata coding-agent identity drift")

    fixture_paths = {
        "before_fixture": {
            "before/allocation.py": BEFORE_SOURCE,
            "tests/test_lost_cent.py": FOCUSED_TEST,
        },
        "after_fixture": {
            "after/allocation.py": AFTER_SOURCE,
            "tests/test_neighboring_behavior.py": BROADER_TEST,
        },
    }
    for fixture_name, paths in fixture_paths.items():
        recorded = metadata[fixture_name]["checksums_sha256"]
        for relative_path, path in paths.items():
            if recorded[relative_path] != sha256(path):
                raise SystemExit(
                    f"metadata fixture checksum drift: {relative_path}"
                )

    for stage in COMMANDS:
        output_hash, status_hash, exit_status = evidence_metadata(stage)
        record = metadata[stage]
        if record["command"] != COMMANDS[stage]:
            raise SystemExit(f"metadata command drift for {stage}")
        if record["exit_status"] != exit_status:
            raise SystemExit(f"metadata exit status drift for {stage}")
        if record["output_sha256"] != output_hash:
            raise SystemExit(f"metadata output checksum drift for {stage}")
        if record["exit_status_sha256"] != status_hash:
            raise SystemExit(
                f"metadata exit-status checksum drift for {stage}"
            )

    patch = metadata["patch"]
    if patch["checksum_sha256"] != sha256(PATCH_FILE):
        raise SystemExit("metadata patch checksum drift")

    support = metadata["final_package_support"]
    expected_support = {
        "allocation.py": sha256(PACKAGE_SOURCE),
        "test_allocation.py": sha256(PACKAGE_TEST),
        "test_golden.py": sha256(PACKAGE_GOLDEN),
        "pytest.ini": sha256(PACKAGE_PYTEST_CONFIG),
    }
    if support["checksums_sha256"] != expected_support:
        raise SystemExit("metadata final-package checksum drift")
    if (
        support["canonical_equivalent_test_count"] != 9
        or support["promoted_exact_tie_test_count"] != 1
        or support["total_test_count"] != 10
    ):
        raise SystemExit("metadata final-package test counts drift")

    origin = metadata["origin_canonical_support_green"]
    if origin["command"] != ORIGIN_COMMAND:
        raise SystemExit("origin command provenance drift")
    if origin["output_sha256"] != sha256(ORIGIN_OUTPUT):
        raise SystemExit("origin output provenance drift")
    if origin["exit_status_sha256"] != sha256(ORIGIN_STATUS):
        raise SystemExit("origin exit-status provenance drift")
    if origin["exit_status"] != int(ORIGIN_STATUS.read_text().strip()):
        raise SystemExit("origin exit status provenance drift")
    if origin["replay_status"] != "preserved_not_executed":
        raise SystemExit("origin replay boundary drift")


def verify_parity_record() -> None:
    parity = PARITY_FILE.read_text().lower()
    required = (
        "before/allocation.py",
        "after/allocation.py",
        "tests/test_lost_cent.py",
        "tests/test_neighboring_behavior.py",
        "patches/allocation.patch",
        "chapter-session.md",
        "evidence/focused_red.txt",
        "evidence/focused_green.txt",
        "evidence/broader_green.txt",
        "evidence/canonical_support_green.txt",
        "evidence/final_package_green.txt",
        "evidence/independent-review.md",
        "pytest.ini",
        "cleanup invariant",
        "complete_independently_reviewed",
        "nine canonical-equivalent",
        "promoted exact-tie",
        "preserved_not_executed",
        "largest remainder",
        "stable input order",
        "fraction(str(weight))",
        "allocate(10, [1, 1, 4]) == [2, 2, 6]",
        "allocate(1, [1, 1, 2]) == [0, 0, 1]",
        "claude code 2.1.210",
        "gpt-5.6-sol[1m]",
        "20 metadata checksum claims",
        "28 non-cache files",
        "six certification files",
        "domain owners",
    )
    missing = [item for item in required if item not in parity]
    if missing:
        raise SystemExit(
            "parity record is incomplete: " + ", ".join(missing)
        )


def unquote_callouts(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line == ">":
            lines.append("")
        elif line.startswith("> "):
            lines.append(line[2:])
        else:
            lines.append(line)
    ending = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + ending


def verify_session_records() -> None:
    patch = PATCH_FILE.read_text()
    records = {
        "session.md": SESSION_FILE.read_text(),
        "chapter-session.md": unquote_callouts(
            CHAPTER_SESSION_FILE.read_text()
        ),
    }
    for record_name, text in records.items():
        if patch not in text:
            raise SystemExit(f"exact patch missing from {record_name}")
        for stage in (
            "focused_red",
            "focused_green",
            "broader_green",
        ):
            output_path, _ = evidence_paths(stage)
            if COMMANDS[stage] not in text:
                raise SystemExit(
                    f"{stage} command missing from {record_name}"
                )
            if output_path.read_text() not in text:
                raise SystemExit(
                    f"{stage} evidence missing from {record_name}"
                )
        if ORIGIN_COMMAND not in text:
            raise SystemExit(
                f"origin verification command missing from {record_name}"
            )
        if ORIGIN_OUTPUT.read_text() not in text:
            raise SystemExit(
                f"origin verification evidence missing from {record_name}"
            )

    chapter_session = records["chapter-session.md"].lower()
    if "claude code 2.1.210" not in chapter_session:
        raise SystemExit("coding-agent version missing from chapter session")
    private_markers = (
        "manuscripts/restructure",
        "/".join(("code", "ch08")),
    )
    if any(marker in chapter_session for marker in private_markers):
        raise SystemExit("private support path leaked into chapter session")


def copy_capture_inputs(work: Path) -> None:
    shutil.copy2(BEFORE_SOURCE, work / "allocation.py")
    shutil.copy2(FOCUSED_TEST, work / "test_lost_cent.py")
    shutil.copy2(BROADER_TEST, work / "test_neighboring_behavior.py")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()

    metadata = json.loads(METADATA_FILE.read_text())
    verify_review_state(metadata)
    verify_static_inputs()
    verify_machine_generated_patch()
    verify_no_work_directories("replay start")
    verify_failure_cleanup()
    package_before = {
        path: sha256(path)
        for path in PACKAGE_FILES
    }
    certification_before = {
        path: sha256(path)
        for path in CERTIFICATION_FILES
    }

    replay_work: Path | None = None
    try:
        with tempfile.TemporaryDirectory(
            dir=CAPTURE_DIR,
            prefix=".work-",
        ) as temp_dir:
            replay_work = Path(temp_dir)
            copy_capture_inputs(replay_work)

            red = focused_result(replay_work)
            if red.returncode != 1:
                sys.stdout.write(red.stdout)
                raise SystemExit(
                    "focused test did not produce the required exit-1 red state"
                )
            handle_evidence("focused_red", red, args.record)

            apply_patch(replay_work)

            focused_green = focused_result(replay_work)
            if focused_green.returncode != 0:
                sys.stdout.write(focused_green.stdout)
                raise SystemExit("focused green could not be reproduced")
            handle_evidence(
                "focused_green",
                focused_green,
                args.record,
            )

            broader_green = broader_result(replay_work)
            if broader_green.returncode != 0:
                sys.stdout.write(broader_green.stdout)
                raise SystemExit("broader green could not be reproduced")
            handle_evidence(
                "broader_green",
                broader_green,
                args.record,
            )
    finally:
        if replay_work is not None and replay_work.exists():
            raise SystemExit("replay work directory survived cleanup")
        verify_no_work_directories("replay cleanup")

    final_green = final_package_result()
    if final_green.returncode != 0:
        sys.stdout.write(final_green.stdout)
        raise SystemExit("final package green could not be reproduced")
    handle_evidence(
        "final_package_green",
        final_green,
        args.record,
    )

    for path, before_hash in package_before.items():
        if sha256(path) != before_hash:
            raise SystemExit(f"final package file changed during replay: {path}")
    for path, before_hash in certification_before.items():
        if sha256(path) != before_hash:
            raise SystemExit(
                f"certification file changed during replay: {path}"
            )

    if not args.record:
        current_metadata = json.loads(METADATA_FILE.read_text())
        if current_metadata != metadata:
            raise SystemExit("metadata changed during replay")
        verify_metadata(current_metadata)
        verify_parity_record()
        verify_session_records()

    print("FINAL PACKAGE VERIFIED: local checksums unchanged")
    print("CERTIFICATION FILES VERIFIED: six unchanged")
    print("ORIGIN PROVENANCE VERIFIED: preserved, not executed")
    print("CLEANUP VERIFIED: success and exception paths are clean")
    print("REVIEW STATE VERIFIED: independently reviewed, Pass")
    print("PARITY VERIFIED" if not args.record else "PARITY PENDING RECORD UPDATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
