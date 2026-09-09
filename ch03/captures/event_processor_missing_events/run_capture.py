"""Record or replay the event processor capture."""
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
METADATA_PATH = CAPTURE_DIR / "metadata.json"
BEFORE_PATH = CAPTURE_DIR / "before" / "event_processor.py"
FOCUSED_TEST = CAPTURE_DIR / "tests" / "focused_test.py"
BROADER_TEST = (
    CAPTURE_DIR / "tests" / "full_capture_check.py"
)
PATCH_PATH = CAPTURE_DIR / "patches" / "event_processor.diff"
WORK_DIR = CAPTURE_DIR / ".work"
WORK_PATH = WORK_DIR / "event_processor.py"
REJECTED_PATH = WORK_DIR / "rejected_event_processor.py"
CHAPTER_SESSION_PATH = CAPTURE_DIR / "chapter-session.md"
COMPLETED_REVIEW_STAGE = "complete_independently_reviewed"

EXPECTED_RED = (
    "FAIL: test_missing_events_collection_raises_value_error\n"
    "expected: ValueError: input must be an object with "
    "an 'events' key\n"
    "observed: KeyError: 'events'\n"
    "PASS: test_explicit_empty_events_is_not_missing\n"
    "observed: reached later empty-result arithmetic\n"
    "1 failed, 1 passed\n"
)
EXPECTED_REJECTED = (
    "PASS: test_missing_events_collection_raises_value_error\n"
    "observed: ValueError: input must be an object with "
    "an 'events' key\n"
    "FAIL: test_explicit_empty_events_is_not_missing\n"
    "expected: explicit empty events to reach later "
    "empty-result arithmetic\n"
    "observed: ValueError: input must be an object with "
    "an 'events' key\n"
    "1 failed, 1 passed\n"
)
EXPECTED_FOCUSED_GREEN = (
    "PASS: test_missing_events_collection_raises_value_error\n"
    "observed: ValueError: input must be an object with "
    "an 'events' key\n"
    "PASS: test_explicit_empty_events_is_not_missing\n"
    "observed: reached later empty-result arithmetic\n"
    "2 passed\n"
)
EXPECTED_BROADER_GREEN = (
    "PASS: test_missing_events_collection_raises_value_error\n"
    "PASS: test_explicit_empty_events_is_not_missing\n"
    "PASS: test_existing_happy_path_still_works\n"
    "3 passed\n"
)
SOURCE_NEEDLE = """    data = json.load(f)

    results = []"""
SOURCE_REPLACEMENT = """    data = json.load(f)
    if "events" not in data:
        raise ValueError(
            "input must be an object with an 'events' key"
        )

    results = []"""
REJECTED_REPLACEMENT = """    data = json.load(f)
    if not data.get("events"):
        raise ValueError(
            "input must be an object with an 'events' key"
        )

    results = []"""
EXPECTED_PROVENANCE = (
    "The broader review is reconstructed. It rebuilds a plausible path "
    "from preserved starting and final implementations; it is not a "
    "captured multi-stage agent run. Inside that review, the missing-events "
    "repair comes from a verified Claude Code 2.1.210.642 capture acting on "
    "`event_processor.py`. The original bounded prompt was not retained, so "
    "the human contract is reconstructed and labeled.\n\n"
    "The inspection, command sequence, exact diff, and green results come "
    "from the retained action record and machine-preserved evidence. They "
    "support one ask-inspect-adjust turn. The later checkpoint and timezone "
    "material extend that turn through reconstructed follow-up work; the "
    "capture does not prove those exchanges."
)
EXPECTED_INSPECTION = (
    "Inspect what the check bought you. The four-line guard is the smallest "
    "reviewable change in the function's surrounding style: it names the "
    "missing-key branch before the existing loop and keeps the full error "
    "message readable without compressing the control flow. The focused "
    "result proves the exact missing-key error and discriminates it from an "
    "explicit empty list: the empty-list case reaches the already-known "
    "later arithmetic defect instead of being rejected as missing. The "
    "broader result proves one representative valid non-empty input still "
    "produces and writes the expected summary. Neither check proves how "
    "non-object JSON, a non-list `events` value, or malformed individual "
    "events behave. The checks enforce the selected missing-versus-empty "
    "policy; they do not choose it. That decision belongs to the people who "
    "own the input contract."
)


class CaptureError(RuntimeError):
    """Report an evidence or replay mismatch."""


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checksum_value(path):
    return f"sha256:{sha256(path)}"


def digest_value(value):
    prefix = "sha256:"
    if not value.startswith(prefix):
        raise CaptureError(f"invalid checksum value: {value}")
    return value[len(prefix):]


def load_metadata():
    return json.loads(
        METADATA_PATH.read_text(encoding="utf-8")
    )


def write_metadata(metadata):
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )


def verify_checksum(path, expected):
    observed = sha256(path)
    expected_digest = digest_value(expected)
    if observed != expected_digest:
        raise CaptureError(
            f"checksum drift: {path}\n"
            f"expected: {expected_digest}\n"
            f"observed: {observed}"
        )


def verify_mapping(mapping):
    for relative_path, expected in mapping.items():
        verify_checksum(
            PACKAGE_ROOT / relative_path,
            expected,
        )


def verify_immutable_inputs(metadata):
    for relative_path, expected in (
        metadata["before_fixture_checksums"].items()
    ):
        verify_checksum(CAPTURE_DIR / relative_path, expected)
    for relative_path, expected in (
        metadata["test_checksums"].items()
    ):
        verify_checksum(CAPTURE_DIR / relative_path, expected)
    verify_mapping(
        metadata["canonical_support_checksums_before"]
    )


def prepare_working_copy():
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    WORK_DIR.mkdir()
    (WORK_DIR / "tmp").mkdir()
    for path in (WORK_PATH, REJECTED_PATH):
        shutil.copy2(BEFORE_PATH, path)
        path.chmod(0o644)


def apply_replacement(path, replacement):
    source = path.read_text(encoding="utf-8")
    if source.count(SOURCE_NEEDLE) != 1:
        raise CaptureError(
            "selected edit no longer has one exact target"
        )
    path.write_text(
        source.replace(SOURCE_NEEDLE, replacement, 1),
        encoding="utf-8",
    )


def generate_patch():
    completed = subprocess.run(
        [
            "diff",
            "-u",
            "--label",
            "a/event_processor.py",
            "--label",
            "b/event_processor.py",
            str(BEFORE_PATH),
            str(WORK_PATH),
        ],
        cwd=CAPTURE_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 1:
        raise CaptureError(
            "diff did not report exactly one changed file: "
            f"exit {completed.returncode}\n{completed.stdout}"
        )
    return completed.stdout


def run_python(script, target):
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["TMPDIR"] = str(WORK_DIR / "tmp")
    completed = subprocess.run(
        [sys.executable, str(script), str(target)],
        cwd=CAPTURE_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def run_canonical_support():
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PY_COLORS"] = "0"
    environment["NO_COLOR"] = "1"
    target = PACKAGE_ROOT / "test_event_processor.py"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-qq",
            "-p",
            "no:cacheprovider",
            "-c",
            str(PACKAGE_ROOT / "pytest.ini"),
            str(target),
        ],
        cwd=PACKAGE_ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def require_result(name, result, expected_status,
                   expected_output):
    status, output = result
    if status != expected_status:
        raise CaptureError(
            f"{name} exit status changed: {status}"
        )
    if output != expected_output:
        raise CaptureError(
            f"{name} output changed\n{output}"
        )


def artifact_records(metadata):
    return [
        metadata["red"],
        metadata["discriminating_control"],
        metadata["focused_green"],
        metadata["broader_green"],
        metadata["canonical_support_green"],
    ]


def artifact_paths(metadata):
    paths = [(PATCH_PATH, metadata["patch"]["checksum"])]
    for record in artifact_records(metadata):
        paths.append((
            CAPTURE_DIR / record["output_path"],
            record["output_checksum"],
        ))
        paths.append((
            CAPTURE_DIR / record["exit_status_path"],
            record["exit_status_checksum"],
        ))
    return paths


def verify_artifact_checksums(metadata):
    for path, expected in artifact_paths(metadata):
        verify_checksum(path, expected)


def write_read_only(path, content):
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        path.chmod(0o644)
    path.write_text(content, encoding="utf-8")
    path.chmod(0o444)


def write_result(record, result):
    status, output = result
    write_read_only(
        CAPTURE_DIR / record["output_path"],
        output,
    )
    write_read_only(
        CAPTURE_DIR / record["exit_status_path"],
        f"{status}\n",
    )


def update_artifact_checksums(metadata):
    metadata["patch"]["checksum"] = checksum_value(PATCH_PATH)
    for record in artifact_records(metadata):
        output_path = CAPTURE_DIR / record["output_path"]
        exit_path = CAPTURE_DIR / record["exit_status_path"]
        record["output_checksum"] = checksum_value(output_path)
        record["exit_status_checksum"] = checksum_value(exit_path)


def record_path(relative_path):
    return CAPTURE_DIR / relative_path


def update_record_checksums(metadata):
    for relative_path in metadata["record_checksums"]:
        metadata["record_checksums"][relative_path] = (
            checksum_value(record_path(relative_path))
        )


def verify_record_checksums(metadata):
    for relative_path, expected in (
        metadata["record_checksums"].items()
    ):
        verify_checksum(record_path(relative_path), expected)


def verify_review_state(metadata):
    if metadata.get("session_stage") != COMPLETED_REVIEW_STAGE:
        return

    review = metadata.get("independent_review")
    if not isinstance(review, dict):
        raise CaptureError(
            "completed independent review metadata is missing"
        )
    if review.get("status") != "completed":
        raise CaptureError(
            "completed package has no completed active review"
        )
    if review.get("verdict") != "Pass":
        raise CaptureError(
            "completed package has no Pass review verdict"
        )

    artifact_path = review.get("artifact_path")
    artifact_checksum = review.get("artifact_checksum")
    if not isinstance(artifact_path, str) or not artifact_path:
        raise CaptureError(
            "completed package has no review artifact path"
        )
    relative_path = Path(artifact_path)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise CaptureError("review artifact path must be package-local")
    if not isinstance(artifact_checksum, str):
        raise CaptureError(
            "completed package has no review artifact checksum"
        )
    artifact = CAPTURE_DIR / relative_path
    if not artifact.is_file():
        raise CaptureError(
            f"completed review artifact is missing: {artifact_path}"
        )
    verify_checksum(artifact, artifact_checksum)


def record_artifacts(metadata, patch, results):
    write_read_only(PATCH_PATH, patch)
    for key, result in results.items():
        write_result(metadata[key], result)
    update_artifact_checksums(metadata)
    update_record_checksums(metadata)
    write_metadata(metadata)


def compare_text(path, observed, name):
    stored = path.read_text(encoding="utf-8")
    if observed != stored:
        raise CaptureError(f"stored {name} drifted")


def compare_result(record, result, name):
    status, output = result
    compare_text(
        CAPTURE_DIR / record["output_path"],
        output,
        f"{name} output",
    )
    compare_text(
        CAPTURE_DIR / record["exit_status_path"],
        f"{status}\n",
        f"{name} exit status",
    )


def compare_artifacts(metadata, patch, results):
    compare_text(PATCH_PATH, patch, "patch")
    for key, result in results.items():
        compare_result(metadata[key], result, key.replace("_", " "))


def unquote_callouts(text):
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


def extract_printed_patch(text, source_name):
    marker = "Listing 3.2 Missing-events validation guard\n\n```diff\n"
    if text.count(marker) != 1:
        raise CaptureError(
            f"printed patch marker drifted: {source_name}"
        )
    remainder = text.split(marker, 1)[1]
    if "\n```" not in remainder:
        raise CaptureError(
            f"printed patch fence is incomplete: {source_name}"
        )
    return remainder.split("\n```", 1)[0] + "\n"


def verify_chapter_session(patch):
    text = CHAPTER_SESSION_PATH.read_text(encoding="utf-8")
    if text.count(EXPECTED_PROVENANCE) != 1:
        raise CaptureError("chapter-session provenance drifted")
    if extract_printed_patch(text, CHAPTER_SESSION_PATH) != patch:
        raise CaptureError("chapter-session patch drifted")
    if text.count(EXPECTED_INSPECTION) != 1:
        raise CaptureError("chapter-session inspection drifted")
    if "manuscripts/restructure" in text or "code/ch03" in text:
        raise CaptureError("private support path leaked into chapter-session")


def run_capture():
    prepare_working_copy()
    red = run_python(FOCUSED_TEST, WORK_PATH)
    require_result("focused red", red, 1, EXPECTED_RED)

    apply_replacement(REJECTED_PATH, REJECTED_REPLACEMENT)
    discriminating = run_python(FOCUSED_TEST, REJECTED_PATH)
    require_result(
        "discriminating control",
        discriminating,
        1,
        EXPECTED_REJECTED,
    )

    apply_replacement(WORK_PATH, SOURCE_REPLACEMENT)
    patch = generate_patch()

    focused_green = run_python(FOCUSED_TEST, WORK_PATH)
    require_result(
        "focused green",
        focused_green,
        0,
        EXPECTED_FOCUSED_GREEN,
    )
    broader_green = run_python(BROADER_TEST, WORK_PATH)
    require_result(
        "broader green",
        broader_green,
        0,
        EXPECTED_BROADER_GREEN,
    )
    canonical_green = run_canonical_support()
    if canonical_green[0] != 0:
        raise CaptureError(
            "final package tests failed:\n"
            f"{canonical_green[1]}"
        )
    return patch, {
        "red": red,
        "discriminating_control": discriminating,
        "focused_green": focused_green,
        "broader_green": broader_green,
        "canonical_support_green": canonical_green,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="intentionally recreate reviewed evidence",
    )
    args = parser.parse_args()
    metadata = load_metadata()

    try:
        verify_review_state(metadata)
        verify_immutable_inputs(metadata)
        patch, results = run_capture()
        if args.record:
            record_artifacts(metadata, patch, results)
        else:
            verify_artifact_checksums(metadata)
            compare_artifacts(metadata, patch, results)
            verify_record_checksums(metadata)
        verify_mapping(
            metadata["canonical_support_checksums_after"]
        )
        verify_chapter_session(patch)

        print("RED: MATCH (exit 1)")
        print(
            "DISCRIMINATION: PASS "
            "(if not data.get(\"events\") rejected)"
        )
        print("PATCH: MATCH (readable missing-key guard)")
        print("FOCUSED GREEN: MATCH (exit 0)")
        print("BROADER GREEN: MATCH (exit 0)")
        print("FINAL PACKAGE: MATCH (exit 0)")
        print("CHAPTER SESSION: MATCH")
        print("INDEPENDENT REVIEW: PASS")
        print("PARITY: PASS")
    except (CaptureError, KeyError, OSError) as exc:
        print(f"CAPTURE ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(WORK_DIR, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
