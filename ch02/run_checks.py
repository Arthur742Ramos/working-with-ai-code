"""Replay the frozen capture, then verify the follow-on fixture correction."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CORRECTION = ROOT / "corrections" / "retry_feedback"
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
ENV.pop("PYTHONPATH", None)


def run(args, cwd, expect_failure=False):
    result = subprocess.run(
        [sys.executable, "-B", *args], cwd=cwd, env=ENV,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout, end="", flush=True)
    if expect_failure:
        if result.returncode != 1 or "AssertionError not raised" not in result.stdout:
            raise RuntimeError("regression did not fail for the original defect")
    elif result.returncode:
        raise RuntimeError(f"verification failed: {args}")


def main():
    manifest = json.loads((CORRECTION / "historical-sha256.json").read_text())
    for relative, expected in manifest.items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"historical file changed: {relative}")
    ignore = shutil.ignore_patterns(
        "corrections", "__pycache__", ".pytest_cache", "*.pyc",
        ".work", ".package-work", "pr_description.json",
    )
    with tempfile.TemporaryDirectory(prefix="ch02-capture-") as directory:
        historical = Path(directory) / "ch02"
        shutil.copytree(ROOT, historical, ignore=ignore)
        for source in (CORRECTION / "historical").iterdir():
            shutil.copy2(source, historical / source.name)
        print("HISTORICAL CAPTURE ONLY: its receipt does not certify the follow-on fix", flush=True)
        run(["captures/pr_generator_retry_wiring/run_capture.py"], historical)
        # The new negative case must expose the old fixture's actual defect.
        print("FOLLOW-ON REGRESSION: expected failure against the original fixture", flush=True)
        shutil.copy2(ROOT / "test_pr_generator.py", historical)
        run(["-m", "unittest", "test_pr_generator.LocalFixtureTests."
             "test_repeated_diff_is_not_validation_feedback"],
            historical, expect_failure=True)
    print("CURRENT PACKAGE: corrected fixture and full regression suite", flush=True)
    run(["test_pr_generator.py"], ROOT)
    print("PASS: frozen historical replay and follow-on fixture correction")


if __name__ == "__main__":
    main()
