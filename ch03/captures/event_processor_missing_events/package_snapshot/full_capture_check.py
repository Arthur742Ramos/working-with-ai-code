"""Run broader checks against an event processor module."""
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


def process(module, input_path, output_path, events):
    input_path.write_text(
        json.dumps(events),
        encoding="utf-8",
    )
    return module.process_events(
        input_path,
        output_path,
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 2, tzinfo=UTC),
    )


def check_missing_events(module, tmp_path):
    try:
        process(
            module,
            tmp_path / "missing.json",
            tmp_path / "missing-output.json",
            {"not_events": []},
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
    summary = process(
        module,
        tmp_path / "empty.json",
        tmp_path / "empty-output.json",
        {"events": []},
    )
    if summary["total_events"] != 0:
        raise AssertionError(
            f"unexpected total: {summary!r}"
        )
    if summary["avg_events"] != 0:
        raise AssertionError(
            f"unexpected average: {summary!r}"
        )


def check_happy_path(module, tmp_path):
    output_path = tmp_path / "valid-output.json"
    summary = process(
        module,
        tmp_path / "valid.json",
        output_path,
        {
            "events": [{
                "timestamp": "2024-01-01T12:00:00Z",
                "user_id": "user-1",
                "type": "view",
            }],
        },
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
        "skipped_events": 0,
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

    module = load_module(Path(sys.argv[1]).resolve())
    checks = [
        (
            "test_missing_events_key_raises_exact_error",
            check_missing_events,
        ),
        (
            "test_explicit_empty_events_has_zero_average",
            check_explicit_empty_events,
        ),
        (
            "test_existing_happy_path_still_works",
            check_happy_path,
        ),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        try:
            for name, check in checks:
                check(module, tmp_path)
                print(f"PASS: {name}")
        except (AssertionError, KeyError) as exc:
            print(f"FAIL: {exc}")
            return 1
    print(f"{len(checks)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
