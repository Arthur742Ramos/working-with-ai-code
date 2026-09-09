#!/usr/bin/env python3
"""Record or replay the complete Chapter 9 house-rule capture."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
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
BEFORE_DIR = CAPTURE_DIR / "before"
AFTER_DIR = CAPTURE_DIR / "after"
TEST_DIR = CAPTURE_DIR / "tests"
PATCH_PATH = CAPTURE_DIR / "patches" / "house_rule_seam.patch"
EVIDENCE_DIR = CAPTURE_DIR / "evidence"
METADATA_PATH = CAPTURE_DIR / "metadata.json"

FOCUSED_TARGET = (
    "tests/test_alerts.py::"
    "test_send_alert_routes_through_house_client"
)
COMMANDS = {
    "red": (
        "PYTHONPATH=before HOUSE_RULE_ROOT=before "
        "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q "
        "-p no:cacheprovider "
        f"{FOCUSED_TARGET}"
    ),
    "focused_green": (
        "PYTHONPATH=before HOUSE_RULE_ROOT=before "
        "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q "
        "-p no:cacheprovider "
        f"{FOCUSED_TARGET}"
    ),
    "broader_green": (
        "PYTHONPATH=before HOUSE_RULE_ROOT=before "
        "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q "
        "-p no:cacheprovider tests"
    ),
    "package_green": (
        "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q "
        "-p no:cacheprovider"
    ),
}

EXPECTED_BEFORE = {
    "alerts.py": (
        "ad35f4f08f1b7d18b198d48a491dc016"
        "0a917233534bddabac05564cb0d5cd8e"
    ),
    "http_client.py": (
        "cba93e87a679816972d8bc091e3d8a0f"
        "ae75b43afa835ada82036b45fa1f4541"
    ),
}
EXPECTED_AFTER = {
    "alerts.py": (
        "39920989758296b10ccc4c13f57d4387"
        "cbfecc266e34a38f098f185385fa44c0"
    ),
    "http_client.py": EXPECTED_BEFORE["http_client.py"],
}
EXPECTED_TESTS = {
    "test_alerts.py": (
        "ec1dd662429f7d9ff7a42b1c9285729d"
        "75d659b7ade0b6237f432805ab120195"
    ),
    "test_house_rules.py": (
        "60f9e05fb81300121e2fa112d8155e52"
        "f020e559aabdc055549d7876d8cd74d8"
    ),
    "test_http_client.py": (
        "7f5faaa061888fe91ecbcdd5ffbedbb22"
        "7805680036ba7c99461ddd9763037d3"
    ),
    "fixtures/direct_requests/alerts.py": EXPECTED_BEFORE["alerts.py"],
}
PACKAGE_FILES = (
    "AGENTS.md",
    "README.md",
    "alerts.py",
    "http_client.py",
    "mcp_policy.py",
    "parity.md",
    "pytest.ini",
    "requirements.txt",
    "retrieval.py",
    "test_alerts.py",
    "test_house_rules.py",
    "test_http_client.py",
    "test_mcp_policy.py",
    "test_package_parity.py",
    "test_retrieval.py",
)
EXPECTED_PATCH = (
    "572173f91e3f2b0a21a6730e606d68e6"
    "d32c8188e0c6617c0ca790b009deb949"
)
EXPECTED_CHANGE_LINES = [
    "-import requests",
    "+from http_client import call",
    "-    response = requests.post(ALERTS_URL, json={\"text\": message})",
    "-    return response.status_code < 400",
    "+    response = call(\"POST\", ALERTS_URL, json={\"text\": message})",
    "+    return response.status < 400",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_hash(path: Path, expected: str, label: str) -> None:
    observed = sha256(path)
    if observed != expected:
        raise RuntimeError(
            f"{label} checksum drifted: {path}\n"
            f"expected: {expected}\nobserved: {observed}"
        )


def load_metadata() -> dict:
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def verify_review_state(metadata: dict) -> str:
    state = metadata.get("review_state")
    if not isinstance(state, dict):
        raise RuntimeError("review_state metadata is missing")

    stage = state.get("stage")
    active = state.get("active_review")
    if not isinstance(active, dict):
        raise RuntimeError("active review metadata is missing")

    if stage == "pending_independent_re_review":
        expected = {
            "status": "pending",
            "verdict": "Pending",
            "artifact": "pending",
        }
        for field, value in expected.items():
            if active.get(field) != value:
                raise RuntimeError(
                    "pending review state drifted: "
                    f"{field} must be {value!r}"
                )
        return "PENDING RE-REVIEW"

    if stage != "complete_independently_reviewed":
        raise RuntimeError(f"unknown review stage: {stage!r}")
    if active.get("status") != "completed":
        raise RuntimeError("completed review has no completed status")
    if active.get("verdict") != "Pass":
        raise RuntimeError("completed review has no Pass verdict")
    if active.get("blocking_findings") != []:
        raise RuntimeError("completed review retains blocking findings")

    artifact = active.get("artifact")
    if not isinstance(artifact, str) or not artifact.strip():
        raise RuntimeError("completed review has no artifact")
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
    expected_checksum = active.get("artifact_checksum")
    if not isinstance(expected_checksum, str) or not expected_checksum.strip():
        raise RuntimeError("completed review has no artifact checksum")
    require_hash(
        artifact_path,
        expected_checksum,
        "independent review artifact",
    )
    return "PASS"


def work_directories() -> list[Path]:
    return sorted(CAPTURE_DIR.glob(".work-*"))


def verify_no_work_directories() -> None:
    leftovers = work_directories()
    if leftovers:
        names = ", ".join(path.name for path in leftovers)
        raise RuntimeError(f"stale disposable work directories: {names}")


@contextmanager
def disposable_work():
    verify_no_work_directories()
    work = Path(tempfile.mkdtemp(dir=CAPTURE_DIR, prefix=".work-"))
    try:
        yield work
    finally:
        shutil.rmtree(work, ignore_errors=True)
    verify_no_work_directories()


def verify_fixture_and_package(metadata: dict) -> None:
    for name, expected in EXPECTED_BEFORE.items():
        require_hash(BEFORE_DIR / name, expected, "before fixture")
        if metadata["before_fixture_checksums"][f"before/{name}"] != expected:
            raise RuntimeError(f"metadata before checksum drifted: {name}")

    for name, expected in EXPECTED_AFTER.items():
        require_hash(AFTER_DIR / name, expected, "after fixture")
        if metadata["after_fixture_checksums"][f"after/{name}"] != expected:
            raise RuntimeError(f"metadata after checksum drifted: {name}")

    for name, expected in EXPECTED_TESTS.items():
        require_hash(TEST_DIR / name, expected, "test fixture")
        if metadata["test_checksums"][f"tests/{name}"] != expected:
            raise RuntimeError(f"metadata test checksum drifted: {name}")

    package_checksums = metadata["package_checksums"]
    if set(package_checksums) != set(PACKAGE_FILES):
        raise RuntimeError("metadata package file set drifted")
    for name in PACKAGE_FILES:
        require_hash(
            PACKAGE_DIR / name,
            package_checksums[name],
            "package source",
        )


def verify_origin_provenance(metadata: dict) -> None:
    origin = metadata["canonical_support_green"]
    if origin["exit_status"] != 0:
        raise RuntimeError("historical canonical green status drifted")
    for key in ("output", "exit_status"):
        require_hash(
            CAPTURE_DIR / origin[f"{key}_file"],
            origin[f"{key}_checksum"],
            "historical canonical evidence",
        )
    if not metadata["canonical_support_checksums"]:
        raise RuntimeError("historical support checksums are missing")
    if not metadata["canonical_chapter_checksums"]:
        raise RuntimeError("historical chapter checksums are missing")


def verify_patch(metadata: dict) -> None:
    require_hash(PATCH_PATH, EXPECTED_PATCH, "patch")
    if metadata["patch"]["checksum"] != EXPECTED_PATCH:
        raise RuntimeError("metadata patch checksum drifted")
    changed = [
        line
        for line in PATCH_PATH.read_text(encoding="utf-8").splitlines()
        if line.startswith(("+", "-"))
        and not line.startswith(("+++", "---"))
    ]
    if changed != EXPECTED_CHANGE_LINES:
        raise RuntimeError("patch is not the approved three-line substitution")
    if (BEFORE_DIR / "http_client.py").read_bytes() != (
        AFTER_DIR / "http_client.py"
    ).read_bytes():
        raise RuntimeError("unchanged shared client drifted in after state")


def verify_metadata(metadata: dict) -> None:
    if metadata["stage"] != "completed":
        raise RuntimeError("metadata stage is not completed")
    if not metadata["production_repair_applied"]:
        raise RuntimeError("metadata does not record the staged repair")
    if not metadata["after_implementation_created"]:
        raise RuntimeError("metadata does not record the after state")
    if metadata["status"] != "complete_smallest_reviewable_diff":
        raise RuntimeError("metadata status is not final")
    if metadata["patch"]["minimality_standard"] != "smallest_reviewable_diff":
        raise RuntimeError("metadata minimality standard drifted")
    if metadata["publication_source"] != {
        "file": "chapter-session.md",
        "status": "current",
        "authorial_inspection": "present_as_single_closing_paragraph",
    }:
        raise RuntimeError("metadata publication source drifted")
    superseded = metadata["superseded_transcript"]
    if superseded["status"] != "superseded_for_staged_rewrite":
        raise RuntimeError("canonical transcript is not marked superseded")
    if superseded["canonical_file_modified"]:
        raise RuntimeError("metadata claims the canonical chapter was modified")
    expected_statuses = {
        "red": 1,
        "focused_green": 0,
        "broader_green": 0,
        "package_green": 0,
    }
    for key, expected_status in expected_statuses.items():
        record = metadata[key]
        if record["command"] != COMMANDS[key]:
            raise RuntimeError(f"metadata command drifted: {key}")
        if record["exit_status"] != expected_status:
            raise RuntimeError(f"metadata status drifted: {key}")


def verify_records(metadata: dict) -> None:
    required = {
        "README.md": (
            "Human-owned policy boundary",
            "Non-recording replay",
            "Independent review state",
            "module-qualified shared-client use",
        ),
        "session.md": (
            "Approval basis",
            "Agent action record",
            "Exact applied diff",
            "Agent evidence boundary",
        ),
        "chapter-session.md": (
            "smallest reviewable diff",
            "Inspect the three changed lines",
            "Service maintainers still set that policy",
            "direct or module-qualified shared-client use",
        ),
        "parity.md": (
            "focused_green.txt",
            "broader_green.txt",
            "house_rule_seam.patch",
            "Printed red excerpt",
            "complete_independently_reviewed",
            "evidence/independent-review.md",
        ),
        "evidence/agent-actions.md": (
            "Strengthened `test_send_alert_routes_through_house_client`",
            "Reran the focused test",
            "Kept `patches/house_rule_seam.patch` byte-identical",
            "Certification repair after first independent review",
        ),
    }
    for relative, tokens in required.items():
        text = (CAPTURE_DIR / relative).read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                raise RuntimeError(
                    f"record is incomplete: {relative}: {token}"
                )

    hash_records = {
        "run_capture.py": metadata["runner"]["checksum"],
        "README.md": metadata["record_checksums"]["README.md"],
        "session.md": metadata["record_checksums"]["session.md"],
        "chapter-session.md": metadata["record_checksums"][
            "chapter-session.md"
        ],
        "parity.md": metadata["record_checksums"]["parity.md"],
        "patches/README.md": metadata["record_checksums"]["patches/README.md"],
        "evidence/agent-actions.md": metadata["agent_action_record"]["checksum"],
    }
    for relative, expected in hash_records.items():
        require_hash(CAPTURE_DIR / relative, expected, "package record")

    correction = metadata["actual_setup_correction"]
    for kind in ("output", "exit_status"):
        require_hash(
            CAPTURE_DIR / correction[f"{kind}_file"],
            correction[f"{kind}_checksum"],
            "preserved broader setup failure",
        )


def verify_publication_evidence(metadata: dict) -> None:
    chapter = (CAPTURE_DIR / "chapter-session.md").read_text(
        encoding="utf-8"
    )
    for key in ("red", "focused_green", "broader_green"):
        evidence = (
            CAPTURE_DIR / metadata[key]["output_file"]
        ).read_text(encoding="utf-8").rstrip("\n")
        quoted = "\n".join(
            ">" if not line else f"> {line}"
            for line in evidence.splitlines()
        )
        if quoted not in chapter:
            raise RuntimeError(
                f"chapter-session.md does not reproduce {key} evidence"
            )


def reset_work(work: Path) -> None:
    ignored = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(BEFORE_DIR, work / "before", ignore=ignored)
    shutil.copytree(TEST_DIR, work / "tests", ignore=ignored)


def run_pytest(
    cwd: Path,
    target: str | None,
    source_root: str | None,
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
    ]
    if target:
        command.append(target)
    env = os.environ.copy()
    env.update({
        "FORCE_COLOR": "0",
        "NO_COLOR": "1",
        "PY_COLORS": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_ADDOPTS": "",
        "TERM": "dumb",
    })
    if source_root is not None:
        env["HOUSE_RULE_ROOT"] = source_root
        env["PYTHONPATH"] = source_root
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def apply_patch_and_verify(work: Path) -> None:
    staged_before = work / "before"
    completed = subprocess.run(
        ["patch", "-s", "-p1", "-i", str(PATCH_PATH)],
        cwd=staged_before,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "stored patch did not apply cleanly\n"
            f"{completed.stdout}"
        )
    for name in EXPECTED_AFTER:
        if (staged_before / name).read_bytes() != (
            AFTER_DIR / name
        ).read_bytes():
            raise RuntimeError(f"recreated after state drifted: {name}")


def require_semantics(results: dict[str, subprocess.CompletedProcess[str]]) -> None:
    red = results["red"]
    if red.returncode != 1 or (
        "send_alert must route method, URL, and JSON "
        "through http_client.call"
        not in red.stdout
    ):
        raise RuntimeError(
            "focused test did not reproduce the required red state\n"
            f"{red.stdout}"
        )
    focused = results["focused_green"]
    if focused.returncode != 0 or "1 passed" not in focused.stdout:
        raise RuntimeError(f"focused green failed\n{focused.stdout}")
    broader = results["broader_green"]
    if broader.returncode != 0 or "10 passed" not in broader.stdout:
        raise RuntimeError(f"broader green failed\n{broader.stdout}")
    package = results["package_green"]
    if package.returncode != 0 or "28 passed" not in package.stdout:
        raise RuntimeError(
            f"package-local green failed\n{package.stdout}"
        )


def stable_output(text: str) -> str:
    return re.sub(r"in \d+(?:\.\d+)?s", "in <TIME>s", text)


def evidence_paths(key: str) -> tuple[Path, Path]:
    record = {
        "red": "focused_red",
        "focused_green": "focused_green",
        "broader_green": "broader_green",
        "package_green": "package_green",
    }[key]
    return (
        EVIDENCE_DIR / f"{record}.txt",
        EVIDENCE_DIR / f"{record}.exit_status",
    )


def record_results(
    results: dict[str, subprocess.CompletedProcess[str]],
    metadata: dict,
) -> dict:
    for key, result in results.items():
        output_path, exit_path = evidence_paths(key)
        output_path.write_text(result.stdout, encoding="utf-8")
        exit_path.write_text(f"{result.returncode}\n", encoding="utf-8")
        metadata[key]["output_checksum"] = sha256(output_path)
        metadata[key]["exit_status_checksum"] = sha256(exit_path)
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    return metadata


def compare_results(
    results: dict[str, subprocess.CompletedProcess[str]],
    metadata: dict,
) -> None:
    for key, result in results.items():
        output_path, exit_path = evidence_paths(key)
        expected_output = output_path.read_text(encoding="utf-8")
        expected_exit = int(exit_path.read_text(encoding="utf-8"))
        if stable_output(result.stdout) != stable_output(expected_output):
            raise RuntimeError(f"stored {key} output drifted")
        if result.returncode != expected_exit:
            raise RuntimeError(f"stored {key} exit status drifted")
        require_hash(
            output_path,
            metadata[key]["output_checksum"],
            f"{key} evidence",
        )
        require_hash(
            exit_path,
            metadata[key]["exit_status_checksum"],
            f"{key} exit evidence",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        action="store_true",
        help="refresh verified command evidence and metadata checksums",
    )
    args = parser.parse_args()
    metadata = load_metadata()

    review_status = verify_review_state(metadata)
    verify_metadata(metadata)
    verify_fixture_and_package(metadata)
    verify_origin_provenance(metadata)
    verify_patch(metadata)
    verify_records(metadata)

    with disposable_work() as work:
        reset_work(work)
        red = run_pytest(work, FOCUSED_TARGET, "before")
        apply_patch_and_verify(work)
        focused_green = run_pytest(work, FOCUSED_TARGET, "before")
        broader_green = run_pytest(work, "tests", "before")

    package_green = run_pytest(PACKAGE_DIR, None, None)
    results = {
        "red": red,
        "focused_green": focused_green,
        "broader_green": broader_green,
        "package_green": package_green,
    }
    require_semantics(results)
    if args.record:
        metadata = record_results(results, metadata)
    compare_results(results, metadata)
    verify_publication_evidence(metadata)
    verify_fixture_and_package(metadata)
    verify_origin_provenance(metadata)
    verify_no_work_directories()

    print(f"RED EXIT: {red.returncode}")
    print("PATCH STATUS: exact three-line patch applied")
    print(f"FOCUSED GREEN EXIT: {focused_green.returncode}")
    print(f"BROADER GREEN EXIT: {broader_green.returncode}")
    print(f"PACKAGE GREEN EXIT: {package_green.returncode}")
    print(f"INDEPENDENT REVIEW: {review_status}")
    print("PARITY STATUS: package-local records and checksums match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
