"""Package-local checks for staged parity and isolation."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest


HERE = Path(__file__).parent
CAPTURE_DIR = HERE / "captures" / "house_rule_seam"


def load_capture_runner():
    path = CAPTURE_DIR / "run_capture.py"
    spec = importlib.util.spec_from_file_location(
        "ch09_capture_runner",
        path,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_outbound_rule_matches_staged_listing():
    assert (HERE / "AGENTS.md").read_text(encoding="utf-8") == (
        "## Outbound HTTP\n\n"
        "- Feature modules route outbound HTTP through\n"
        "  http_client.call.\n"
        "- Feature modules do not import a transport directly.\n"
        "- Tests inject a transport and make no live calls.\n"
        "- test_house_rules.py enforces the import boundary.\n"
    )


def test_green_alert_keeps_the_captured_interface_repair():
    top_level = (HERE / "alerts.py").read_text(encoding="utf-8")
    captured_after = (
        CAPTURE_DIR / "after" / "alerts.py"
    ).read_text(encoding="utf-8")
    required_lines = (
        "from http_client import call",
        'response = call("POST", ALERTS_URL, json={"text": message})',
        "return response.status < 400",
    )

    for line in required_lines:
        assert line in top_level
        assert line in captured_after


def test_parity_map_covers_each_staged_code_surface():
    parity = (HERE / "parity.md").read_text(encoding="utf-8")

    for token in (
        "Listing 9.1 outbound HTTP rule",
        "Listing 9.2 `Response` and `call` interface",
        "Listing 9.3 illustrative skill shape",
        "Listing 9.4 retrieve, preserve provenance, then inject",
        "MCP resources, prompts, and tools",
        "Lethal-trifecta containment",
        "Real shared-client session",
    ):
        assert token in parity


def test_replay_and_collection_are_package_local():
    runner = (
        CAPTURE_DIR / "run_capture.py"
    ).read_text(encoding="utf-8")
    pytest_config = (HERE / "pytest.ini").read_text(encoding="utf-8")

    for forbidden in (
        "REPO_ROOT",
        "CANONICAL_DIR",
        "CANONICAL_CHAPTER",
        "parents[5]",
    ):
        assert forbidden not in runner
    assert "norecursedirs = captures" in pytest_config
    assert "test_package_parity.py" in pytest_config


def test_completed_review_state_requires_active_pass_receipt():
    runner = load_capture_runner()
    metadata = json.loads(
        (CAPTURE_DIR / "metadata.json").read_text(encoding="utf-8")
    )

    assert runner.verify_review_state(metadata) == "PASS"

    invalid = deepcopy(metadata)
    invalid["review_state"]["active_review"]["status"] = "pending"
    with pytest.raises(RuntimeError, match="completed status"):
        runner.verify_review_state(invalid)

    invalid = deepcopy(metadata)
    invalid["review_state"]["active_review"]["verdict"] = "Fail"
    with pytest.raises(RuntimeError, match="Pass verdict"):
        runner.verify_review_state(invalid)

    invalid = deepcopy(metadata)
    invalid["review_state"]["active_review"][
        "blocking_findings"
    ] = ["unresolved finding"]
    with pytest.raises(RuntimeError, match="retains blocking findings"):
        runner.verify_review_state(invalid)

    invalid = deepcopy(metadata)
    invalid["review_state"]["active_review"]["artifact"] = "pending"
    with pytest.raises(RuntimeError, match="artifact cannot be pending"):
        runner.verify_review_state(invalid)

    invalid = deepcopy(metadata)
    invalid["review_state"]["active_review"]["artifact"] = "README.md"
    with pytest.raises(RuntimeError, match="under evidence"):
        runner.verify_review_state(invalid)

    invalid = deepcopy(metadata)
    invalid["review_state"]["active_review"][
        "artifact_checksum"
    ] = "0" * 64
    with pytest.raises(RuntimeError, match="checksum drifted"):
        runner.verify_review_state(invalid)


def test_disposable_work_is_cleaned_after_failure():
    runner = load_capture_runner()
    runner.verify_no_work_directories()
    work = None

    with pytest.raises(RuntimeError, match="intentional cleanup probe"):
        with runner.disposable_work() as work:
            raise RuntimeError("intentional cleanup probe")

    assert work is not None and not work.exists()
    runner.verify_no_work_directories()
