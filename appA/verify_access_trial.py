"""Replay the printed access trial in a temporary copy."""

from pathlib import Path
import subprocess
import sys
import tempfile

FIXTURE = Path(__file__).resolve().parent / "access_trial"
REPAIRED_STORE = '''JOBS = (
    {"id": "job-1", "owner": "u1", "status": "ready"},
    {"id": "job-2", "owner": "u2", "status": "queued"},
)


def find_job(actor_id, job_id):
    for job in JOBS:
        if job["id"] == job_id and job["owner"] == actor_id:
            return job.copy()
    return None
'''
REPAIRED_SERVICE = '''from store import find_job


def get_job(actor_id, job_id):
    return find_job(actor_id, job_id)
'''


def run(work, *args):
    return subprocess.run(
        [sys.executable, "-B", *args], cwd=work, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )


def main():
    with tempfile.TemporaryDirectory(prefix="access-trial-") as directory:
        work = Path(directory)
        for name in ("store.py", "service.py", "test_access.py"):
            (work / name).write_bytes((FIXTURE / name).read_bytes())
        tests = (work / "test_access.py").read_bytes()
        red = run(work, "-m", "unittest", "-v", "test_access")
        assert red.returncode == 1, red.stdout
        assert "Ran 4 tests" in red.stdout, red.stdout
        assert "FAILED (failures=1)" in red.stdout, red.stdout
        assert "test_another_owner_cannot_read_job" in red.stdout, red.stdout
        print("STARTING FIXTURE: 3 passed, 1 expected failure")
        (work / "store.py").write_text(REPAIRED_STORE)
        (work / "service.py").write_text(REPAIRED_SERVICE)
        assert (work / "test_access.py").read_bytes() == tests
        green = run(work, "-m", "unittest", "-v", "test_access")
        assert green.returncode == 0 and "Ran 4 tests" in green.stdout, green.stdout
        extra = run(work, "-c", 'from service import get_job; '
                    'assert get_job("u1", "job-2") is None')
        assert extra.returncode == 0, extra.stdout
        print("REFERENCE REPAIR: 4 passed; opposite-owner check passed")


if __name__ == "__main__":
    main()
