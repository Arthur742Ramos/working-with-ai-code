"""Package-local checks for the maintained Chapter 9 teaching surfaces."""

from pathlib import Path


HERE = Path(__file__).parent
CAPTURE_DIR = HERE / "captures" / "house_rule_seam"


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
