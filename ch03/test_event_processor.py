import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from event_processor import process_events

PACKAGE_ROOT = Path(__file__).resolve().parent
EXPECTED_ERROR = (
    "input must be an object with an 'events' key"
)

UTC = timezone.utc
JAN15 = datetime(2024, 1, 15, tzinfo=UTC)
JAN16 = datetime(2024, 1, 16, tzinfo=UTC)


def _run(tmp_path, events,
         start=JAN15, end=JAN16):
    inp = tmp_path / "in.json"
    inp.write_text(
        json.dumps({"events": events}),
        encoding="utf-8",
    )
    out = tmp_path / "out.json"
    return process_events(
        str(inp), str(out), start, end
    )


def test_empty_input_zero_average(tmp_path):
    summary = _run(tmp_path, [])
    assert summary["total_events"] == 0
    assert summary["avg_events"] == 0


def test_bad_timestamp_is_skipped(tmp_path):
    events = [
        {"user_id": "u1", "type": "click",
         "timestamp": "2024-01-15T10:00:00Z"},
        {"user_id": "u2", "type": "view",
         "timestamp": "not-a-date"},
    ]
    summary = _run(tmp_path, events)
    assert summary["total_events"] == 1
    assert "u2" not in summary["per_user"]


def test_duplicate_types_collapse(tmp_path):
    events = [
        {"user_id": "u1", "type": "click",
         "timestamp": "2024-01-15T10:00:00Z"},
        {"user_id": "u1", "type": "click",
         "timestamp": "2024-01-15T11:00:00Z"},
        {"user_id": "u1", "type": "view",
         "timestamp": "2024-01-15T12:00:00Z"},
    ]
    summary = _run(tmp_path, events)
    u1 = summary["per_user"]["u1"]
    assert u1["count"] == 3
    assert u1["types"] == ["click", "view"]


def test_missing_events_key_raises(tmp_path):
    inp = tmp_path / "in.json"
    inp.write_text(
        json.dumps({"not_events": []}),
        encoding="utf-8",
    )
    out = tmp_path / "out.json"
    with pytest.raises(ValueError) as caught:
        process_events(
            str(inp), str(out), JAN15, JAN16
        )
    assert str(caught.value) == EXPECTED_ERROR


def test_offset_timestamp_in_range(tmp_path):
    events = [
        {"user_id": "u1", "type": "click",
         "timestamp":
             "2024-01-15T10:30:00+05:00"},
    ]
    summary = _run(
        tmp_path, events,
        start=datetime(2024, 1, 15, 5,
                       tzinfo=UTC),
        end=datetime(2024, 1, 15, 6,
                     tzinfo=UTC),
    )
    assert summary["total_events"] == 1


def test_valid_event_outside_window(tmp_path):
    events = [
        {"user_id": "u1", "type": "click",
         "timestamp": "2024-02-01T10:00:00Z"},
    ]
    summary = _run(tmp_path, events)
    assert summary["total_events"] == 0
    assert summary["avg_events"] == 0


@pytest.mark.parametrize(
    "script_name",
    ["focused_test.py", "full_capture_check.py"],
)
def test_reader_command_is_executable(script_name):
    completed = subprocess.run(
        [
            sys.executable,
            script_name,
            "event_processor.py",
        ],
        cwd=PACKAGE_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout
    assert "failed" not in completed.stdout.lower()
