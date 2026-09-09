"""Record or replay the Boolean-as-integer role-handoff capture."""

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

CAPTURE_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = CAPTURE_DIR.parents[1]
BEFORE_PATH = CAPTURE_DIR / "before" / "validator.py"
FOCUSED_TEST = (
    CAPTURE_DIR
    / "tests"
    / "test_bool_is_not_accepted_as_int.py"
)
REVIEW_PATH_TEST = (
    CAPTURE_DIR
    / "tests"
    / "test_review_artifact_path.py"
)
PATCH_PATH = CAPTURE_DIR / "patches" / "strict-int.patch"
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
RED_OUTPUT_PATH = EVIDENCE_DIR / "focused-red.txt"
RED_STATUS_PATH = EVIDENCE_DIR / "focused-red.exit-status"
FOCUSED_GREEN_OUTPUT_PATH = EVIDENCE_DIR / "focused-green.txt"
FOCUSED_GREEN_STATUS_PATH = (
    EVIDENCE_DIR / "focused-green.exit-status"
)
BROADER_GREEN_OUTPUT_PATH = EVIDENCE_DIR / "broader-green.txt"
BROADER_GREEN_STATUS_PATH = (
    EVIDENCE_DIR / "broader-green.exit-status"
)
METADATA_PATH = CAPTURE_DIR / "metadata.json"
RUNNER_PATH = CAPTURE_DIR / "run_capture.py"
WORK_DIR = CAPTURE_DIR / ".work"
WORK_PATH = WORK_DIR / "validator.py"
WORK_BROADER_TEST = WORK_DIR / "test_validator.py"
COMPLETED_REVIEW_STAGE = "complete_independently_reviewed"
FINAL_SOURCE = PACKAGE_ROOT / "validator.py"
FINAL_TEST = PACKAGE_ROOT / "test_validator.py"
FINAL_FOCUSED_TEST = (
    PACKAGE_ROOT / "test_bool_is_not_accepted_as_int.py"
)
FINAL_CLI = PACKAGE_ROOT / "cli.py"
FINAL_SCHEMA = PACKAGE_ROOT / "schema.json"
FINAL_CONFIG = PACKAGE_ROOT / "config.json"
FINAL_INVALID_CONFIG = PACKAGE_ROOT / "invalid_config.json"
PYTEST_CONFIG = PACKAGE_ROOT / "pytest.ini"
PACKAGE_SUPPORT_PATHS = (
    FINAL_SOURCE,
    FINAL_TEST,
    FINAL_FOCUSED_TEST,
    FINAL_CLI,
    FINAL_SCHEMA,
    FINAL_CONFIG,
    FINAL_INVALID_CONFIG,
    PYTEST_CONFIG,
)

EXPECTED_BASELINE_CHECKSUMS = {
    BEFORE_PATH: (
        "a4b2a26cb36e225ef3bd246e63072b5d"
        "fa84a5c781b48ad94fdd36c83f7faa5b"
    ),
    FOCUSED_TEST: (
        "60cf0c94bec0abb3a5899c4ea1c8e62e"
        "a762eb891c067e23b59cc19b8f0f4364"
    ),
    REVIEW_PATH_TEST: (
        "ba10ae54ceef26ee1a0d570fe988241f2"
        "6ad0d1929fedbce1c1979a4f16a3f54"
    ),
    FINAL_SOURCE: (
        "a3f749380fdf05dadf128190ec4b03b7"
        "76ada720b7d9b2ef5679d112da04ce10"
    ),
    FINAL_TEST: (
        "032c04880464b3dfbe59568b189004a19"
        "77f1ce55a7e51bd1e16a401ef15de9d"
    ),
    FINAL_FOCUSED_TEST: (
        "c48d3e2788a0fb3ee49aa7a7c0578c1"
        "adc196fd021f797665328a78566164ff8"
    ),
    FINAL_CLI: (
        "382da48431ac6cc869d024a138635380c"
        "12f1cc3b39acceccfe4485430385efc"
    ),
    FINAL_SCHEMA: (
        "0d75c5fdf197e324535d4721c7d91a10"
        "ccec0f77e5af86be0ff6b670be3ae24e"
    ),
    FINAL_CONFIG: (
        "a54bf8fbe745d74053f21557ff1048451"
        "78bbeac3264fcd50addfd1a730f599f"
    ),
    FINAL_INVALID_CONFIG: (
        "64e395a2596a58feecfb6b04c9137ae4"
        "764bc1c0f3a2eb333475bde6e7e3d74a"
    ),
    PYTEST_CONFIG: (
        "8b4b211e3e0c79dbbdc503bd4b1f39d1"
        "08e2115415eb4da47d56b381e5d2671a"
    ),
}
EXPECTED_RED = (
    "FAIL: test_bool_is_not_accepted_as_int\n"
    "expected: port: expected int\n"
    "observed: no validation errors; True was accepted\n"
)
EXPECTED_FOCUSED_GREEN = (
    "PASS: test_bool_is_not_accepted_as_int\n"
    "observed: port: expected int\n"
)
OLD_PREDICATE = '"int": lambda value: isinstance(value, int),'
NEW_PREDICATE = '"int": lambda value: type(value) is int,'


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_work_dir():
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    if WORK_DIR.exists():
        raise RuntimeError("disposable work directory was not removed")


def load_metadata():
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def verify_review_state(metadata):
    if metadata.get("capture_stage") != COMPLETED_REVIEW_STAGE:
        return

    review = metadata.get("independent_review")
    if not isinstance(review, dict):
        raise RuntimeError(
            "completed independent review metadata is missing"
        )
    if review.get("status") != "completed":
        raise RuntimeError(
            "completed package has no completed active review"
        )
    if review.get("verdict") != "Pass":
        raise RuntimeError(
            "completed package has no Pass review verdict"
        )

    artifact_path = review.get("artifact_path")
    artifact_checksum = review.get("artifact_checksum")
    if not isinstance(artifact_path, str) or not artifact_path:
        raise RuntimeError(
            "completed package has no review artifact path"
        )
    relative_path = Path(artifact_path)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise RuntimeError("review artifact path must be package-local")
    if (
        not isinstance(artifact_checksum, str)
        or not artifact_checksum.startswith("sha256:")
    ):
        raise RuntimeError(
            "completed package has no valid review artifact checksum"
        )

    capture_root = CAPTURE_DIR.resolve()
    evidence_root = EVIDENCE_DIR.resolve()
    if not evidence_root.is_relative_to(capture_root):
        raise RuntimeError(
            "evidence directory must resolve under capture package"
        )

    artifact = (CAPTURE_DIR / relative_path).resolve()
    if not artifact.is_relative_to(evidence_root):
        raise RuntimeError("review artifact must be under evidence/")
    if not artifact.is_file():
        raise RuntimeError(
            f"completed review artifact is missing: {artifact_path}"
        )
    expected = artifact_checksum.removeprefix("sha256:")
    observed = checksum(artifact)
    if observed != expected:
        raise RuntimeError(
            f"review artifact checksum drift: {artifact}\n"
            f"expected: {expected}\n"
            f"observed: {observed}"
        )


def verify_baseline_checksums():
    for path, expected in EXPECTED_BASELINE_CHECKSUMS.items():
        observed = checksum(path)
        if observed != expected:
            raise RuntimeError(
                f"checksum drift: {path}\n"
                f"expected: {expected}\n"
                f"observed: {observed}"
            )


def run_command(command, cwd):
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def run_focused_test():
    return run_command(
        [sys.executable, str(FOCUSED_TEST), str(WORK_PATH)],
        CAPTURE_DIR,
    )


def normalize_broader_output(output):
    without_color = re.sub(r"\x1b\[[0-9;]*m", "", output)
    return re.sub(r" in \d+\.\d+s", " in <TIME>s", without_color)


def run_broader_test():
    status, output = run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "test_validator.py",
        ],
        WORK_DIR,
    )
    return status, normalize_broader_output(output)


def apply_smallest_edit():
    before_text = WORK_PATH.read_text(encoding="utf-8")
    if before_text.count(OLD_PREDICATE) != 1:
        raise RuntimeError("strict integer predicate is not unique")
    after_text = before_text.replace(OLD_PREDICATE, NEW_PREDICATE)
    WORK_PATH.write_text(after_text, encoding="utf-8")
    return before_text, after_text


def generate_patch(before_text, after_text):
    return "".join(
        difflib.unified_diff(
            before_text.splitlines(keepends=True),
            after_text.splitlines(keepends=True),
            fromfile="before/validator.py",
            tofile="after/validator.py",
        )
    )


def store_or_compare(record, path, content):
    if record:
        path.parent.mkdir(exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return
    if path.read_text(encoding="utf-8") != content:
        raise RuntimeError(f"stored artifact changed: {path}")


def verify_expected_results(red, focused_green, broader_green):
    red_status, red_output = red
    if red_status != 1 or red_output != EXPECTED_RED:
        raise RuntimeError(
            "focused red result changed\n"
            f"exit: {red_status}\noutput:\n{red_output}"
        )

    focused_status, focused_output = focused_green
    if focused_status != 0 or focused_output != EXPECTED_FOCUSED_GREEN:
        raise RuntimeError(
            "focused green result changed\n"
            f"exit: {focused_status}\noutput:\n{focused_output}"
        )

    broader_status, broader_output = broader_green
    if broader_status != 0 or "8 passed" not in broader_output:
        raise RuntimeError(
            "broader green result changed\n"
            f"exit: {broader_status}\noutput:\n{broader_output}"
        )


def store_or_compare_evidence(
    record,
    red,
    patch,
    focused_green,
    broader_green,
):
    red_status, red_output = red
    focused_status, focused_output = focused_green
    broader_status, broader_output = broader_green

    store_or_compare(record, RED_OUTPUT_PATH, red_output)
    store_or_compare(record, RED_STATUS_PATH, f"{red_status}\n")
    store_or_compare(record, PATCH_PATH, patch)
    store_or_compare(
        record,
        FOCUSED_GREEN_OUTPUT_PATH,
        focused_output,
    )
    store_or_compare(
        record,
        FOCUSED_GREEN_STATUS_PATH,
        f"{focused_status}\n",
    )
    store_or_compare(
        record,
        BROADER_GREEN_OUTPUT_PATH,
        broader_output,
    )
    store_or_compare(
        record,
        BROADER_GREEN_STATUS_PATH,
        f"{broader_status}\n",
    )


def verify_metadata_checksums():
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    recorded = {
        RUNNER_PATH: metadata["runner"]["sha256"],
        BEFORE_PATH: metadata["before_fixture"]["sha256"],
        FOCUSED_TEST: metadata["focused_test"]["sha256"],
        REVIEW_PATH_TEST: metadata["review_validation_test"][
            "sha256"
        ],
        RED_OUTPUT_PATH: metadata["focused_test"][
            "red_output_sha256"
        ],
        RED_STATUS_PATH: metadata["focused_test"][
            "red_exit_status_sha256"
        ],
        PATCH_PATH: metadata["patch"]["sha256"],
        FOCUSED_GREEN_OUTPUT_PATH: metadata["green_evidence"][
            "focused_output_sha256"
        ],
        FOCUSED_GREEN_STATUS_PATH: metadata["green_evidence"][
            "focused_exit_status_sha256"
        ],
        BROADER_GREEN_OUTPUT_PATH: metadata["green_evidence"][
            "broader_output_sha256"
        ],
        BROADER_GREEN_STATUS_PATH: metadata["green_evidence"][
            "broader_exit_status_sha256"
        ],
        FINAL_SOURCE: metadata["final_support_checksums"][
            "validator.py"
        ],
        FINAL_TEST: metadata["final_support_checksums"][
            "test_validator.py"
        ],
        FINAL_FOCUSED_TEST: metadata["final_support_checksums"][
            "test_bool_is_not_accepted_as_int.py"
        ],
        FINAL_CLI: metadata["final_support_checksums"]["cli.py"],
        FINAL_SCHEMA: metadata["final_support_checksums"][
            "schema.json"
        ],
        FINAL_CONFIG: metadata["final_support_checksums"][
            "config.json"
        ],
        FINAL_INVALID_CONFIG: metadata["final_support_checksums"][
            "invalid_config.json"
        ],
        PYTEST_CONFIG: metadata["final_support_checksums"][
            "pytest.ini"
        ],
    }
    for path, expected in recorded.items():
        observed = checksum(path)
        if observed != expected:
            raise RuntimeError(
                f"metadata checksum drift: {path}\n"
                f"expected: {expected}\n"
                f"observed: {observed}"
            )


def replay(record):
    clean_work_dir()
    verify_baseline_checksums()
    support_before = {
        path: checksum(path)
        for path in PACKAGE_SUPPORT_PATHS
    }

    WORK_DIR.mkdir()
    shutil.copy2(BEFORE_PATH, WORK_PATH)
    shutil.copy2(FINAL_TEST, WORK_BROADER_TEST)

    red = run_focused_test()
    before_text, after_text = apply_smallest_edit()
    patch = generate_patch(before_text, after_text)
    focused_green = run_focused_test()
    broader_green = run_broader_test()
    verify_expected_results(red, focused_green, broader_green)
    store_or_compare_evidence(
        record,
        red,
        patch,
        focused_green,
        broader_green,
    )

    support_after = {
        path: checksum(path)
        for path in PACKAGE_SUPPORT_PATHS
    }
    if support_before != support_after:
        raise RuntimeError("final support changed during replay")
    if not record:
        verify_metadata_checksums()

    print("RED")
    print(red[1], end="")
    print(f"EXIT STATUS: {red[0]}")
    print("PATCH")
    print(patch, end="")
    print("PATCH STATUS: MATCH")
    print("FOCUSED GREEN")
    print(focused_green[1], end="")
    print(f"EXIT STATUS: {focused_green[0]}")
    print("BROADER GREEN")
    print(broader_green[1], end="")
    print(f"EXIT STATUS: {broader_green[0]}")
    print("FINAL SUPPORT: UNCHANGED")
    print("PARITY: REPLAYED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="refresh reviewed evidence from the immutable before state",
    )
    args = parser.parse_args()
    try:
        clean_work_dir()
        metadata = load_metadata()
        verify_review_state(metadata)
        replay(args.record)
        if metadata.get("capture_stage") == COMPLETED_REVIEW_STAGE:
            print("INDEPENDENT REVIEW: PASS")
        else:
            print("INDEPENDENT REVIEW: PENDING")
    except (json.JSONDecodeError, KeyError, OSError, RuntimeError) as exc:
        print(f"CAPTURE ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        clean_work_dir()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
