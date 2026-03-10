"""Listing 3.10: Test cases, part 1.

From "Working with AI as a Real Teammate" (Manning)
Chapter 3
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from event_processor import process_events

START = datetime(
    2024, 1, 1, tzinfo=timezone.utc
)
END = datetime(
    2024, 12, 31, tzinfo=timezone.utc
)


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data))


def test_empty_results_no_crash(
    tmp_path,
):
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(inp, {"events": []})

    result = process_events(
        str(inp), str(out), START, END
    )
    assert result["total_events"] == 0
    assert result["avg_events_per_user"] == 0


def test_bad_timestamp_is_skipped(
    tmp_path,
):
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(
        inp,
        {"events": [
            {
                "timestamp": "not-a-date",
                "user_id": "u1",
                "type": "click",
            }
        ]},
    )

    result = process_events(
        str(inp), str(out), START, END
    )
    assert result["skipped_events"] == 1
