"""Build a cited timeline from structured events."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Event:
    """One observed operational event."""

    timestamp: str
    deployment_id: str
    service: str
    revision: str
    severity: str
    event: str
    source: str
    trace_id: str | None = None
    error_rate: float | None = None

    def __post_init__(self) -> None:
        rate = self.error_rate
        if rate is None:
            return
        if (
            isinstance(rate, bool)
            or not isinstance(rate, (int, float))
            or not math.isfinite(rate)
            or not 0 <= rate <= 1
        ):
            raise ValueError(
                "error_rate must be finite, 0 to 1"
            )


def load_events(path: Path) -> list[Event]:
    """Load JSON lines without guessing fields."""
    events: list[Event] = []
    content = path.read_text(encoding="utf-8")
    for number, line in enumerate(
        content.splitlines(),
        start=1,
    ):
        data = json.loads(line)
        events.append(
            Event(
                timestamp=data["timestamp"],
                deployment_id=data["deployment_id"],
                service=data["service"],
                revision=data["revision"],
                severity=data["severity"],
                event=data["event"],
                source=f"{path.name}:{number}",
                trace_id=data.get("trace_id"),
                error_rate=data.get("error_rate"),
            )
        )
    return events


def _event_time(event: Event) -> datetime:
    value = event.timestamp.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp needs a UTC offset")
    return parsed


def select_timeline(
    events: Iterable[Event],
    deployment_id: str,
) -> list[Event]:
    """Select one deployment and order observed facts."""
    selected = (
        event
        for event in events
        if event.deployment_id == deployment_id
    )
    return sorted(selected, key=_event_time)


def format_event(event: Event) -> str:
    """Keep source identifiers beside each fact."""
    trace = ""
    if event.trace_id:
        trace = f" trace={event.trace_id}"
    rate = ""
    if event.error_rate is not None:
        rate = f" error_rate={event.error_rate:.3f}"
    return (
        f"[{event.source}] "
        f"{event.timestamp} {event.severity} "
        f"{event.event} revision={event.revision}"
        f"{rate}{trace}"
    )


def main() -> int:
    """Print a bounded, source-linked timeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("deployment_id")
    args = parser.parse_args()
    events = load_events(args.log)
    timeline = select_timeline(
        events,
        args.deployment_id,
    )
    for event in timeline:
        print(format_event(event))
    return 0 if timeline else 1


if __name__ == "__main__":
    raise SystemExit(main())
