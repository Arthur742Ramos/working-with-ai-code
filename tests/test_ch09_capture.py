"""Regression checks for timing-tolerant, content-strict capture publication."""

import importlib.util
from pathlib import Path
import os
import runpy
import shutil
import subprocess
import sys
from types import SimpleNamespace

import pytest


CAPTURE = Path(__file__).resolve().parents[1] / "ch09/captures/house_rule_seam"


def load_runner():
    spec = importlib.util.spec_from_file_location("house_rule_runner", CAPTURE / "run_capture.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    return runner


def publication_results(runner):
    metadata = runner.load_metadata()
    results = {}
    for key in ("red", "focused_green", "broader_green"):
        output = (CAPTURE / metadata[key]["output_file"]).read_text(encoding="utf-8")
        results[key] = SimpleNamespace(stdout=runner.stable_output(output).replace("<TIME>", "123.45"))
    return metadata, results


def test_publication_accepts_only_elapsed_time_changes():
    runner = load_runner()
    metadata, results = publication_results(runner)
    runner.verify_publication_evidence(metadata, results)
    runner.verify_publication_evidence(metadata)


@pytest.mark.parametrize("phase", ["red", "focused_green", "broader_green"])
def test_publication_rejects_changed_behavior(phase):
    runner = load_runner()
    metadata, results = publication_results(runner)
    results[phase].stdout = results[phase].stdout.replace("failed", "passed").replace("1 passed", "2 passed").replace("10 passed", "11 passed")
    with pytest.raises(RuntimeError, match=f"reproduce {phase} evidence"):
        runner.verify_publication_evidence(metadata, results)


def test_record_rejects_unpublished_output_before_writing(monkeypatch):
    runner = load_runner()
    metadata, results = publication_results(runner)
    monkeypatch.setattr(runner, "load_metadata", lambda: metadata)
    for name in ("verify_metadata", "verify_fixture_and_package", "verify_origin_provenance", "verify_patch", "verify_records", "require_semantics"):
        monkeypatch.setattr(runner, name, lambda *args: None)
    monkeypatch.setattr(runner, "verify_review_state", lambda *args: "PASS")
    monkeypatch.setattr(runner, "reset_work", lambda *args: None)
    monkeypatch.setattr(runner, "apply_patch_and_verify", lambda *args: None)
    results["red"].stdout = "unexpected changed diagnostic\n1 failed in 0.01s\n"
    sequence = iter([results["red"], results["focused_green"], results["broader_green"], SimpleNamespace(stdout="28 passed", returncode=0)])
    monkeypatch.setattr(runner, "run_pytest", lambda *args: next(sequence))
    def unexpected_write(*args):
        pytest.fail("record mode wrote before publication validation")
    monkeypatch.setattr(runner, "record_results", unexpected_write)
    monkeypatch.setattr("sys.argv", ["run_capture.py", "--record"])
    with pytest.raises(RuntimeError, match="reproduce red evidence"):
        runner.main()
    runner.verify_no_work_directories()


def test_package_run_clears_capture_environment(monkeypatch):
    runner = load_runner()
    monkeypatch.setenv("PYTHONPATH", "before")
    monkeypatch.setenv("HOUSE_RULE_ROOT", "before")
    monkeypatch.setenv("PYTEST_ADDOPTS", "--invalid-option")
    observed = {}
    monkeypatch.setattr(runner.subprocess, "run", lambda *args, **kwargs: observed.update(kwargs))
    runner.run_pytest(CAPTURE.parents[1], None, None)
    assert "PYTHONPATH" not in observed["env"]
    assert "HOUSE_RULE_ROOT" not in observed["env"]
    assert observed["env"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
    assert observed["env"]["PYTEST_ADDOPTS"] == ""


def test_readable_retriever_keeps_ranking_and_stable_ties(capsys):
    demo = runpy.run_path(str(CAPTURE.parents[1] / "teaching/retrieval_demo.py"))
    assert "required-source recall@2: 1.0" in capsys.readouterr().out
    Chunk = demo["Chunk"]
    chunks = [Chunk("first", "today", "source", "HTTP"), Chunk("second", "today", "source", "HTTP"), Chunk("other", "today", "source", "database")]
    assert [chunk.source_id for chunk in demo["retrieve"]("HTTP", chunks, 2)] == ["first", "second"]


@pytest.mark.skipif(os.name == "nt", reason="Historical traceback evidence was captured on POSIX")
def test_record_then_replay_in_disposable_package(tmp_path):
    package = tmp_path / "ch09"
    shutil.copytree(CAPTURE.parents[1], package, ignore=shutil.ignore_patterns("__pycache__", ".work*"))
    capture = package / "captures/house_rule_seam"
    environment = os.environ.copy()
    environment.update(PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    for options in (["--record"], []):
        result = subprocess.run([sys.executable, str(capture / "run_capture.py"), *options], cwd=package, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        assert result.returncode == 0, result.stdout
        assert "RED EXIT: 1" in result.stdout
        assert "PACKAGE GREEN EXIT: 0" in result.stdout
        assert list(capture.glob(".work-*")) == []
