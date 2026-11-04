"""Replay the historical capture, then check the current package."""

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CAPTURE = Path("captures/house_rule_seam")
HISTORY = ROOT / "corrections/guard_description/historical"
EXPECTED = {
    "README.md": (
        "2087002afcd1ff3afa1d883dbbb4a30e"
        "1425235ca8c4714072395ff019e16794"
    ),
    "test_house_rules.py": (
        "b99f48d626cacf83199fedc9cb0188ce"
        "2564fa6c365511a51cb762c8691ae75a"
    ),
}


def main():
    for name, expected in EXPECTED.items():
        actual = hashlib.sha256((HISTORY / name).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"historical file changed: {name}")

    stale = list((ROOT / CAPTURE).glob(".work-*"))
    if stale:
        raise RuntimeError(f"capture work directories already exist: {stale}")

    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    env.pop("PYTHONPATH", None)
    env.pop("PYTEST_ADDOPTS", None)
    ignore = shutil.ignore_patterns(
        "corrections", "__pycache__", ".pytest_cache", "*.pyc", ".venv"
    )
    with tempfile.TemporaryDirectory(prefix="ch09-capture-") as directory:
        historical = Path(directory) / "ch09"
        shutil.copytree(ROOT, historical, ignore=ignore)
        for name in EXPECTED:
            shutil.copy2(HISTORY / name, historical / name)
        print("HISTORICAL CAPTURE: replaying original package", flush=True)
        subprocess.run(
            [sys.executable, "-B", str(CAPTURE / "run_capture.py")],
            cwd=historical,
            env=env,
            check=True,
        )

    print("CURRENT PACKAGE: running maintained checks", flush=True)
    subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=ROOT,
        env=env,
        check=True,
    )
    print("PASS: historical replay and current package")


if __name__ == "__main__":
    main()
