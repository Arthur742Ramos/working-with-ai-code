"""Negative controls for the separate, non-recording behavioral verifier.

Run explicitly: python3 -m unittest -v test_verify_behavior
The sealed four-test package suite and its discovery settings are unchanged.
"""

import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

import verify_behavior as check


class BehavioralReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = check.load_runner()

    def result(self, name, output=None, status=None):
        path, exit_path = self.runner.evidence_paths(name)
        return SimpleNamespace(
            stdout=path.read_text() if output is None else output,
            returncode=int(exit_path.read_text()) if status is None else status,
        )

    def test_retained_output_and_exact_missing_caret_are_accepted(self):
        red = self.result("focused-red")
        check.compare_result(self.runner, "focused-red", red)
        self.assertEqual(red.stdout.count(check.CARET_CONTEXT), 1)
        red.stdout = red.stdout.replace(check.CARET_CONTEXT, check.WITHOUT_CARET)
        check.compare_result(self.runner, "focused-red", red)

    def test_changed_failure_value_is_rejected(self):
        red = self.result("focused-red")
        red.stdout = red.stdout.replace("1.0 != 0.5", "1.0 != 0.25")
        with self.assertRaisesRegex(RuntimeError, "output drifted"):
            check.compare_result(self.runner, "focused-red", red)
        with self.assertRaisesRegex(RuntimeError, "required denominator"):
            self.runner.verify_red(red)

    def test_other_output_and_caret_changes_are_rejected(self):
        original = self.result("focused-red").stdout
        for output in (
            original + "unexpected diagnostic\n",
            original.replace("line 21", "line 22"),
            original.replace("self.assertEqual(rate, 0.50)", "self.assertEqual(rate, 0.25)"),
            original.replace("~~~~~~~~~~~~~~~~^^^^^^^^^^^^", "^^^^^^^^"),
            original.replace(check.CARET_CONTEXT, check.CARET_CONTEXT + check.CARET_CONTEXT),
            original.replace("FAILED (failures=1)", "FAILED (failures=2)"),
        ):
            with self.subTest(output=output):
                with self.assertRaisesRegex(RuntimeError, "output drifted"):
                    check.compare_result(self.runner, "focused-red", self.result("focused-red", output))

    def test_wrong_red_status_and_setup_failure_are_rejected(self):
        for status in (0, 2):
            with self.subTest(status=status):
                with self.assertRaisesRegex(RuntimeError, "exit status drifted"):
                    check.compare_result(self.runner, "focused-red", self.result("focused-red", status=status))
        for output in ("ImportError: missing dependency\n", self.result("focused-red").stdout + "ImportError\n"):
            with self.subTest(output=output):
                with self.assertRaises(RuntimeError):
                    self.runner.verify_red(self.result("focused-red", output))
                with self.assertRaises(RuntimeError):
                    check.compare_result(self.runner, "focused-red", self.result("focused-red", output))

    def test_wrong_green_count_name_and_exit_are_rejected(self):
        green = self.result("broader-green")
        for output, status in (
            (green.stdout.replace("Ran 4 tests", "Ran 3 tests"), 0),
            (green.stdout.replace("test_pending_attempts_are_excluded", "test_unrelated"), 0),
            (green.stdout.replace(" ... ok", " ... skipped 'not run'", 1), 0),
            (green.stdout, 1),
            (green.stdout + check.CARET_CONTEXT, 0),
        ):
            with self.subTest(output=output, status=status):
                with self.assertRaises(RuntimeError):
                    check.compare_result(self.runner, "broader-green", self.result("broader-green", output, status))

    def test_runner_drift_is_rejected_before_import(self):
        with tempfile.TemporaryDirectory() as directory:
            capture = Path(directory)
            shutil.copy2(check.CAPTURE / "run_capture.py", capture / "run_capture.py")
            with (capture / "run_capture.py").open("a") as stream:
                stream.write("\nraise AssertionError('must not be imported')\n")
            with self.assertRaisesRegex(RuntimeError, "runner checksum drifted"):
                check.load_runner(capture)

    def test_patch_evidence_and_metadata_drift_are_rejected(self):
        mutations = (
            "patches/production.diff",
            "evidence/focused-red.txt",
            "evidence/focused-red.exit-status",
            "evidence/independent-review.md",
            "metadata.json",
        )
        for relative in mutations:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                chapter = Path(directory) / "ch12"
                shutil.copytree(check.ROOT, chapter)
                capture = chapter / "captures/benchmark_denominator"
                path = capture / relative
                if relative == "metadata.json":
                    path.write_text(path.read_text().replace('"verdict": "Pass"', '"verdict": "Fail"'))
                else:
                    path.write_bytes(path.read_bytes() + b"tampered\n")
                with self.assertRaises(RuntimeError):
                    check.load_runner(capture).verify_inputs(check_evidence=True)

    def test_wrong_after_state_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "workflow_metrics.py"
            source.write_text("# wrong after-state\n")
            with self.assertRaisesRegex(RuntimeError, "after-state checksum drifted"):
                check.verify_after_state(self.runner, source)

    def test_record_mode_is_forbidden(self):
        result = subprocess.run(
            [sys.executable, "-B", str(check.ROOT / "verify_behavior.py"), "--record"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --record", result.stdout)

    def test_replay_preserves_every_chapter_file(self):
        def hashes():
            return {str(path.relative_to(check.ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in check.ROOT.rglob("*") if path.is_file()}
        before = hashes()
        result = check.verify_behavior()
        self.assertEqual(result, {
            "focused_red": 1, "patch": 0, "focused_green": 0,
            "broader_green": 0, "maintained_green": 0,
        })
        self.assertEqual(hashes(), before)


if __name__ == "__main__":
    unittest.main()
