import json
from datetime import datetime, timezone

import pytest

from event_processor import process_events

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
