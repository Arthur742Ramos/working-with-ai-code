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
    with pytest.raises(ValueError):
        process_events(
            str(inp), str(out), JAN15, JAN16
        )


def test_offset_timestamp_in_range(tmp_path):
    # 10:30+05:00 == 05:30Z; window 05-06Z
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
