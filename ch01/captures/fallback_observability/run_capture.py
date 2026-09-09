"""Record or replay the fallback observability capture."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CAPTURE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = CAPTURE_DIR.parents[1]
PACKAGE_APP = PACKAGE_DIR / "app.py"
PACKAGE_REQUIREMENTS = PACKAGE_DIR / "requirements.txt"
BEFORE_DIR = CAPTURE_DIR / "before"
AFTER_APP = CAPTURE_DIR / "after" / "app.py"
WORK_DIR = CAPTURE_DIR / ".work"
FOCUSED_TEST = CAPTURE_DIR / "tests" / "focused_test.py"
BROADER_TEST = CAPTURE_DIR / "tests" / "broader_test.py"
PATCH_PATH = CAPTURE_DIR / "patches" / "production.diff"
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
METADATA_PATH = CAPTURE_DIR / "metadata.json"
REVIEW_ARTIFACT = EVIDENCE_DIR / "independent-review.md"
DOCUMENT_PATHS = {
    "README.md": CAPTURE_DIR / "README.md",
    "parity.md": CAPTURE_DIR / "parity.md",
    "session.md": CAPTURE_DIR / "session.md",
}

EXPECTED_SHA256 = {
    PACKAGE_APP: (
        "924e0b762ae35257f2f0cceb8ca0141053592bc990063990"
        "e14f2e580a9b45b1"
    ),
    PACKAGE_REQUIREMENTS: (
        "efe1c0f6461b461805f7ab37a1f8865890a209800a28b425de981189"
        "c7003807"
    ),
    BEFORE_DIR / "app.py": (
        "666360566a1925279c2e427924c28d53f1cc8045ed3f6a01c"
        "fb157c8f7b2de00"
    ),
    BEFORE_DIR / "requirements.txt": (
        "efe1c0f6461b461805f7ab37a1f8865890a209800a28b425de981189"
        "c7003807"
    ),
    AFTER_APP: (
        "c7a1a70f355ef1762880bd26410852e6e8760c4facc5a256"
        "dc4cd5aa99e04033"
    ),
    FOCUSED_TEST: (
        "8ce91c5b30a70c3970620b541fcb13ae33281be86d8cf346"
        "6979023787ccce13"
    ),
    BROADER_TEST: (
        "2d0ef4e79a4aa4e39406942b1436b4814733a2fce87864df"
        "241e36d1a4eac32e"
    ),
    PATCH_PATH: (
        "ee8b08b09abab2a0b770f85c9ad61aa0a49e311d237c8f84"
        "258727431b8235ab"
    ),
}
EXPECTED_EVIDENCE_SHA256 = {
    EVIDENCE_DIR / "focused-red.txt": (
        "487e7b5f36cdada818ac757dda6063fc67dedf9812f86efa6"
        "734c4c4ea64bf81"
    ),
    EVIDENCE_DIR / "focused-red.exit": (
        "4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9e"
        "e954a27460dd865"
    ),
    EVIDENCE_DIR / "patch-apply.txt": (
        "3fe558f82dd0bc042bb32af4d1a5d9e2a771edac386c07bd7"
        "5d5363b711b0f25"
    ),
    EVIDENCE_DIR / "patch-apply.exit": (
        "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc"
        "94f6f3fe3ab86aa"
    ),
    EVIDENCE_DIR / "focused-green.txt": (
        "00a7b8215359d71b85cefd9f9e8363c2dca02611b3aaa9cfd"
        "8895f46ef66cdf9"
    ),
    EVIDENCE_DIR / "focused-green.exit": (
        "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc"
        "94f6f3fe3ab86aa"
    ),
    EVIDENCE_DIR / "broader-green.txt": (
        "673173a00d4c0eeb22b9be0bca068d76c722fb5b44f930c6"
        "e25f682e6d9c6183"
    ),
    EVIDENCE_DIR / "broader-green.exit": (
        "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc"
        "94f6f3fe3ab86aa"
    ),
    REVIEW_ARTIFACT: (
        "b7579f678ebee383a2d97db1cc8d34e8172fc35c0bed91a5c"
        "4bc7f4fa2509777"
    ),
}

EXPECTED_RED = (
    "FAIL: test_redis_outage_routes_fallback_warning_to_app_logger\n"
    "expected: 1 fallback warning on application logger\n"
    "observed: 0 fallback warnings on application logger\n"
    "neighbor retained: user-1 first 10=200, "
    "11th=429; user-2 first=200\n"
)
EXPECTED_PATCH = "patching file app.py\n"
EXPECTED_FOCUSED_GREEN = (
    "PASS: test_redis_outage_routes_fallback_warning_to_app_logger\n"
    "observed: 1 fallback warning on application logger\n"
    "neighbor retained: user-1 first 10=200, "
    "11th=429; user-2 first=200\n"
)
EXPECTED_BROADER_GREEN = (
    "PASS: test_healthy_storage_emits_no_fallback_warning\n"
    "observed: 0 fallback warnings on application logger\n"
    "neighbor retained: user-1 first 10=200, "
    "11th=429; user-2 first=200\n"
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checksum_value(value, field):
    if not isinstance(value, str):
        raise RuntimeError(f"missing checksum field: {field}")
    return value.removeprefix("sha256:")


def load_metadata():
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def verify_active_review(metadata):
    if metadata.get("session_stage") != (
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
    artifact_path = (CAPTURE_DIR / artifact).resolve()
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


def verify_metadata_checksums(metadata):
    runner_expected = checksum_value(
        metadata.get("runner_checksum"),
        "runner_checksum",
    )
    verify_checksums({Path(__file__).resolve(): runner_expected})

    document_checksums = metadata.get("document_checksums")
    if not isinstance(document_checksums, dict):
        raise RuntimeError("missing document_checksums metadata")
    for relative, path in DOCUMENT_PATHS.items():
        expected = checksum_value(
            document_checksums.get(relative),
            f"document_checksums.{relative}",
        )
        verify_checksums({path: expected})


def verify_checksums(expected_hashes):
    for path, expected in expected_hashes.items():
        if not path.exists():
            raise RuntimeError(f"required file is missing: {path}")
        observed = sha256(path)
        if observed != expected:
            raise RuntimeError(
                f"checksum drift: {path}\n"
                f"expected: {expected}\nobserved: {observed}"
            )


def verify_inputs(check_evidence):
    metadata = load_metadata()
    verify_active_review(metadata)
    verify_metadata_checksums(metadata)
    verify_checksums(EXPECTED_SHA256)
    if check_evidence:
        verify_checksums(EXPECTED_EVIDENCE_SHA256)
    historical_hook = '''def on_limiter_fallback():
    """Emit a fallback warning through the application logger."""
    app.logger.warning("rate limiter entered in-memory fallback")


'''
    expected_package = AFTER_APP.read_text(encoding="utf-8").replace(
        historical_hook,
        "",
    )
    if PACKAGE_APP.read_text(encoding="utf-8") != expected_package:
        raise RuntimeError(
            "package app differs from the reviewed cleanup state"
        )
    if (BEFORE_DIR / "requirements.txt").read_bytes() != (
        PACKAGE_REQUIREMENTS.read_bytes()
    ):
        raise RuntimeError("capture requirements differ from package")

    generated = subprocess.run(
        [
            "diff",
            "-u",
            "--label",
            "a/app.py",
            "--label",
            "b/app.py",
            str(BEFORE_DIR / "app.py"),
            str(AFTER_APP),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if generated.returncode != 1:
        raise RuntimeError("machine diff did not report one change")
    if generated.stdout != PATCH_PATH.read_text(encoding="utf-8"):
        raise RuntimeError("stored patch is not the machine diff")


def run(command, cwd=CAPTURE_DIR):
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def require_result(name, result, expected_exit, expected_output):
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"{name} exit changed: expected {expected_exit}, "
            f"observed {result.returncode}"
        )
    if result.stdout != expected_output:
        raise RuntimeError(
            f"{name} output changed\nobserved:\n{result.stdout}"
        )


def evidence_paths(name):
    return (
        EVIDENCE_DIR / f"{name}.txt",
        EVIDENCE_DIR / f"{name}.exit",
    )


def record_result(name, result):
    output_path, exit_path = evidence_paths(name)
    output_path.write_text(result.stdout, encoding="utf-8")
    exit_path.write_text(f"{result.returncode}\n", encoding="utf-8")


def compare_result(name, result):
    output_path, exit_path = evidence_paths(name)
    if not output_path.exists() or not exit_path.exists():
        raise RuntimeError(
            f"{name} evidence missing; run --record after review"
        )
    if output_path.read_text(encoding="utf-8") != result.stdout:
        raise RuntimeError(f"stored {name} output drifted")
    if exit_path.read_text(encoding="utf-8") != (
        f"{result.returncode}\n"
    ):
        raise RuntimeError(f"stored {name} exit drifted")


def main():
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
        shutil.copytree(BEFORE_DIR, WORK_DIR)
        work_app = WORK_DIR / "app.py"

        red = run([sys.executable, str(FOCUSED_TEST), str(work_app)])
        require_result("focused red", red, 1, EXPECTED_RED)

        patch = run(
            ["patch", "-p1", "-i", str(PATCH_PATH)],
            cwd=WORK_DIR,
        )
        require_result("patch apply", patch, 0, EXPECTED_PATCH)
        if work_app.read_bytes() != AFTER_APP.read_bytes():
            raise RuntimeError("patched work copy differs from after state")

        focused = run(
            [sys.executable, str(FOCUSED_TEST), str(work_app)]
        )
        require_result(
            "focused green", focused, 0, EXPECTED_FOCUSED_GREEN
        )

        broader = run(
            [sys.executable, str(BROADER_TEST), str(work_app)]
        )
        require_result(
            "broader green", broader, 0, EXPECTED_BROADER_GREEN
        )
        verify_inputs(check_evidence=not args.record)

        results = {
            "focused-red": red,
            "patch-apply": patch,
            "focused-green": focused,
            "broader-green": broader,
        }
        if args.record:
            EVIDENCE_DIR.mkdir(exist_ok=True)
            for name, result in results.items():
                record_result(name, result)
            verify_checksums(EXPECTED_EVIDENCE_SHA256)
            mode = "RECORDED"
        else:
            for name, result in results.items():
                compare_result(name, result)
            mode = "VERIFIED"

        print(f"RED {mode}: exit {red.returncode}")
        print(red.stdout, end="")
        print(f"PATCH {mode}: exit {patch.returncode}")
        print(patch.stdout, end="")
        print(f"FOCUSED GREEN {mode}: exit {focused.returncode}")
        print(focused.stdout, end="")
        print(f"BROADER GREEN {mode}: exit {broader.returncode}")
        print(broader.stdout, end="")
        print("PARITY: PATCH, EVIDENCE, AND PACKAGE HASHES MATCH")
        return 0
    finally:
        shutil.rmtree(WORK_DIR, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
