"""Exercise reader-visible red/green states in isolated copies.

Invoke explicitly from the repository root; chapter pytest configurations keep
their historical final-package test counts and capture evidence unchanged.
"""

import os
from pathlib import Path
import runpy
import re
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
IGNORED = shutil.ignore_patterns("__pycache__", ".pytest_cache", ".venv", ".work*")


def run(cwd, *args, status=0, env=None):
    environment = os.environ.copy()
    environment.update(PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTEST_ADDOPTS="")
    environment.pop("PYTHONPATH", None)
    environment.pop("HOUSE_RULE_ROOT", None)
    if env:
        environment.update(env)
    result = subprocess.run(args, cwd=cwd, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    assert result.returncode == status, result.stdout
    return result.stdout


def pytest_at(cwd, *targets, status=0, env=None):
    return run(cwd, sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *targets, status=status, env=env)


@pytest.mark.parametrize("chapter,count", [("ch07", 13), ("ch08", 10), ("ch09", 28), ("ch10", 57), ("ch11", 29)])
def test_final_package_is_self_contained(tmp_path, chapter, count):
    package = tmp_path / chapter
    shutil.copytree(ROOT / chapter, package, ignore=IGNORED)
    assert f"{count} passed" in pytest_at(package)


def test_ch07_documented_real_paths_preserve_red_and_green():
    capture = ROOT / "ch07/captures/strict_float_validator"
    red = run(capture, sys.executable, "tests/focused_test.py", "before/validator.py", status=1)
    assert "5 failed" in red
    green = run(capture, sys.executable, "tests/focused_test.py", "../../validator.py")
    assert green.count("PASS:") == 5
    assert "0 failed" in green
    assert "9 passed" in pytest_at(capture / "../..", "test_validator.py")


def test_ch08_readable_draft_still_demonstrates_lost_cent():
    draft = runpy.run_path(str(ROOT / "ch08/teaching/draft_allocation.py"))
    assert draft["allocate"](100, [1, 1, 1]) == [33, 33, 33]
    with pytest.raises(AssertionError):
        draft["smoke_test"](100, [1, 1, 1])


def test_ch09_direct_before_and_after_checks_have_explicit_roots():
    capture = ROOT / "ch09/captures/house_rule_seam"
    before = {"PYTHONPATH": "before", "HOUSE_RULE_ROOT": "before"}
    focused = pytest_at(capture, "tests/test_alerts.py::test_send_alert_routes_through_house_client", status=1, env=before)
    assert "1 failed" in focused
    assert "send_alert must route method, URL, and JSON" in focused
    assert "4 failed, 6 passed" in pytest_at(capture, "tests", status=1, env=before)
    after = {"PYTHONPATH": "after", "HOUSE_RULE_ROOT": "after"}
    assert "10 passed" in pytest_at(capture, "tests", env=after)


def test_ch11_focused_target_uses_staged_configuration(tmp_path):
    capture = ROOT / "ch11/captures/deployment_policy_value"
    for source in (capture / "before/deployment_guard.py", capture / "before/deployment.json", capture / "tests/test_deployment_policy.py"):
        shutil.copy2(source, tmp_path / source.name)
    target = "test_deployment_policy.py::test_schema_valid_deployment_satisfies_policy"
    red = pytest_at(tmp_path, target, status=1)
    assert "1 failed" in red and "AssertionError" in red
    shutil.copy2(ROOT / "ch11/deployment.json", tmp_path / "deployment.json")
    assert "1 passed" in pytest_at(tmp_path, target)


@pytest.mark.parametrize("patch,target,red_count,green_count", [
    ("service-slice-before.patch", "tests/test_service.py", 14, 14),
    ("sqlite-row-before.patch", "tests/test_sqlite_repository.py::test_get_for_user_maps_unsnoozed_reminder", 1, 1),
])
def test_ch10_walkthrough_patch_from_chapter_directory(tmp_path, patch, target, red_count, green_count):
    package = tmp_path / "ch10"
    shutil.copytree(ROOT / "ch10", package, ignore=IGNORED)
    run(tmp_path, "git", "init", "--quiet")
    # Match the published Git blob bytes even with a Windows global Git default.
    run(tmp_path, "git", "config", "core.autocrlf", "false")
    for relative in ("reminders/service.py", "tests/test_service.py", "captures/service-slice-before.patch"):
        path = package / relative
        path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    run(tmp_path, "git", "add", "ch10")
    run(tmp_path, "git", "-c", "user.name=Reader workflow check", "-c", "user.email=reader@example.invalid", "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Reader baseline")
    # Resolve the same root used by the README before applying ch10/... paths.
    repo_root = Path(run(package, "git", "rev-parse", "--show-toplevel").strip())
    run(repo_root, "git", "switch", "-c", "reader-controlled-repair")
    run(repo_root, "git", "apply", "--unidiff-zero", f"ch10/captures/{patch}")
    red = pytest_at(package, target, status=1)
    assert f"{red_count} failed" in red
    source = "reminders/service.py" if patch.startswith("service") else "reminders/repository.py"
    run(package, "git", "restore", source)
    assert f"{green_count} passed" in pytest_at(package, target)
    if patch.startswith("service"):
        run(package, "git", "restore", "tests/test_service.py")
    assert run(repo_root, "git", "status", "--short") == ""


def test_ch10_documented_batch_replay_keeps_manifest_consistent(tmp_path):
    package = tmp_path / "batch_case"
    shutil.copytree(ROOT / "ch10/batch_case", package, ignore=IGNORED)
    output = run(package, sys.executable, "replay_capture.py")
    assert "PASS: hashes, exact patch, 49 baseline, expected red, batch green, 85 final" in output


@pytest.mark.skipif(os.name == "nt", reason="POSIX shell examples run on the Linux CI runner")
@pytest.mark.parametrize("chapter", ["ch08", "ch11"])
def test_documented_isolation_block_cleans_up_and_returns(tmp_path, chapter):
    readme = (ROOT / chapter / "README.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```bash\n(.*?)```", readme, re.DOTALL)
    block = next(block for block in blocks if "package_copy=$(mktemp" in block)
    package_copies = tmp_path / "packages"
    package_copies.mkdir()
    pytest_temp = tmp_path / "pytest"
    pytest_temp.mkdir()
    run(ROOT / chapter, "bash", "-c", block + '\nexit_code=$?\ntest "$exit_code" -eq 0 && test "$PWD" = "$starting_dir"', env={"TMPDIR": str(package_copies), "PYTEST_DEBUG_TEMPROOT": str(pytest_temp), "starting_dir": str(ROOT / chapter)})
    assert list(package_copies.iterdir()) == []
