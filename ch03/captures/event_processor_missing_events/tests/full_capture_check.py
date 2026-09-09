"""Broader check for the bounded missing-events repair."""
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
HAPPY_TEST = "test_existing_happy_path_still_works"


def load_module(module_path):
    spec = importlib.util.spec_from_file_location(
        "captured_event_processor",
        module_path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_missing_events(module, tmp_path):
    input_path = tmp_path / "missing.json"
    output_path = tmp_path / "missing-output.json"
    input_path.write_text(
        json.dumps({"not_events": []}),
        encoding="utf-8",
    )
    try:
        module.process_events(
            input_path,
            output_path,
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
        )
    except ValueError as exc:
        if str(exc) == EXPECTED_ERROR:
            return
        raise AssertionError(
            f"unexpected ValueError: {exc}"
        ) from exc
    except Exception as exc:
        raise AssertionError(
            "missing events raised "
            f"{type(exc).__name__}: {exc}"
        ) from exc
    raise AssertionError(
        "missing events did not raise ValueError"
    )


def check_explicit_empty_events(module, tmp_path):
    input_path = tmp_path / "empty.json"
    output_path = tmp_path / "empty-output.json"
    input_path.write_text(
        json.dumps({"events": []}),
        encoding="utf-8",
    )
    try:
        module.process_events(
            input_path,
            output_path,
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
        )
    except ZeroDivisionError:
        return
    except Exception as exc:
        raise AssertionError(
            "explicit empty events were rejected before "
            "later arithmetic: "
            f"{type(exc).__name__}: {exc}"
        ) from exc
    raise AssertionError(
        "explicit empty events did not reach later arithmetic"
    )


def check_happy_path(module, tmp_path):
    input_path = tmp_path / "valid.json"
    output_path = tmp_path / "valid-output.json"
    input_path.write_text(
        json.dumps({
            "events": [{
                "timestamp": "2024-01-01 12:00:00",
                "user_id": "user-1",
                "type": "view",
            }],
        }),
        encoding="utf-8",
    )
    summary = module.process_events(
        input_path,
        output_path,
        datetime(2024, 1, 1),
        datetime(2024, 1, 2),
    )
    expected = {
        "total_events": 1,
        "unique_users": 1,
        "per_user": {
            "user-1": {
                "count": 1,
                "types": ["view"],
            },
        },
        "avg_events": 1.0,
    }
    if summary != expected:
        raise AssertionError(
            f"unexpected summary: {summary!r}"
        )
    written = json.loads(
        output_path.read_text(encoding="utf-8")
    )
    if written != expected:
        raise AssertionError(
            f"unexpected output: {written!r}"
        )


def main():
    if len(sys.argv) != 2:
        print(
            "usage: full_capture_check.py "
            "EVENT_PROCESSOR_PATH"
        )
        return 2

    module = load_module(Path(sys.argv[1]))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        try:
            check_missing_events(module, tmp_path)
            print(f"PASS: {MISSING_TEST}")
            check_explicit_empty_events(module, tmp_path)
            print(f"PASS: {EMPTY_TEST}")
            check_happy_path(module, tmp_path)
            print(f"PASS: {HAPPY_TEST}")
        except AssertionError as exc:
            print(f"FAIL: {exc}")
            return 1
    print("3 passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
