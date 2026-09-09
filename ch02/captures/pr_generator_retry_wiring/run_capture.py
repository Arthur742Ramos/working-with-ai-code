"""Record or replay the complete Chapter 2 retry capture."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CAPTURE_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = CAPTURE_DIR.parents[1]
BEFORE_DIR = CAPTURE_DIR / "before"
AFTER_DIR = CAPTURE_DIR / "after"
WORK_DIR = CAPTURE_DIR / ".work"
PACKAGE_WORK_DIR = CAPTURE_DIR / ".package-work"
TEST_DIR = CAPTURE_DIR / "tests"
PATCH_PATH = (
    CAPTURE_DIR
    / "patches"
    / "pr_generator_retry_wiring.patch"
)
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
RECERTIFICATION_PATH = (
    EVIDENCE_DIR / "final-polish-recertification.json"
)
METADATA_PATH = CAPTURE_DIR / "metadata.json"
PENDING_REVIEW_STAGE = (
    "repairs_applied_pending_independent_review"
)
COMPLETED_REVIEW_STAGE = "complete_independently_reviewed"
GENERATED_RESIDUE_NAMES = {"__pycache__", ".pytest_cache"}

SOURCE_NAMES = (
    "pr_generator.py",
    "schema.py",
    "llm_client.py",
)
EXPECTED_BEFORE = {
    "pr_generator.py": (
        "9fbcd6df24a6ca772f20770b260bb95d94339949f89e4e30c"
        "f193ff9e81ba09f"
    ),
    "schema.py": (
        "e87b7d4428f7af9310967e49bef0d5feea1af8c52d774f798"
        "2671ae13ca8b9b2"
    ),
    "llm_client.py": (
        "a795563c91a9d853d984e5fe7988b9ed17aef454e8ae4381e"
        "936dee32f5a2e56"
    ),
}
EXPECTED_RED = """FAIL: test_cli_retries_after_malformed_json
expected: CLI recovers after malformed JSON on the second chat call
observed: SystemExit: 1 after 1 chat call
stderr: Error: Invalid JSON: Expecting value: line 1 column 1 (char 0)
"""
EXPECTED_FOCUSED_GREEN = """PASS: test_cli_retries_after_malformed_json
observed: CLI succeeded after 2 chat calls
"""
EXPECTED_BROADER_GREEN = """PASS: test_valid_first_response_stays_single_attempt
observed: CLI succeeded after 1 chat call
PASS: test_schema_failure_retries_with_feedback
observed: CLI succeeded after 2 chat calls
PASS: test_retry_exhaustion_stays_bounded
observed: CLI failed after 3 chat calls
3 passed
"""
EXPECTED_CHANGE_LINES = [
    "-            pr = generate_pr_description(diff)",
    "+            pr = generate_with_retry(diff)",
]
COMMANDS = {
    "red": (
        "PYTHONDONTWRITEBYTECODE=1 python3 "
        "tests/focused_test.py .work/pr_generator.py"
    ),
    "focused_green": (
        "PYTHONDONTWRITEBYTECODE=1 python3 "
        "tests/focused_test.py .work/pr_generator.py"
    ),
    "broader_green": (
        "PYTHONDONTWRITEBYTECODE=1 python3 "
        "tests/broader_test.py .work/pr_generator.py"
    ),
}


class CaptureError(RuntimeError):
    """Report an evidence or replay mismatch."""


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_hash(path, expected, label):
    observed = sha256(path)
    if observed != expected:
        raise CaptureError(
            f"{label} checksum drifted: {path.name}\n"
            f"expected: {expected}\n"
            f"observed: {observed}"
        )


def load_metadata():
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def review_artifact_path(review, checksum_field):
    artifact = review.get("artifact_path")
    if not isinstance(artifact, str) or not artifact.strip():
        raise CaptureError("review artifact path is missing")
    if artifact.strip().lower() == "pending":
        raise CaptureError("completed review artifact cannot be pending")
    relative = Path(artifact)
    if relative.is_absolute() or ".." in relative.parts:
        raise CaptureError("review artifact path must be package-local")
    path = (CAPTURE_DIR / relative).resolve()
    if not path.is_relative_to(EVIDENCE_DIR.resolve()):
        raise CaptureError("review artifact must be under evidence/")
    if not path.is_file():
        raise CaptureError(f"review artifact is missing: {artifact}")
    expected = review.get(checksum_field)
    if not isinstance(expected, str) or not expected.strip():
        raise CaptureError("review artifact checksum is missing")
    require_hash(path, expected, "review artifact")
    return path


def verify_first_review(metadata):
    first_review = metadata.get("first_independent_review")
    if not isinstance(first_review, dict):
        raise CaptureError("first independent review is missing")
    if first_review.get("status") != "completed":
        raise CaptureError("first independent review is not completed")
    if first_review.get("verdict") != "Fail":
        raise CaptureError("first independent review must retain Fail")
    if first_review.get("repair_status") != "resolved":
        raise CaptureError("first-review repair status drifted")
    findings = first_review.get("blocking_findings")
    if not isinstance(findings, list) or len(findings) != 3:
        raise CaptureError("first-review finding count drifted")
    review_artifact_path(
        first_review,
        "artifact_checksum_sha256",
    )


def verify_review_state(metadata):
    stage = metadata.get("stage")
    if metadata.get("capture_stage") != stage:
        raise CaptureError("capture stage fields disagree")

    if stage == PENDING_REVIEW_STAGE:
        required = {
            "independent_review_status": "pending",
            "status": "Pending",
        }
        for field, expected in required.items():
            if metadata.get(field) != expected:
                raise CaptureError(
                    "pending repair stage requires "
                    f"{field}={expected!r}"
                )

        first_review = metadata.get("first_independent_review")
        if not isinstance(first_review, dict):
            raise CaptureError("first independent review is missing")
        if first_review.get("status") != "completed":
            raise CaptureError("first independent review is not completed")
        if first_review.get("verdict") != "Fail":
            raise CaptureError("first independent review must retain Fail")
        if first_review.get("repair_status") != (
            "resolved_pending_re_review"
        ):
            raise CaptureError("first-review repair status drifted")
        findings = first_review.get("blocking_findings")
        if not isinstance(findings, list) or len(findings) != 3:
            raise CaptureError("first-review finding count drifted")
        review_artifact_path(
            first_review,
            "artifact_checksum_sha256",
        )

        active = metadata.get("independent_review")
        if not isinstance(active, dict):
            raise CaptureError("active independent review state is missing")
        if active.get("status") != "pending":
            raise CaptureError("active independent review must be pending")
        if active.get("verdict") is not None:
            raise CaptureError("pending review cannot carry a verdict")
        if active.get("artifact_path") != "pending":
            raise CaptureError("pending review cannot carry a receipt")
        return

    if stage == COMPLETED_REVIEW_STAGE:
        required = {
            "independent_review_status": "completed",
            "status": "Pass",
        }
        for field, expected in required.items():
            if metadata.get(field) != expected:
                raise CaptureError(
                    "completed review stage requires "
                    f"{field}={expected!r}"
                )
        verify_first_review(metadata)
        active = metadata.get("independent_review")
        if not isinstance(active, dict):
            raise CaptureError("completed independent review is missing")
        if active.get("status") != "completed":
            raise CaptureError("completed review status drifted")
        if active.get("verdict") != "Pass":
            raise CaptureError("completed review verdict must be Pass")
        if active.get("blocking_findings") != []:
            raise CaptureError("completed Pass review has blocking findings")
        if active.get("non_blocking_findings") != []:
            raise CaptureError(
                "completed Pass review has non-blocking findings"
            )
        review_artifact_path(
            active,
            "artifact_checksum_sha256",
        )
        return

    raise CaptureError(f"unsupported capture stage: {stage!r}")


def cleanup_work():
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    shutil.rmtree(PACKAGE_WORK_DIR, ignore_errors=True)


def verify_no_generated_residue():
    residue = []
    for path in PACKAGE_ROOT.rglob("*"):
        if path.name in GENERATED_RESIDUE_NAMES:
            residue.append(path)
        elif path.is_file() and path.suffix == ".pyc":
            residue.append(path)
    if residue:
        relative = sorted(
            str(path.relative_to(PACKAGE_ROOT)) for path in residue
        )
        raise CaptureError(
            "generated package residue is present: "
            + ", ".join(relative)
        )
    if WORK_DIR.exists() or PACKAGE_WORK_DIR.exists():
        raise CaptureError("capture working directories were not removed")


def verify_origin(metadata):
    origin = metadata["origin_support_checksums"]
    for name, expected in EXPECTED_BEFORE.items():
        require_hash(
            BEFORE_DIR / name,
            expected,
            "before fixture",
        )
        recorded = metadata["before_fixture_checksums"][
            f"before/{name}"
        ]
        if recorded != expected:
            raise CaptureError(
                f"metadata before checksum drifted: {name}"
            )
        if origin[f"code/ch02/{name}"] != expected:
            raise CaptureError(
                f"origin support checksum drifted: {name}"
            )

    chapter = metadata["origin_chapter_checksums"]
    if chapter["before"] != chapter["after"]:
        raise CaptureError(
            "origin chapter provenance is inconsistent"
        )


def verify_package(metadata):
    checksums = metadata["package_support_checksums"]
    for relative, expected in checksums.items():
        require_hash(
            PACKAGE_ROOT / relative,
            expected,
            "package support",
        )
    if (PACKAGE_ROOT / "llm_client.py").exists():
        raise CaptureError(
            "stale top-level llm_client.py is still present"
        )


def verify_final_polish_recertification(metadata):
    record = metadata.get("final_polish_recertification")
    if not isinstance(record, dict):
        raise CaptureError("final-polish recertification is missing")
    if record.get("status") != "Pass":
        raise CaptureError("final-polish recertification must Pass")
    if record.get("test_count") != 18:
        raise CaptureError("final-polish test count drifted")
    require_hash(
        RECERTIFICATION_PATH,
        record.get("checksum_sha256"),
        "final-polish recertification",
    )
    receipt = json.loads(
        RECERTIFICATION_PATH.read_text(encoding="utf-8")
    )
    if receipt.get("status") != "Pass":
        raise CaptureError("final-polish receipt does not Pass")
    if receipt.get("test_count") != 18:
        raise CaptureError("final-polish receipt test count drifted")
    for relative, expected in receipt["support_checksums"].items():
        require_hash(
            PACKAGE_ROOT / relative,
            expected,
            "recertified support",
        )
    for relative, expected in receipt["historical_checksums"].items():
        require_hash(
            CAPTURE_DIR / relative,
            expected,
            "preserved historical artifact",
        )


def verify_after_and_patch(metadata):
    for name in SOURCE_NAMES:
        expected = metadata["after_fixture_checksums"][
            f"after/{name}"
        ]
        require_hash(AFTER_DIR / name, expected, "after fixture")

    for name in ("schema.py", "llm_client.py"):
        if (BEFORE_DIR / name).read_bytes() != (
            AFTER_DIR / name
        ).read_bytes():
            raise CaptureError(
                f"non-target after file changed: {name}"
            )

    require_hash(
        PATCH_PATH,
        metadata["patch"]["checksum"],
        "patch",
    )
    changed = [
        line
        for line in PATCH_PATH.read_text(
            encoding="utf-8"
        ).splitlines()
        if (
            line.startswith(("+", "-"))
            and not line.startswith(("+++", "---"))
        )
    ]
    if changed != EXPECTED_CHANGE_LINES:
        raise CaptureError(
            "patch is not the approved one-line substitution"
        )


def verify_tests(metadata):
    for name in ("focused_test.py", "broader_test.py"):
        expected = metadata["test_checksums"][f"tests/{name}"]
        require_hash(TEST_DIR / name, expected, "capture test")


def run_test(test_name):
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            str(TEST_DIR / test_name),
            str(WORK_DIR / "pr_generator.py"),
        ],
        cwd=CAPTURE_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def reset_work():
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    shutil.copytree(BEFORE_DIR, WORK_DIR)


def apply_patch_and_verify():
    completed = subprocess.run(
        [
            "patch",
            "-s",
            "-p1",
            "-i",
            str(PATCH_PATH),
        ],
        cwd=WORK_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise CaptureError(
            "stored patch did not apply cleanly\n"
            f"{completed.stdout}"
        )
    for name in SOURCE_NAMES:
        if (WORK_DIR / name).read_bytes() != (
            AFTER_DIR / name
        ).read_bytes():
            raise CaptureError(
                f"recreated after state drifted: {name}"
            )


def require_result(label, code, output, expected_code,
                   expected_output):
    if code != expected_code or output != expected_output:
        raise CaptureError(
            f"{label} changed\n"
            f"expected exit: {expected_code}\n"
            f"observed exit: {code}\n"
            f"observed output:\n{output}"
        )


def evidence_paths(label):
    return (
        EVIDENCE_DIR / f"{label}.txt",
        EVIDENCE_DIR / f"{label}.exit",
    )


def record_evidence(label, code, output):
    output_path, exit_path = evidence_paths(label)
    output_path.write_text(output, encoding="utf-8")
    exit_path.write_text(f"{code}\n", encoding="utf-8")


def compare_evidence(label, code, output, metadata):
    output_path, exit_path = evidence_paths(label)
    if output_path.read_text(encoding="utf-8") != output:
        raise CaptureError(f"stored {label} output drifted")
    if int(exit_path.read_text(encoding="utf-8")) != code:
        raise CaptureError(f"stored {label} exit drifted")
    metadata_key = {
        "focused-red": "red",
        "focused-green": "focused_green",
        "broader-green": "broader_green",
    }[label]
    record = metadata[metadata_key]
    require_hash(
        output_path,
        record["output_checksum"],
        f"{label} output",
    )
    require_hash(
        exit_path,
        record["exit_file_checksum"],
        f"{label} exit",
    )


def verify_metadata(metadata):
    verify_review_state(metadata)
    if not metadata["production_repair_applied"]:
        raise CaptureError(
            "metadata does not record the captured repair"
        )
    expected_statuses = {
        "red": 1,
        "focused_green": 0,
        "broader_green": 0,
    }
    for key, expected_status in expected_statuses.items():
        record = metadata[key]
        if record["command"] != COMMANDS[key]:
            raise CaptureError(f"metadata command drifted: {key}")
        if record["exit_status"] != expected_status:
            raise CaptureError(f"metadata status drifted: {key}")


def verify_records(metadata):
    required = {
        "README.md": (
            "Human-owned policy boundary",
            "Non-recording replay",
            ".package-work/",
            "first-independent-review.md",
            "independent-review.md",
            "complete_independently_reviewed",
            "final-polish-recertification.json",
        ),
        "session.md": (
            "Approval basis",
            "Agent action record",
            "Exact applied diff",
            "Agent evidence boundary",
            "Post-capture first-review repair",
        ),
        "parity.md": (
            "focused-green.txt",
            "broader-green.txt",
            "pr_generator_retry_wiring.patch",
            "Promoted chapter implementation",
            "first-independent-review.md",
            "independent-review.md",
            "final-polish-recertification.json",
            "Review-state gate",
            "Cleanup gate",
        ),
        "evidence/agent-actions.md": (
            "Replayed the focused red state",
            "Generated the unified diff",
        ),
    }
    for relative, tokens in required.items():
        path = CAPTURE_DIR / relative
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                raise CaptureError(
                    f"record is incomplete: {relative}: {token}"
                )

    action_path = EVIDENCE_DIR / "agent-actions.md"
    require_hash(
        action_path,
        metadata["agent_action_record"]["checksum"],
        "agent action record",
    )
    require_hash(
        CAPTURE_DIR / "run_capture.py",
        metadata["runner"]["checksum"],
        "runner",
    )
    for name in ("README.md", "session.md", "parity.md"):
        require_hash(
            CAPTURE_DIR / name,
            metadata["record_checksums"][name],
            "package record",
        )


def package_copy_ignore(_directory, names):
    ignored = {
        "__pycache__",
        ".pytest_cache",
        ".work",
        ".package-work",
        "pr_description.json",
    }
    return [name for name in names if name in ignored]


def run_isolated_package_tests():
    shutil.rmtree(PACKAGE_WORK_DIR, ignore_errors=True)
    shutil.copytree(
        PACKAGE_ROOT,
        PACKAGE_WORK_DIR,
        ignore=package_copy_ignore,
    )
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONNOUSERSITE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            "-B",
            "-c",
            (
                "import runpy, sys; "
                "sys.path.insert(0, '.'); "
                "runpy.run_path('test_pr_generator.py', "
                "run_name='__main__')"
            ),
        ],
        cwd=PACKAGE_WORK_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise CaptureError(
            "isolated package tests failed\n"
            f"{completed.stdout}"
        )
    if "Ran 18 tests" not in completed.stdout:
        raise CaptureError(
            "isolated package suite did not run all 18 tests\n"
            f"{completed.stdout}"
        )
    return completed.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="refresh verified capture evidence after review",
    )
    args = parser.parse_args()
    metadata = load_metadata()

    cleanup_work()
    verify_no_generated_residue()
    try:
        verify_metadata(metadata)
        verify_origin(metadata)
        verify_package(metadata)
        verify_final_polish_recertification(metadata)
        verify_after_and_patch(metadata)
        verify_tests(metadata)
        verify_records(metadata)

        reset_work()
        red_code, red_output = run_test("focused_test.py")
        require_result(
            "focused red",
            red_code,
            red_output,
            1,
            EXPECTED_RED,
        )

        apply_patch_and_verify()
        focused_code, focused_output = run_test(
            "focused_test.py"
        )
        require_result(
            "focused green",
            focused_code,
            focused_output,
            0,
            EXPECTED_FOCUSED_GREEN,
        )
        broader_code, broader_output = run_test(
            "broader_test.py"
        )
        require_result(
            "broader green",
            broader_code,
            broader_output,
            0,
            EXPECTED_BROADER_GREEN,
        )

        results = (
            ("focused-red", red_code, red_output),
            ("focused-green", focused_code, focused_output),
            ("broader-green", broader_code, broader_output),
        )
        if args.record:
            for label, code, output in results:
                record_evidence(label, code, output)
        for label, code, output in results:
            compare_evidence(
                label,
                code,
                output,
                metadata,
            )

        package_code = run_isolated_package_tests()
        verify_origin(metadata)
        verify_package(metadata)
        cleanup_work()
        verify_no_generated_residue()
        print(f"RED EXIT: {red_code}")
        print("PATCH STATUS: exact one-line patch applied")
        print(f"FOCUSED GREEN EXIT: {focused_code}")
        print(f"BROADER GREEN EXIT: {broader_code}")
        print(f"PACKAGE GREEN EXIT: {package_code}")
        print("REVIEW STATUS: completed independent review; verdict Pass")
        print("CLEANUP STATUS: no generated residue")
        print("PARITY STATUS: package-local records match")
        return 0
    finally:
        cleanup_work()


if __name__ == "__main__":
    raise SystemExit(main())
