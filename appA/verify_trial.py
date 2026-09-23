"""Replay the Appendix A parser trial without changing the printed fixtures."""

from pathlib import Path
import subprocess
import sys
import tempfile


FIXTURE = Path(__file__).resolve().parent
REPAIRED = '''def parse_count(text: str) -> int:
    value = int(text)
    if value < 0:
        raise ValueError("count must be non-negative")
    return value
'''
TESTS = ("test_positive", "test_zero", "test_non_integer", "test_negative")


def run_tests(work: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "-v", "test_parser"],
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def require_result(
    result: subprocess.CompletedProcess[str],
    status: int,
    expected: tuple[str, ...],
    phase: str,
) -> None:
    if result.returncode != status or any(
        text not in result.stdout for text in expected
    ):
        raise RuntimeError(f"{phase} did not match the expected result:\n{result.stdout}")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="appendix-a-trial-") as directory:
        work = Path(directory)
        for name in ("parser.py", "test_parser.py"):
            (work / name).write_bytes((FIXTURE / name).read_bytes())
        tests = (work / "test_parser.py").read_bytes()

        red = run_tests(work)
        require_result(
            red,
            1,
            (
                "Ran 4 tests",
                "FAILED (failures=1)",
                "ValueError not raised",
                "test_negative (test_parser.CountTests.test_negative) ... FAIL",
                *(f"{name} (test_parser.CountTests.{name}) ... ok" for name in TESTS[:-1]),
            ),
            "starting fixture",
        )
        print("STARTING FIXTURE: 3 passed, 1 expected failure")

        (work / "parser.py").write_text(REPAIRED, encoding="utf-8")
        if (work / "test_parser.py").read_bytes() != tests:
            raise RuntimeError("reference repair changed the printed tests")
        green = run_tests(work)
        require_result(
            green,
            0,
            ("Ran 4 tests", "OK", *(
                f"{name} (test_parser.CountTests.{name}) ... ok" for name in TESTS
            )),
            "reference repair",
        )
        print("REFERENCE REPAIR: 4 passed with unchanged tests")

        extra = subprocess.run(
            [sys.executable, "-B", "-c",
             'from parser import parse_count; parse_count("-2")'],
            cwd=work,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require_result(
            extra,
            1,
            ("ValueError: count must be non-negative",),
            "independent negative input",
        )
        print("INDEPENDENT NEGATIVE INPUT: rejected")


if __name__ == "__main__":
    main()
