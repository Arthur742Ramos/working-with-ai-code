"""Replay the frozen capture, then verify the separately recorded logging repair."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CAPTURE = Path("captures/incident_orphan_product_policy")
CORRECTION = Path("corrections/missing_product_logging")
MANIFEST = CORRECTION / "manifest.json"
RUNTIME_FILES = {"shop.db", "server.log"}
RUNTIME_DIRS = {".work", ".pytest_cache", "__pycache__"}


def package_checksums():
    checksums = {}
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if (
            not path.is_file()
            or relative == MANIFEST
            or path.name in RUNTIME_FILES
            or path.suffix == ".pyc"
            or any(part in RUNTIME_DIRS for part in relative.parts)
        ):
            continue
        checksums[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(checksums.items()))


def verify_publication():
    metadata = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    if package_checksums() != metadata["publication_sha256"]:
        raise RuntimeError("current publication inventory or checksum drift")


def run(command, cwd, expected=0):
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(
        command, cwd=cwd, env=environment, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    if result.returncode != expected:
        raise RuntimeError(
            "unexpected exit status for %r: expected %d, observed %d\n%s"
            % (command, expected, result.returncode, result.stdout)
        )
    return result.stdout


def apply_patch(root, path):
    run(["patch", "-p1", "-i", str(path)], root)


def stage_history(destination):
    """Restore the exact old inventory without editing the original capture."""
    metadata = json.loads((ROOT / CAPTURE / "metadata.json").read_text(encoding="utf-8"))
    replacements = {
        "README.md": CORRECTION / "before/README.md",
        "tests/test_capture_inventory.py": CORRECTION / "before/test_capture_inventory.py",
        "server.py": CAPTURE / "before/server.py",
    }
    for name in metadata["package_inventory"]:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / replacements.get(name, Path(name)), target)
    apply_patch(destination, ROOT / CAPTURE / "patches/missing-product-policy.diff")


def check_logging(root, stem, expected):
    output = run([sys.executable, str(ROOT / "tests/test_request_logging.py"), str(root)], root, expected)
    evidence = ROOT / CORRECTION / "evidence"
    if output != (evidence / (stem + ".txt")).read_text(encoding="utf-8"):
        raise RuntimeError("follow-on %s output changed" % stem)
    if expected != int((evidence / (stem + ".exitstatus")).read_text()):
        raise RuntimeError("follow-on %s exit status changed" % stem)
    print(stem.upper())
    print(output, end="")
    print("EXIT STATUS: %d" % expected)


def main():
    verify_publication()
    before = package_checksums()
    manifest_before = (ROOT / MANIFEST).read_bytes()
    with tempfile.TemporaryDirectory(prefix="ch05-replay-") as temporary:
        history = Path(temporary) / "historical"
        stage_history(history)
        print("HISTORICAL CAPTURE ONLY (the old receipt does not certify the follow-on repair)")
        print(run([sys.executable, str(history / CAPTURE / "run_capture.py")], history), end="")
        print(run([sys.executable, str(history / "tests/test_capture_inventory.py")], history), end="")
        check_logging(history, "logging-red", 1)

        corrected = Path(temporary) / "corrected"
        corrected.mkdir()
        shutil.copy2(history / "server.py", corrected / "server.py")
        apply_patch(corrected, ROOT / CORRECTION / "request-logging.diff")
        if (corrected / "server.py").read_bytes() != (ROOT / "server.py").read_bytes():
            raise RuntimeError("follow-on patch does not reproduce the current server")
        shutil.copy2(ROOT / "seed.py", corrected / "seed.py")
        for name in ("test_orphan_policy.py", "test_orphan_policy_broader.py"):
            print(run([sys.executable, str(ROOT / "tests" / name), str(corrected)], corrected), end="")
        check_logging(corrected, "logging-green", 0)
        print(run([sys.executable, str(ROOT / "tests/test_capture_inventory.py")], ROOT), end="")

    verify_publication()
    if before != package_checksums() or manifest_before != (ROOT / MANIFEST).read_bytes():
        raise RuntimeError("maintained files changed during replay")
    print("CURRENT PUBLICATION: follow-on patch, logging checks and unchanged behavior verified")
    print("PROVENANCE: historical capture and current publication verified separately; no evidence rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
