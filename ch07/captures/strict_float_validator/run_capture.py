#!/usr/bin/env python3
"""Record or replay the complete strict-float capture."""

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
BEFORE_PATH = CAPTURE_DIR / "before" / "validator.py"
FOCUSED_TEST_PATH = CAPTURE_DIR / "tests" / "focused_test.py"
BROADER_TEST_PATH = CAPTURE_DIR / "tests" / "test_validator.py"
PATCH_PATH = CAPTURE_DIR / "patches" / "strict_float_validator.diff"
APPROVED_INSERTION = (
    '    "dict": lambda value: isinstance(value, dict),\n'
)
STRICT_FLOAT_LINE = (
    '    "float": lambda value: type(value) is float,\n'
)
WIDENED_FLOAT_LINE = (
    '    "float": lambda value: isinstance(value, float),\n'
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


def run_focused(validator_path: Path) -> subprocess.CompletedProcess[str]:
    return run_command(
        [
            sys.executable,
            str(FOCUSED_TEST_PATH),
            str(validator_path),
        ],
        CAPTURE_DIR,
    )


def run_pytest(cwd: Path) -> subprocess.CompletedProcess[str]:
    return run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "test_validator.py",
        ],
        cwd,
    )


def apply_approved_change(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(APPROVED_INSERTION) != 1:
        raise RuntimeError("approved insertion point drifted")
    path.write_text(
        text.replace(
            APPROVED_INSERTION,
            APPROVED_INSERTION + STRICT_FLOAT_LINE,
        ),
        encoding="utf-8",
    )


def apply_widened_change(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(STRICT_FLOAT_LINE) != 1:
        raise RuntimeError("strict float line drifted")
    path.write_text(
        text.replace(STRICT_FLOAT_LINE, WIDENED_FLOAT_LINE),
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
        fromfile="a/validator.py",
        tofile="b/validator.py",
    ))


def verify_review_state(metadata: dict) -> None:
    stage = metadata.get("capture_stage")
    if stage == "ready_for_independent_re_review":
        required = {
            "independent_review_status": "pending",
            "status": "Pending",
        }
        for field, expected in required.items():
            if metadata.get(field) != expected:
                raise RuntimeError(
                    f"pending re-review requires {field}={expected!r}"
                )
        review = metadata.get("previous_independent_review")
        if not isinstance(review, dict):
            raise RuntimeError(
                "pending re-review requires previous review metadata"
            )
        if review.get("status") != "completed":
            raise RuntimeError("previous review must be completed")
        if review.get("verdict") != "Fail":
            raise RuntimeError("previous review must record verdict 'Fail'")
        if not review.get("blocking_findings"):
            raise RuntimeError(
                "failed previous review must retain blocking findings"
            )
        return

    if stage != "complete_independently_reviewed":
        raise RuntimeError(f"unsupported capture stage: {stage!r}")
    previous = metadata.get("previous_independent_review")
    if not isinstance(previous, dict):
        raise RuntimeError("completed stage must retain previous review")
    if previous.get("status") != "completed":
        raise RuntimeError("previous review must remain completed")
    if previous.get("verdict") != "Fail":
        raise RuntimeError("previous review must retain verdict 'Fail'")
    if not previous.get("blocking_findings"):
        raise RuntimeError("previous review must retain blocking findings")
    if metadata.get("independent_review_status") != "completed":
        raise RuntimeError("completed stage requires completed review")
    if metadata.get("status") != "Pass":
        raise RuntimeError("completed stage requires status 'Pass'")
    review = metadata.get("independent_review")
    if not isinstance(review, dict) or review.get("verdict") != "Pass":
        raise RuntimeError("completed stage requires active Pass review")
    artifact = Path(review.get("artifact_path", ""))
    if artifact.is_absolute() or ".." in artifact.parts:
        raise RuntimeError("review artifact path must be package-local")
    artifact_path = (CAPTURE_DIR / artifact).resolve()
    if not artifact_path.is_relative_to(EVIDENCE_DIR.resolve()):
        raise RuntimeError("review artifact must be under evidence/")
    if not artifact_path.is_file():
        raise RuntimeError("completed review artifact is missing")
    require_checksum(
        artifact_path,
        review.get("artifact_checksum_sha256", ""),
    )


def verify_static_inputs(metadata: dict) -> None:
    for relative, expected in metadata[
        "before_fixture"
    ]["checksums_sha256"].items():
        require_checksum(CAPTURE_DIR / relative, expected)
    for relative, expected in metadata[
        "capture_input_checksums_sha256"
    ].items():
        require_checksum(CAPTURE_DIR / relative, expected)
    for relative, expected in metadata[
        "package_read_only_checksums_sha256"
    ]["before"].items():
        require_checksum(PACKAGE_DIR / relative, expected)


def artifact_paths(metadata: dict) -> list[str]:
    return [
        metadata["red"]["output_path"],
        metadata["red"]["exit_status_path"],
        metadata["patch"]["path"],
        metadata["focused_green"]["output_path"],
        metadata["focused_green"]["exit_status_path"],
        metadata["broader_green"]["output_path"],
        metadata["broader_green"]["exit_status_path"],
        metadata["origin_canonical_support_green"]["output_path"],
        metadata["origin_canonical_support_green"]["exit_status_path"],
    ]


def verify_stored_artifacts(metadata: dict) -> None:
    paths = artifact_paths(metadata)
    checksums = metadata["artifact_checksums_sha256"]
    if set(paths) != set(checksums):
        raise RuntimeError("metadata artifact checksum coverage drifted")
    for relative, expected in checksums.items():
        require_checksum(CAPTURE_DIR / relative, expected)


def write_or_compare_text(
    path: Path,
    observed: str,
    record: bool,
) -> None:
    if record:
        path.write_text(observed, encoding="utf-8")
        return
    expected = path.read_text(encoding="utf-8")
    if observed != expected:
        raise RuntimeError(f"stored artifact drift: {path}")


def handle_result(
    result: subprocess.CompletedProcess[str],
    expected_status: int,
    output_path: Path,
    status_path: Path,
    record: bool,
    normalize_pytest_time: bool = False,
) -> None:
    if result.returncode != expected_status:
        raise RuntimeError(
            f"exit status drift for {output_path.name}: "
            f"expected {expected_status}, "
            f"observed {result.returncode}\n"
            f"output:\n{result.stdout}"
        )
    output = (
        stable_pytest_output(result.stdout)
        if normalize_pytest_time
        else result.stdout
    )
    write_or_compare_text(output_path, output, record)
    write_or_compare_text(
        status_path,
        f"{result.returncode}\n",
        record,
    )


def verify_action_record(metadata: dict) -> None:
    path = CAPTURE_DIR / metadata["agent_action_record"]["path"]
    require_checksum(
        path,
        metadata["agent_action_record"]["sha256"],
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    actions = [json.loads(line) for line in lines]
    sequences = [action["sequence"] for action in actions]
    if sequences != list(range(1, len(actions) + 1)):
        raise RuntimeError("agent action sequence drifted")


def verify_policy_discrimination(
    validator_path: Path,
    work_dir: Path,
) -> None:
    adversarial_dir = work_dir / "adversarial-isinstance"
    adversarial_dir.mkdir()
    widened_validator = adversarial_dir / "validator.py"
    shutil.copy2(validator_path, widened_validator)
    apply_widened_change(widened_validator)
    shutil.copy2(
        BROADER_TEST_PATH,
        adversarial_dir / "test_validator.py",
    )

    focused = run_focused(widened_validator)
    if focused.returncode == 0:
        raise RuntimeError(
            "focused check accepted widened isinstance float policy"
        )
    if "test_float_subclass_is_rejected_as_float" not in focused.stdout:
        raise RuntimeError(
            "focused widened-policy failure missed float subclass"
        )

    broader = run_pytest(adversarial_dir)
    if broader.returncode == 0:
        raise RuntimeError(
            "broader check accepted widened isinstance float policy"
        )
    if "test_float_subclass_is_rejected_by_policy" not in broader.stdout:
        raise RuntimeError(
            "broader widened-policy failure missed float subclass"
        )


def verify_parity(metadata: dict) -> None:
    parity = (CAPTURE_DIR / "parity.md").read_text(
        encoding="utf-8"
    )
    required = {
        metadata["red"]["output_path"],
        metadata["patch"]["path"],
        metadata["focused_green"]["output_path"],
        metadata["broader_green"]["output_path"],
        metadata["agent_action_record"]["path"],
        "Listing 7.2",
        "Table 7.1",
    }
    missing = sorted(item for item in required if item not in parity)
    if missing:
        raise RuntimeError(
            "parity ledger is missing: " + ", ".join(missing)
        )


def verify_package_unchanged(metadata: dict) -> None:
    before = metadata[
        "package_read_only_checksums_sha256"
    ]["before"]
    after = metadata[
        "package_read_only_checksums_sha256"
    ]["after"]
    if before != after:
        raise RuntimeError("package before/after declarations differ")
    for relative, expected in after.items():
        require_checksum(PACKAGE_DIR / relative, expected)


def capture(record: bool) -> None:
    metadata_bytes = METADATA_PATH.read_bytes()
    metadata = json.loads(metadata_bytes)
    verify_review_state(metadata)
    verify_static_inputs(metadata)
    verify_action_record(metadata)
    if not record:
        verify_stored_artifacts(metadata)

    with tempfile.TemporaryDirectory(
        dir=CAPTURE_DIR,
        prefix=".work-",
    ) as temp_dir:
        work_dir = Path(temp_dir)
        work_validator = work_dir / "validator.py"
        work_broader_test = work_dir / "test_validator.py"
        shutil.copy2(BEFORE_PATH, work_validator)

        red = run_focused(work_validator)
        handle_result(
            red,
            metadata["red"]["exit_status"],
            CAPTURE_DIR / metadata["red"]["output_path"],
            CAPTURE_DIR / metadata["red"]["exit_status_path"],
            record,
        )

        apply_approved_change(work_validator)
        require_checksum(
            work_validator,
            metadata["patch"]["after_state_sha256"],
        )
        patch = generated_patch(BEFORE_PATH, work_validator)
        write_or_compare_text(PATCH_PATH, patch, record)

        focused_green = run_focused(work_validator)
        handle_result(
            focused_green,
            metadata["focused_green"]["exit_status"],
            CAPTURE_DIR / metadata["focused_green"]["output_path"],
            CAPTURE_DIR / metadata["focused_green"]["exit_status_path"],
            record,
        )

        shutil.copy2(BROADER_TEST_PATH, work_broader_test)
        broader_green = run_pytest(work_dir)
        handle_result(
            broader_green,
            metadata["broader_green"]["exit_status"],
            CAPTURE_DIR / metadata["broader_green"]["output_path"],
            CAPTURE_DIR / metadata["broader_green"]["exit_status_path"],
            record,
            normalize_pytest_time=True,
        )
        verify_policy_discrimination(work_validator, work_dir)

    leftovers = sorted(CAPTURE_DIR.glob(".work-*"))
    if leftovers:
        raise RuntimeError(
            "disposable work state was not cleaned: "
            + ", ".join(str(path) for path in leftovers)
        )

    if not record:
        verify_stored_artifacts(metadata)
        verify_parity(metadata)
    verify_review_state(metadata)
    verify_static_inputs(metadata)
    verify_action_record(metadata)
    verify_package_unchanged(metadata)
    if METADATA_PATH.read_bytes() != metadata_bytes:
        raise RuntimeError("metadata changed during replay")
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
    print(f"POLICY DISCRIMINATION {status}: isinstance rejected")
    print(f"CLEANUP {status}: no disposable work state")
    print(
        "ORIGIN SUPPORT EVIDENCE VERIFIED: "
        "stored artifact checksums only"
    )
    if not record:
        print("PARITY VERIFIED: capture artifacts match metadata")


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
