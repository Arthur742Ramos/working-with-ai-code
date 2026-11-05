"""Run the focused checks against an event processor module."""
import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_ERROR = (
    "input must be an object with an 'events' key"
)
UTC = timezone.utc


def load_module(module_path):
    spec = importlib.util.spec_from_file_location(
        "reader_event_processor",
        module_path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def invoke(module, input_path, output_path):
    return module.process_events(
        input_path,
        output_path,
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 2, tzinfo=UTC),
    )


def check_missing_events(module, tmp_path):
    input_path = tmp_path / "missing.json"
    output_path = tmp_path / "missing-output.json"
    input_path.write_text(
        json.dumps({"not_events": []}),
        encoding="utf-8",
    )
    try:
        invoke(module, input_path, output_path)
    except ValueError as exc:
        if str(exc) == EXPECTED_ERROR:
            print(
                "PASS: "
                "test_missing_events_key_raises_exact_error"
            )
            return True
        print(f"FAIL: unexpected ValueError: {exc}")
        return False
    except Exception as exc:
        print(
            "FAIL: missing events raised "
            f"{type(exc).__name__}: {exc}"
        )
        return False
    print("FAIL: missing events did not raise ValueError")
    return False


def check_explicit_empty_events(module, tmp_path):
    input_path = tmp_path / "empty.json"
    output_path = tmp_path / "empty-output.json"
    input_path.write_text(
        json.dumps({"events": []}),
        encoding="utf-8",
    )
    try:
        summary = invoke(module, input_path, output_path)
    except Exception as exc:
        print(
            "FAIL: explicit empty events raised "
            f"{type(exc).__name__}: {exc}"
        )
        return False
    if (summary["total_events"] == 0
            and summary["avg_events"] == 0):
        print(
            "PASS: "
            "test_explicit_empty_events_has_zero_average"
        )
        return True
    print(f"FAIL: unexpected empty summary: {summary!r}")
    return False


def main():
    if len(sys.argv) != 2:
        print("usage: focused_test.py EVENT_PROCESSOR_PATH")
        return 2

    module = load_module(Path(sys.argv[1]).resolve())
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        results = [
            check_missing_events(module, tmp_path),
            check_explicit_empty_events(module, tmp_path),
        ]
    failures = results.count(False)
    if failures:
        print(f"{failures} failed, {len(results) - failures} passed")
        return 1
    print(f"{len(results)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
