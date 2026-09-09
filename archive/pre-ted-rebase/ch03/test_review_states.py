"""Regression checks for the intermediate review listing."""

import importlib.util
import json
from datetime import datetime
from pathlib import Path

import pytest


def load_intermediate():
    path = Path(__file__).with_name(
        "listing_3_6_event_processor_after_blockers.py"
    )
    spec = importlib.util.spec_from_file_location("intermediate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.process_events


@pytest.mark.parametrize("payload", [{}, {"other": []}])
def test_accepted_missing_events_guard_survives(tmp_path, payload):
    source = tmp_path / "input.json"
    source.write_text(json.dumps(payload))
    with pytest.raises(ValueError) as caught:
        load_intermediate()(
            source, tmp_path / "output.json",
            datetime(2024, 1, 15), datetime(2024, 1, 16),
        )
    assert str(caught.value) == (
        "input must be an object with an 'events' key"
    )


@pytest.mark.parametrize("count", [0, 1, 2])
def test_empty_and_nonempty_batches_survive(tmp_path, count):
    event = {"timestamp": "2024-01-15 12:00:00",
             "user_id": "u1", "type": "click"}
    source = tmp_path / "input.json"
    source.write_text(json.dumps({"events": [event] * count}))
    output = tmp_path / "output.json"
    result = load_intermediate()(
        source, output, datetime(2024, 1, 15), datetime(2024, 1, 16),
    )
    assert result["total_events"] == count
    assert result["avg_events"] == count
    assert json.loads(output.read_text()) == result
