"""Process user events from JSON.

Example policy: naive timestamps are interpreted as UTC.
This is a human-defined contract, not an emitter audit.
"""
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def _to_utc(dt):
    """Normalize to aware UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_timestamp(value):
    """Parse an ISO 8601 timestamp to aware UTC."""
    if (isinstance(value, str)
            and value.endswith("Z")):
        value = value[:-1] + "+00:00"
    return _to_utc(
        datetime.fromisoformat(value)
    )


def process_events(input_path, output_path,
                   start_date, end_date):
    """Process events under the timezone contract."""
    with open(input_path) as f:
        data = json.load(f)

    if not isinstance(data, dict) or \
            "events" not in data:
        raise ValueError(
            "input must be an object with "
            "an 'events' key"
        )
    if not isinstance(data["events"], list):
        raise ValueError(
            "'events' must be a list"
        )

    start_date = _to_utc(start_date)
    end_date = _to_utc(end_date)

    results = []
    for event in data["events"]:
        ts = (event.get("timestamp")
              if isinstance(event, dict)
              else event)
        try:
            event_date = _parse_timestamp(ts)
        except (ValueError, TypeError) as exc:
            logger.warning(
                "Skipping unparseable "
                "timestamp %r: %s", ts, exc
            )
            continue
        if start_date <= event_date <= end_date:
            results.append(event)

    users = {}
    skipped_events = 0
    for event in results:
        if (not isinstance(event, dict)
                or "user_id" not in event
                or "type" not in event):
            skipped_events += 1
            continue
        user = event["user_id"]
        if user not in users:
            users[user] = {
                "count": 0,
                "types": set(),
            }
        users[user]["count"] += 1
        users[user]["types"].add(
            event["type"]
        )

    for stats in users.values():
        stats["types"] = sorted(
            stats["types"]
        )

    counted = len(results) - skipped_events
    summary = {
        "total_events": counted,
        "unique_users": len(users),
        "per_user": users,
        "skipped_events": skipped_events,
        "avg_events": (
            counted / len(users)
            if users else 0
        ),
    }

    logger.info(
        "Summary: %d counted, %d skipped, "
        "%d users",
        counted, skipped_events, len(users),
    )
    with open(output_path, "w") as out:
        json.dump(summary, out)
    return summary
