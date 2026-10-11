"""Capture replay controls formatting without weakening artifact checks."""

import importlib.util
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = [
    "ch08/captures/lost_cent_allocation",
    "ch09/captures/house_rule_seam",
    "ch11/captures/deployment_policy_value",
]


def load_runner(capture):
    spec = importlib.util.spec_from_file_location("capture_runner", ROOT / capture / "run_capture.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    return runner


@pytest.mark.parametrize("capture", CAPTURES)
def test_replay_controls_inherited_pytest_formatting(capture, monkeypatch):
    runner = load_runner(capture)
    for name, value in (("CI", "true"), ("BUILD_NUMBER", "123"), ("COLUMNS", "20"), ("PYTEST_ADDOPTS", "-vv --invalid-option")):
        monkeypatch.setenv(name, value)
    observed = {}
    monkeypatch.setattr(runner.subprocess, "run", lambda *args, **kwargs: observed.update(kwargs))
    if capture.startswith("ch09"):
        runner.run_pytest(ROOT / "ch09", None, None)
    else:
        runner.run_command(["python", "-m", "pytest"], ROOT)
    environment = observed["env"]
    assert "CI" not in environment
    assert "BUILD_NUMBER" not in environment
    assert environment["COLUMNS"] == "80"
    assert environment["PYTEST_ADDOPTS"] == ""
    assert environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"


def test_original_allocation_patch_produces_exact_after_state(tmp_path):
    runner = load_runner(CAPTURES[0])
    original_patch = runner.PATCH_FILE.read_bytes()
    shutil.copyfile(runner.BEFORE_SOURCE, tmp_path / "allocation.py")
    runner.verify_static_inputs()
    runner.apply_patch(tmp_path)
    assert (tmp_path / "allocation.py").read_bytes() == runner.AFTER_SOURCE.read_bytes()
    assert runner.PATCH_FILE.read_bytes() == original_patch


def test_allocation_patch_checksum_rejects_artifact_drift(tmp_path, monkeypatch):
    runner = load_runner(CAPTURES[0])
    patch = tmp_path / "modified.patch"
    patch.write_bytes(runner.PATCH_FILE.read_bytes() + b"\n")
    monkeypatch.setattr(runner, "EXPECTED_SHA256", {patch: runner.EXPECTED_SHA256[runner.PATCH_FILE]})
    with pytest.raises(SystemExit, match="checksum drift"):
        runner.verify_static_inputs()

