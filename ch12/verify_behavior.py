"""Non-recording behavioral replay with one documented traceback equivalence.

This is a separately maintained check, not the sealed historical replay.
It retains all other normalized output and integrity comparisons.
"""

import argparse
import hashlib
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
CAPTURE = ROOT / "captures" / "benchmark_denominator"
RUNNER_SHA256 = "fccea0c62f6903e35b6c75b1ab2d2a513412e75423ac2b7f5c56cdde068104cd"
CARET_CONTEXT = (
    "    self.assertEqual(rate, 0.50)\n"
    "    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^\n"
    "AssertionError: 1.0 != 0.5\n"
)
WITHOUT_CARET = (
    "    self.assertEqual(rate, 0.50)\n"
    "AssertionError: 1.0 != 0.5\n"
)


def load_runner(capture=CAPTURE):
    """Reject a changed historical runner before importing it."""
    path = capture / "run_capture.py"
    if hashlib.sha256(path.read_bytes()).hexdigest() != RUNNER_SHA256:
        raise RuntimeError("historical runner checksum drifted")
    spec = importlib.util.spec_from_file_location("ch12_historical_capture", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("historical runner could not be loaded")
    runner = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(runner)
    finally:
        sys.dont_write_bytecode = previous
    return runner


def output_for_comparison(runner, name, output):
    text = runner.stable_output(output)
    if name == "focused-red":
        # Only the observed caret line at this exact failing assertion is
        # optional. Other caret lines, diagnostics and source remain compared.
        text = text.replace(CARET_CONTEXT, WITHOUT_CARET, 1)
    return text


def compare_result(runner, name, result):
    output_path, status_path = runner.evidence_paths(name)
    expected = output_path.read_text(encoding="utf-8")
    status = status_path.read_text(encoding="utf-8")
    if status != f"{result.returncode}\n":
        raise RuntimeError(f"{name} exit status drifted")
    if output_for_comparison(runner, name, result.stdout) != (
        output_for_comparison(runner, name, expected)
    ):
        raise RuntimeError(f"{name} output drifted")


def verify_after_state(runner, source):
    if runner.sha256(source) != runner.EXPECTED_AFTER_SHA256:
        raise RuntimeError("patched after-state checksum drifted")
    generated = runner.generate_diff(source)
    if generated.returncode != 1:
        raise RuntimeError("machine diff did not report one change")
    if generated.stdout != runner.PATCH_PATH.read_text(encoding="utf-8"):
        raise RuntimeError("stored patch is not the exact machine diff")


def verify_behavior(capture=CAPTURE):
    runner = load_runner(capture)
    runner.verify_inputs(check_evidence=True)
    # The historical normalizer recognizes the final .work-replay component.
    # This directory is under a new system temporary root, never the capture.
    with tempfile.TemporaryDirectory(prefix="ch12-behavior-") as directory:
        work = Path(directory) / ".work-replay"
        work.mkdir()
        source = work / "workflow_metrics.py"
        shutil.copy2(runner.BEFORE_SOURCE, source)
        shutil.copy2(runner.FOCUSED_TEST, work / "test_workflow_metrics.py")
        focused = [sys.executable, "-m", "unittest", "-v", runner.FOCUSED_TARGET]
        red = runner.run(focused, work)
        runner.verify_red(red)
        compare_result(runner, "focused-red", red)

        patch = runner.run(
            ["patch", "-p1", "-i", str(runner.PATCH_PATH)], work,
        )
        if patch.returncode != 0:
            raise RuntimeError("production patch did not apply cleanly")
        compare_result(runner, "patch-apply", patch)
        verify_after_state(runner, source)

        green = runner.run(focused, work)
        runner.verify_green("focused green", green, 1)
        compare_result(runner, "focused-green", green)
        command = [sys.executable, "-m", "unittest", "-v", "test_workflow_metrics"]
        broader = runner.run(command, work)
        runner.verify_green("broader green", broader, 4)
        compare_result(runner, "broader-green", broader)

        # Run the maintained source from a temporary copy as well. No tests or
        # generated files are placed in the checked-out chapter package.
        package = Path(directory) / "maintained"
        package.mkdir()
        shutil.copy2(runner.PACKAGE_SOURCE, package / "workflow_metrics.py")
        shutil.copy2(runner.PACKAGE_TEST, package / "test_workflow_metrics.py")
        current = runner.run(command, package)
        runner.verify_green("maintained green", current, 4)
        compare_result(runner, "broader-green", current)
    runner.verify_inputs(check_evidence=True)
    return {
        "focused_red": red.returncode,
        "patch": patch.returncode,
        "focused_green": green.returncode,
        "broader_green": broader.returncode,
        "maintained_green": current.returncode,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    # No record mode or forwarding of arguments to the historical runner.
    parser.parse_args(argv)
    results = verify_behavior()
    for name, status in results.items():
        print(f"{name}: verified exit {status}")
    print("BEHAVIORAL REPLAY VERIFIED: historical inputs unchanged")
    print("COMPARISON: paths, timing and one exact denominator-assertion caret line")
    print("STRICT HISTORICAL TRANSCRIPT EQUALITY: not asserted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
