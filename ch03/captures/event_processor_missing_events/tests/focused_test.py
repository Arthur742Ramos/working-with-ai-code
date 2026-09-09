"""Focused checks for the missing-events input contract."""
import importlib.util
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

EXPECTED_ERROR = (
    "input must be an object with an 'events' key"
)
MISSING_TEST = (
    "test_missing_events_collection_raises_value_error"
)
EMPTY_TEST = (
    "test_explicit_empty_events_is_not_missing"
)


def load_module(module_path):
    spec = importlib.util.spec_from_file_location(
        "captured_event_processor",
        module_path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def invoke(module, input_path, output_path):
    return module.process_events(
        input_path,
        output_path,
        datetime(2024, 1, 1),
        datetime(2024, 1, 2),
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
        observed = f"ValueError: {exc}"
        expected = f"ValueError: {EXPECTED_ERROR}"
        if str(exc) == EXPECTED_ERROR:
            return True, [
                f"PASS: {MISSING_TEST}",
                f"observed: {observed}",
            ]
        return False, [
            f"FAIL: {MISSING_TEST}",
            f"expected: {expected}",
            f"observed: {observed}",
        ]
    except Exception as exc:
        return False, [
            f"FAIL: {MISSING_TEST}",
            "expected: ValueError: " + EXPECTED_ERROR,
            "observed: " + f"{type(exc).__name__}: {exc}",
        ]
    return False, [
        f"FAIL: {MISSING_TEST}",
        "expected: ValueError: " + EXPECTED_ERROR,
        "observed: no exception",
    ]


def check_explicit_empty_events(module, tmp_path):
    input_path = tmp_path / "empty.json"
    output_path = tmp_path / "empty-output.json"
    input_path.write_text(
        json.dumps({"events": []}),
        encoding="utf-8",
    )
    try:
        invoke(module, input_path, output_path)
    except ZeroDivisionError:
        return True, [
            f"PASS: {EMPTY_TEST}",
            "observed: reached later empty-result arithmetic",
        ]
    except Exception as exc:
        return False, [
            f"FAIL: {EMPTY_TEST}",
            "expected: explicit empty events to reach later "
            "empty-result arithmetic",
            "observed: " + f"{type(exc).__name__}: {exc}",
        ]
    return False, [
        f"FAIL: {EMPTY_TEST}",
        "expected: explicit empty events to reach later "
        "empty-result arithmetic",
        "observed: no exception",
    ]


def main():
    if len(sys.argv) != 2:
        print("usage: focused_test.py EVENT_PROCESSOR_PATH")
        return 2

    module = load_module(Path(sys.argv[1]))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        results = [
            check_missing_events(module, tmp_path),
            check_explicit_empty_events(module, tmp_path),
        ]

    failures = 0
    for passed, lines in results:
        print("\n".join(lines))
        if not passed:
            failures += 1
    if failures:
        print(f"{failures} failed, {len(results) - failures} passed")
        return 1
    print(f"{len(results)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
