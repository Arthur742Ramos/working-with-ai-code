"""Record or replay the orphan-product policy capture."""
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
TEST_DIR = CAPTURE_DIR / "tests"
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
PATCH_PATH = (
    CAPTURE_DIR
    / "patches"
    / "missing-product-policy.diff"
)
METADATA_PATH = CAPTURE_DIR / "metadata.json"
PARITY_PATH = CAPTURE_DIR / "parity.md"
PUBLICATION_PATH = CAPTURE_DIR / "chapter-session.md"
REVIEW_ARTIFACT_RELATIVE = "evidence/independent-review.md"
REVIEW_ARTIFACT_PATH = CAPTURE_DIR / REVIEW_ARTIFACT_RELATIVE
WORK_DIR = CAPTURE_DIR / ".work"
FINAL_WORK_DIR = WORK_DIR / "final-package"
FINAL_SERVER = PACKAGE_ROOT / "server.py"
FINAL_SEED = PACKAGE_ROOT / "seed.py"
FINAL_TEST_DIR = PACKAGE_ROOT / "tests"
PACKAGE_DOCUMENTS = (
    "README.md",
    "session.md",
    "parity.md",
    "patches/README.md",
    "chapter-session.md",
)
EXPECTED_BEFORE_SHA256 = {
    "server.py": (
        "c1db53308867ffe7d4e5123f5295630e"
        "e758f3cd7dfd67d9712fec6545fdd9f4"
    ),
    "seed.py": (
        "725779b8202a0a2ef77ea6e089153e36"
        "d995215cfcf310f07a54c4e6b3bc27b3"
    ),
}
EXPECTED_FINAL_SHA256 = {
    "server.py": (
        "1fc1fc84d1cd04aa51580232d21bdba8"
        "5d62569a108e460b263c0fd475c10937"
    ),
    "seed.py": EXPECTED_BEFORE_SHA256["seed.py"],
}
EXPECTED_TEST_SHA256 = {
    "test_orphan_policy.py": (
        "22e9b50365e2fb9e34c3a8098b66d48e"
        "cbd29f73da0c05a0918a0766bdfb5c60"
    ),
    "test_orphan_policy_broader.py": (
        "ab66761982ce85c4c5b3d6705233a9d7"
        "d7c5d33815a2e121f2176a83433658da"
    ),
}
EXPECTED_PATCH_SHA256 = (
    "8d60f09a62115a6ec83da53e60c2fd7a"
    "164333af14841ea60c0b81ea557c3a84"
)
EXPECTED_PUBLICATION_SHA256 = (
    "1f3671006cd53578851f1d16910976704"
    "f2bcdd81a9e5ab29878efb4677b7506"
)
EVIDENCE_NAMES = (
    "focused-red.txt",
    "focused-red.exitstatus",
    "focused-green.txt",
    "focused-green.exitstatus",
    "broader-green.txt",
    "broader-green.exitstatus",
)
PENDING_REVIEW_STAGE = "complete_red_patch_green_replay"
COMPLETED_REVIEW_STAGE = "complete_independently_reviewed"
RUNTIME_FILE_NAMES = {"shop.db", "server.log"}
RUNTIME_DIR_NAMES = {".work", ".pytest_cache", "__pycache__"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_checksum(path, expected):
    if not path.exists():
        raise RuntimeError(f"required file is missing: {path}")
    observed = sha256(path)
    if observed != expected:
        raise RuntimeError(
            f"checksum drift: {path}\n"
            f"expected: {expected}\n"
            f"observed: {observed}"
        )


def load_metadata():
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def checksum_value(value, field):
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"missing checksum field: {field}")
    return value.removeprefix("sha256:")


def verify_review_state(metadata):
    stage = metadata.get("capture_stage")
    review_status = metadata.get("independent_review_status")
    package_status = metadata.get("status")
    review = metadata.get("independent_review")

    if stage == PENDING_REVIEW_STAGE:
        if review_status != "pending" or package_status != "Pending":
            raise RuntimeError(
                "pending review stage requires pending package state"
            )
        if not isinstance(review, dict):
            raise RuntimeError(
                "pending review stage requires independent_review metadata"
            )
        expected = {
            "status": "pending",
            "verdict": "Pending",
            "artifact": "pending",
        }
        for field, value in expected.items():
            if review.get(field) != value:
                raise RuntimeError(
                    "pending review stage requires "
                    f"independent_review.{field}={value!r}"
                )
        return

    if stage != COMPLETED_REVIEW_STAGE:
        raise RuntimeError(f"unknown capture review stage: {stage!r}")
    if review_status != "completed" or package_status != "Pass":
        raise RuntimeError(
            "completed review stage requires completed / Pass state"
        )
    if not isinstance(review, dict):
        raise RuntimeError(
            "completed review stage requires independent_review metadata"
        )
    if review.get("status") != "completed":
        raise RuntimeError(
            "completed review stage requires active review status completed"
        )
    if review.get("verdict") != "Pass":
        raise RuntimeError(
            "completed review stage requires active verdict Pass"
        )

    artifact = review.get("artifact_path")
    if artifact != REVIEW_ARTIFACT_RELATIVE:
        raise RuntimeError(
            "completed review stage requires active artifact "
            f"{REVIEW_ARTIFACT_RELATIVE!r}"
        )
    artifact_path = (CAPTURE_DIR / artifact).resolve()
    if not artifact_path.is_relative_to(EVIDENCE_DIR.resolve()):
        raise RuntimeError("review artifact must be under evidence/")
    if not artifact_path.is_file():
        raise RuntimeError(
            f"completed review artifact is missing: {artifact_path}"
        )
    expected = checksum_value(
        review.get("artifact_checksum_sha256"),
        "independent_review.artifact_checksum_sha256",
    )
    observed = sha256(artifact_path)
    if observed != expected:
        raise RuntimeError(
            "independent review artifact checksum drift\n"
            f"expected: {expected}\nobserved: {observed}"
        )

    attribution_fields = (
        "reviewer_role",
        "reviewer_tool",
        "review_date",
    )
    for field in attribution_fields:
        value = review.get(field)
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(
                "completed review stage requires attributable field "
                f"independent_review.{field}"
            )

    receipt = artifact_path.read_text(encoding="utf-8")
    required_receipt_lines = (
        "Verdict: **PASS**",
        f"- Reviewer role: {review['reviewer_role']}",
        f"- Reviewer tool: {review['reviewer_tool']}",
        f"- Review date: {review['review_date']}",
    )
    for line in required_receipt_lines:
        if line not in receipt:
            raise RuntimeError(
                "independent review artifact contradicts active metadata: "
                f"missing {line!r}"
            )


def is_runtime_path(path):
    relative = path.relative_to(PACKAGE_ROOT)
    return (
        path.name in RUNTIME_FILE_NAMES
        or path.suffix == ".pyc"
        or any(part in RUNTIME_DIR_NAMES for part in relative.parts)
    )


def maintained_package_files():
    return sorted(
        path
        for path in PACKAGE_ROOT.rglob("*")
        if path.is_file() and not is_runtime_path(path)
    )


def verify_package_inventory(metadata):
    expected = metadata.get("package_inventory")
    if not isinstance(expected, list) or not all(
        isinstance(item, str) for item in expected
    ):
        raise RuntimeError("missing package_inventory metadata")
    if expected != sorted(expected) or len(expected) != len(set(expected)):
        raise RuntimeError("package_inventory must be sorted and unique")
    observed = [
        path.relative_to(PACKAGE_ROOT).as_posix()
        for path in maintained_package_files()
    ]
    if observed != expected:
        raise RuntimeError(
            "maintained package inventory drift\n"
            f"expected: {expected}\nobserved: {observed}"
        )


def runtime_residue():
    return sorted(
        path
        for path in PACKAGE_ROOT.rglob("*")
        if is_runtime_path(path)
    )


def cleanup_runtime_residue():
    for path in reversed(runtime_residue()):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
    remaining = runtime_residue()
    if remaining:
        rendered = ", ".join(
            path.relative_to(PACKAGE_ROOT).as_posix()
            for path in remaining
        )
        raise RuntimeError(f"runtime residue cleanup failed: {rendered}")


def verify_sources(metadata):
    verify_review_state(metadata)
    verify_package_inventory(metadata)

    for name, expected in EXPECTED_BEFORE_SHA256.items():
        require_checksum(BEFORE_DIR / name, expected)

    for name, expected in EXPECTED_FINAL_SHA256.items():
        require_checksum(PACKAGE_ROOT / name, expected)

    for name, expected in EXPECTED_TEST_SHA256.items():
        capture_test = TEST_DIR / name
        final_test = FINAL_TEST_DIR / name
        require_checksum(capture_test, expected)
        require_checksum(final_test, expected)
        if capture_test.read_bytes() != final_test.read_bytes():
            raise RuntimeError(f"capture and final test drift: {name}")

    if (BEFORE_DIR / "seed.py").read_bytes() != FINAL_SEED.read_bytes():
        raise RuntimeError("final seed drifted from the incident fixture")

    require_checksum(PATCH_PATH, EXPECTED_PATCH_SHA256)
    require_checksum(
        PUBLICATION_PATH,
        EXPECTED_PUBLICATION_SHA256,
    )

    expected_final = metadata["final_package_sha256"]
    for relative, expected in expected_final.items():
        require_checksum(PACKAGE_ROOT / relative, expected)

    publication = metadata["publication_surface"]
    if publication["sha256"] != EXPECTED_PUBLICATION_SHA256:
        raise RuntimeError("publication metadata checksum drift")


def verify_stored_artifacts(metadata):
    if metadata["runner_sha256"] != sha256(Path(__file__)):
        raise RuntimeError("runner checksum drift")
    if metadata["patch_sha256"] != EXPECTED_PATCH_SHA256:
        raise RuntimeError("metadata patch checksum drift")
    for name in EVIDENCE_NAMES:
        expected = metadata["evidence_sha256"][name]
        require_checksum(EVIDENCE_DIR / name, expected)
    require_checksum(
        PARITY_PATH,
        metadata["parity_sha256"],
    )
    for relative in PACKAGE_DOCUMENTS:
        require_checksum(
            CAPTURE_DIR / relative,
            metadata["package_document_sha256"][relative],
        )


def prepare_work():
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    WORK_DIR.mkdir()
    for name in EXPECTED_BEFORE_SHA256:
        shutil.copy2(BEFORE_DIR / name, WORK_DIR / name)


def prepare_final_work():
    FINAL_WORK_DIR.mkdir()
    shutil.copy2(FINAL_SERVER, FINAL_WORK_DIR / "server.py")
    shutil.copy2(FINAL_SEED, FINAL_WORK_DIR / "seed.py")
    shutil.copytree(FINAL_TEST_DIR, FINAL_WORK_DIR / "tests")


def run_test(test_dir, name, work_dir=None, cwd=PACKAGE_ROOT):
    command = [sys.executable, str(test_dir / name)]
    if work_dir is not None:
        command.append(str(work_dir))
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def write_result(stem, exit_status, output):
    EVIDENCE_DIR.mkdir(exist_ok=True)
    (EVIDENCE_DIR / f"{stem}.txt").write_text(
        output,
        encoding="utf-8",
    )
    (EVIDENCE_DIR / f"{stem}.exitstatus").write_text(
        f"{exit_status}\n",
        encoding="utf-8",
    )


def compare_result(stem, exit_status, output):
    stored_output = (
        EVIDENCE_DIR / f"{stem}.txt"
    ).read_text(encoding="utf-8")
    stored_status = int(
        (EVIDENCE_DIR / f"{stem}.exitstatus")
        .read_text(encoding="utf-8")
        .strip()
    )
    if output != stored_output:
        raise RuntimeError(f"stored {stem} output changed")
    if exit_status != stored_status:
        raise RuntimeError(f"stored {stem} exit status changed")


def preserve_result(record, stem, exit_status, output):
    if record:
        write_result(stem, exit_status, output)
    else:
        compare_result(stem, exit_status, output)


def apply_patch():
    completed = subprocess.run(
        ["patch", "-p1", "-i", str(PATCH_PATH)],
        cwd=WORK_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "stored patch did not apply cleanly\n"
            + completed.stdout
        )


def generated_diff(after_path):
    completed = subprocess.run(
        [
            "diff",
            "-u",
            "--label",
            "a/server.py",
            "--label",
            "b/server.py",
            str(BEFORE_DIR / "server.py"),
            str(after_path),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 1:
        raise RuntimeError(
            "working diff was missing or diff failed\n"
            + completed.stdout
        )
    return completed.stdout


def require_exit(label, observed, expected, output):
    if observed != expected:
        raise RuntimeError(
            f"{label} exit status changed\n"
            f"expected: {expected}\n"
            f"observed: {observed}\n"
            f"output:\n{output}"
        )


def require_matching_result(label, left, right):
    if left != right:
        raise RuntimeError(f"{label} output or status drifted")


def reproduce(record):
    cleanup_runtime_residue()
    try:
        _reproduce(record)
    finally:
        shutil.rmtree(WORK_DIR, ignore_errors=True)
        cleanup_runtime_residue()


def _reproduce(record):
    metadata = load_metadata()
    verify_sources(metadata)
    if not record:
        verify_stored_artifacts(metadata)

    package_before = {
        path: sha256(path)
        for path in maintained_package_files()
        if not (record and path.is_relative_to(EVIDENCE_DIR))
    }

    prepare_work()
    try:
        red = run_test(
            TEST_DIR,
            "test_orphan_policy.py",
            WORK_DIR,
        )
        red_status, red_output = red
        require_exit("focused red", red_status, 1, red_output)
        preserve_result(
            record,
            "focused-red",
            red_status,
            red_output,
        )

        apply_patch()
        require_checksum(
            WORK_DIR / "server.py",
            EXPECTED_FINAL_SHA256["server.py"],
        )
        observed_diff = generated_diff(WORK_DIR / "server.py")
        stored_diff = PATCH_PATH.read_text(encoding="utf-8")
        if observed_diff != stored_diff:
            raise RuntimeError("machine-generated patch changed")
        if (WORK_DIR / "server.py").read_bytes() != FINAL_SERVER.read_bytes():
            raise RuntimeError("patched server differs from final package")

        focused = run_test(
            TEST_DIR,
            "test_orphan_policy.py",
            WORK_DIR,
        )
        focused_status, focused_output = focused
        require_exit(
            "focused green",
            focused_status,
            0,
            focused_output,
        )
        preserve_result(
            record,
            "focused-green",
            focused_status,
            focused_output,
        )

        broader = run_test(
            TEST_DIR,
            "test_orphan_policy_broader.py",
            WORK_DIR,
        )
        broader_status, broader_output = broader
        require_exit(
            "broader green",
            broader_status,
            0,
            broader_output,
        )
        preserve_result(
            record,
            "broader-green",
            broader_status,
            broader_output,
        )

        prepare_final_work()
        final_test_dir = FINAL_WORK_DIR / "tests"
        final_focused = run_test(
            final_test_dir,
            "test_orphan_policy.py",
            cwd=FINAL_WORK_DIR,
        )
        final_broader = run_test(
            final_test_dir,
            "test_orphan_policy_broader.py",
            cwd=FINAL_WORK_DIR,
        )
        require_exit(
            "final focused green",
            final_focused[0],
            0,
            final_focused[1],
        )
        require_exit(
            "final broader green",
            final_broader[0],
            0,
            final_broader[1],
        )
        require_matching_result(
            "focused capture-to-final",
            focused,
            final_focused,
        )
        require_matching_result(
            "broader capture-to-final",
            broader,
            final_broader,
        )

        verify_sources(metadata)
        package_after = {
            path: sha256(path) for path in package_before
        }
        if package_before != package_after:
            raise RuntimeError("final package changed during replay")
    finally:
        shutil.rmtree(WORK_DIR, ignore_errors=True)

    print("RED")
    print(red_output, end="")
    print(f"EXIT STATUS: {red_status}")
    print("PATCH STATUS: exact stored diff applied")
    print("FOCUSED GREEN")
    print(focused_output, end="")
    print(f"EXIT STATUS: {focused_status}")
    print("BROADER GREEN")
    print(broader_output, end="")
    print(f"EXIT STATUS: {broader_status}")
    print("FINAL PACKAGE GREEN: focused and broader checks passed")
    print(
        "FINAL PACKAGE STATUS: inventory and checksums verified unchanged"
    )
    if record:
        print("PARITY STATUS: record replay complete; run default replay")
    else:
        print("PARITY STATUS: checksum verified")
    print("INDEPENDENT REVIEW: completed Pass receipt verified")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="recreate red and green evidence",
    )
    args = parser.parse_args()
    reproduce(args.record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
