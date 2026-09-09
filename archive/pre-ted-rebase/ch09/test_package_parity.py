"""Package-local checks for the maintained Chapter 9 teaching surfaces."""

from pathlib import Path
import importlib.util
from types import SimpleNamespace

import pytest


HERE = Path(__file__).parent
CAPTURE_DIR = HERE / "captures" / "house_rule_seam"
SPEC = importlib.util.spec_from_file_location(
    "house_rule_capture_runner", CAPTURE_DIR / "run_capture.py",
)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def test_outbound_rule_matches_the_staged_listing():
    assert (HERE / "AGENTS.md").read_text(encoding="utf-8") == (
        "## Outbound HTTP\n\n"
        "- Feature modules route outbound HTTP through\n"
        "  http_client.call.\n"
        "- Feature modules do not import a transport directly.\n"
        "- Tests inject a transport and make no live calls.\n"
        "- test_house_rules.py enforces the import boundary.\n"
    )


def test_green_alert_keeps_the_three_line_repair():
    source = (HERE / "alerts.py").read_text(encoding="utf-8")
    captured_after = (
        CAPTURE_DIR / "after" / "alerts.py"
    ).read_text(encoding="utf-8")
    required_lines = (
        "from http_client import call",
        'response = call("POST", ALERTS_URL, json={"text": message})',
        "return response.status < 400",
    )

    for line in required_lines:
        assert line in source
        assert line in captured_after


def test_parity_map_covers_current_chapter_surfaces():
    parity = (HERE / "parity.md").read_text(encoding="utf-8")

    for token in (
        "Listing 9.1 outbound rule",
        "Listing 9.2 shared HTTP seam",
        "Listing 9.3 illustrative skill shape",
        "Listing 9.4 retrieval flow",
        "MCP resources, prompts, and tools",
        "Lethal-trifecta containment",
        "Real alert seam session",
    ):
        assert token in parity


def test_capture_is_public_and_package_local():
    session = (
        CAPTURE_DIR / "session.md"
    ).read_text(encoding="utf-8")
    runner = (
        CAPTURE_DIR / "run_capture.py"
    ).read_text(encoding="utf-8")

    for forbidden in (
        "AI_Book_Official",
        "manuscripts/",
        "chapters/",
        "code/ch09",
    ):
        assert forbidden not in session
        assert forbidden not in runner


def test_capture_patch_preserves_the_exact_boundary_change():
    patch = (
        CAPTURE_DIR / "patches" / "house_rule_seam.patch"
    ).read_text(encoding="utf-8")

    assert "-import requests" in patch
    assert "+from http_client import call" in patch
    assert (
        '-    response = requests.post('
        in patch
    )
    assert (
        '+    response = call("POST", ALERTS_URL, json={"text": message})'
        in patch
    )
    assert "-    return response.status_code < 400" in patch
    assert "+    return response.status < 400" in patch


def test_pytest_collection_excludes_capture_internals():
    pytest_config = (HERE / "pytest.ini").read_text(encoding="utf-8")
    assert "norecursedirs = captures" in pytest_config


def test_capture_keeps_the_shared_client_unchanged():
    before = (CAPTURE_DIR / "before" / "http_client.py").read_bytes()
    after = (CAPTURE_DIR / "after" / "http_client.py").read_bytes()
    assert before == after
    assert b"TRANSIENT_STATUSES = frozenset({429, 502, 503, 504})" in before
    assert b"inject one with set_transport" in before


def test_capture_accepts_only_the_expected_red():
    diagnostic = (
        "send_alert must route method, URL, and JSON through http_client.call"
    )
    RUNNER.require_result(
        SimpleNamespace(returncode=1, stdout=f"{diagnostic}\n1 failed in 0.01s\n"),
        1, "1 failed", diagnostic,
    )
    with pytest.raises(RuntimeError, match="did not match"):
        RUNNER.require_result(
            SimpleNamespace(returncode=1, stdout="unrelated failure\n1 failed\n"),
            1, "1 failed", diagnostic,
        )


def test_capture_rejects_drifted_after_state(tmp_path, monkeypatch):
    for filename in ("alerts.py", "http_client.py"):
        (tmp_path / filename).write_bytes(
            (CAPTURE_DIR / "after" / filename).read_bytes(),
        )
    monkeypatch.setattr(RUNNER, "WORK_DIR", tmp_path)
    RUNNER.verify_after_state()
    (tmp_path / "http_client.py").write_text("changed\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="after state drifted"):
        RUNNER.verify_after_state()


def test_capture_cleanup_retains_evidence(tmp_path):
    (tmp_path / ".work").mkdir()
    (tmp_path / ".work-review").mkdir()
    (tmp_path / "evidence").mkdir()
    RUNNER.clean_work_directories(tmp_path)
    RUNNER.require_work_cleanup(tmp_path)
    assert (tmp_path / "evidence").is_dir()
