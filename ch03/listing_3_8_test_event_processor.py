import json
import pytest
from datetime import datetime, timezone
from pathlib import Path
from event_processor import process_events

START = datetime(
    2024, 1, 1, tzinfo=timezone.utc
)
END = datetime(
    2024, 12, 31, tzinfo=timezone.utc
)


def write_json(path: Path, data: dict):
    """Helper to write test fixtures."""
    path.write_text(json.dumps(data))


def test_empty_results_no_crash(
    tmp_path,
):
    """Zero matching events must not
    raise division by zero."""
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(inp, {"events": []})

    result = process_events(              #A
        str(inp), str(out), START, END
    )
    assert result["total_events"] == 0
    assert result["avg_events_per_user"] == 0


def test_bad_timestamp_skipped(
    tmp_path,
):
    """Unparseable timestamps skip, not
    crash."""
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(inp, {"events": [
        {
            "timestamp": "not-a-date",    #B
            "user_id": "u1",
            "type": "click"
        }
    ]})

    result = process_events(
        str(inp), str(out), START, END
    )
    assert result["skipped_events"] == 1
    assert result["total_events"] == 0


def test_duplicate_types_collapsed(
    tmp_path,
):
    """Repeated event types stored once."""
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(inp, {"events": [
        {
            "timestamp": "2024-06-01",
            "user_id": "u1",
            "type": "click"
        },
        {
            "timestamp": "2024-06-02",
            "user_id": "u1",
            "type": "click"               #C
        },
    ]})

    result = process_events(
        str(inp), str(out), START, END
    )
    user = result["per_user"]["u1"]
    assert user["count"] == 2
    assert user["types"] == ["click"]


def test_missing_events_key_raises(
    tmp_path,
):
    """Missing 'events' key raises
    ValueError."""
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(inp, {"data": []})         #D

    with pytest.raises(ValueError):
        process_events(
            str(inp), str(out), START, END
        )


def test_file_cleanup_on_error(
    tmp_path,
):
    """Input file closes even on parse
    error."""
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    inp.write_text("{bad json")           #E

    with pytest.raises(json.JSONDecodeError):
        process_events(
            str(inp), str(out), START, END
        )
    # If file handle leaked, this would
    # fail on Windows
    inp.unlink()
