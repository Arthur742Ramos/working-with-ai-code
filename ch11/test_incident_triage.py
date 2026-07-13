from dataclasses import replace
from pathlib import Path

import pytest

from incident_triage import (
    Event,
    format_event,
    load_events,
    select_timeline,
)


LOG = Path(__file__).parent / "incident.jsonl"


def test_timeline_keeps_only_one_deployment() -> None:
    events = load_events(LOG)

    timeline = select_timeline(events, "deploy-104")

    assert len(timeline) == 5
    assert {event.deployment_id for event in timeline} == {
        "deploy-104",
    }
    timestamps = [event.timestamp for event in timeline]
    assert timestamps == sorted(timestamps)


def test_timeline_preserves_trace_evidence() -> None:
    events = load_events(LOG)
    timeline = select_timeline(events, "deploy-104")
    error = next(
        event
        for event in timeline
        if event.severity == "ERROR"
    )

    rendered = format_event(error)

    assert "error_rate_above_limit" in rendered
    assert "[incident.jsonl:4]" in rendered
    assert "error_rate=0.071" in rendered
    trace = "trace=4bf92f3577b34da6a3ce929d0e0e4736"
    assert trace in rendered
    for invalid in (
        False,
        float("nan"),
        float("inf"),
        -0.001,
        1.1,
    ):
        with pytest.raises(
            ValueError,
            match="error_rate must be finite",
        ):
            replace(error, error_rate=invalid)


def test_unknown_deployment_has_no_timeline() -> None:
    events = load_events(LOG)

    assert select_timeline(events, "deploy-999") == []


def test_timeline_orders_mixed_utc_offsets() -> None:
    shared = {
        "deployment_id": "deploy-104",
        "service": "sample-api",
        "revision": "sample-api:1.8.0",
        "severity": "INFO",
        "event": "observed",
    }
    later = Event(
        timestamp="2030-04-18T15:00:00+02:00",
        source="incident.jsonl:2",
        **shared,
    )
    earlier = Event(
        timestamp="2030-04-18T12:30:00Z",
        source="incident.jsonl:1",
        **shared,
    )

    timeline = select_timeline(
        [later, earlier],
        "deploy-104",
    )

    assert timeline == [earlier, later]
