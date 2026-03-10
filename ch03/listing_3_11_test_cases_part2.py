"""Listing 3.11: Test cases, part 2.

From "Working with AI as a Real Teammate" (Manning)
Chapter 3
"""

import pytest


def test_duplicate_types_collapse_to_one(
    tmp_path,
):
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(
        inp,
        {"events": [
            {
                "timestamp": "2024-06-01",
                "user_id": "u1",
                "type": "click",
            },
            {
                "timestamp": "2024-06-02",
                "user_id": "u1",
                "type": "click",
            },
        ]},
    )

    result = process_events(
        str(inp), str(out), START, END
    )
    assert result["per_user"]["u1"]["types"] == ["click"]


def test_missing_events_key_raises(
    tmp_path,
):
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(inp, {"data": []})

    with pytest.raises(ValueError):
        process_events(
            str(inp), str(out), START, END
        )


def test_timezone_offset_is_parsed(
    tmp_path,
):
    inp = tmp_path / "in.json"
    out = tmp_path / "out.json"
    write_json(
        inp,
        {"events": [
            {
                "timestamp":
                    "2024-06-01T12:00:00+02:00",
                "user_id": "u1",
                "type": "click",
            }
        ]},
    )

    result = process_events(
        str(inp), str(out), START, END
    )
    assert result["total_events"] == 1
