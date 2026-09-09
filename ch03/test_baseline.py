import json
from datetime import datetime
from event_processor import process_events


def test_one_valid_event(tmp_path):
    inp, out = tmp_path / "in.json", tmp_path / "out.json"
    event = {"user_id": "u1", "type": "click",
             "timestamp": "2024-01-15 12:00:00"}
    inp.write_text(json.dumps({"events": [event]}))
    result = process_events(
        inp, out, datetime(2024, 1, 15),
        datetime(2024, 1, 16),
    )
    assert result["total_events"] == 1
    assert result["avg_events"] == 1
    assert json.loads(out.read_text()) == result
