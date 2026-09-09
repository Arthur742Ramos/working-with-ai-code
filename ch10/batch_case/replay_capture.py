"""Reconstruct and repeat the capture without editing its evidence."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(args, cwd, expected=0):
    result = subprocess.run(
        args, cwd=cwd, text=True, capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if result.returncode != expected:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def main():
    manifest = json.loads(
        (ROOT / "evidence/manifest.json").read_text(),
    )
    for relative, digest in manifest["sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        if actual != digest:
            raise RuntimeError(f"hash mismatch: {relative}")
    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        shutil.copytree(ROOT / "evidence/before/reminders", work / "reminders")
        shutil.copytree(ROOT / "tests", work / "tests")
        (work / "tests/test_batch_snooze.py").unlink()
        shutil.copy2(ROOT / "pytest.ini", work)
        shutil.copy2(ROOT / "probe_atomicity.py", work)
        baseline = run([sys.executable, "-m", "pytest", "-q"], work)
        assert "49 passed" in baseline, baseline
        red = run([sys.executable, "probe_atomicity.py", "legacy"], work, 1)
        assert "batch partially committed" in red, red
        assert "('rem-1', '2030-01-02T12:15:00+00:00')" in red, red
        run(["patch", "-p1", "--batch", "-i",
             str(ROOT / "evidence/production.patch")], work)
        expected = {p.name: p.read_bytes() for p in (ROOT / "reminders").glob("*.py")}
        actual = {p.name: p.read_bytes() for p in (work / "reminders").glob("*.py")}
        assert actual == expected, "patch does not reconstruct final modules"
        shutil.copy2(ROOT / "tests/test_batch_snooze.py", work / "tests")
        green = run([sys.executable, "probe_atomicity.py", "batch"], work)
        assert "atomicity=PASS" in green, green
        suite = run([sys.executable, "-m", "pytest", "-q"], work)
        assert "85 passed" in suite, suite
    print("PASS: hashes, exact patch, 49 baseline, expected red, batch green, 85 final")


if __name__ == "__main__":
    main()
