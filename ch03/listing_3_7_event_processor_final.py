import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def parse_timestamp(
    raw: str,
) -> datetime | None:
    """Parse ISO 8601 timestamp.
    Returns None on failure."""
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=timezone.utc
            )
        return dt
    except (ValueError, TypeError):
        logger.warning(
            "Skipping unparseable "
            "timestamp: %s", raw
        )
        return None


def process_events(
    input_path: str,
    output_path: str,
    start_date: datetime,
    end_date: datetime,
) -> dict:
    """Process user events from JSON.

    Reads events, filters by date range,
    computes per-user statistics, and
    writes a JSON summary.

    Raises:
        ValueError: if input data is
            malformed
    """
    with open(input_path) as f:
        data = json.load(f)

    if "events" not in data:              #A
        raise ValueError(
            "Missing 'events' key in "
            "input data"
        )
    if not isinstance(data["events"], list):
        raise ValueError(
            "'events' must be a list"
        )

    results = []
    skipped = 0
    for event in data["events"]:
        ts = parse_timestamp(
            event.get("timestamp", "")
        )
        if ts is None:
            skipped += 1
            continue
        if start_date <= ts <= end_date:
            results.append(event)

    users: dict[str, dict] = {}
    for event in results:
        uid = event["user_id"]
        if uid not in users:
            users[uid] = {
                "count": 0,
                "types": set(),           #B
            }
        users[uid]["count"] += 1
        users[uid]["types"].add(
            event["type"]
        )

    # Converting sets to sorted lists
    for info in users.values():           #C
        info["types"] = sorted(
            info["types"]
        )

    avg = (
        len(results) / len(users)
        if users
        else 0
    )

    summary = {
        "total_events": len(results),
        "unique_users": len(users),
        "skipped_events": skipped,
        "per_user": users,
        "avg_events_per_user": round(
            avg, 2
        ),
    }

    with open(output_path, "w") as out:
        json.dump(summary, out, indent=2)

    logger.info(                          #D
        "Processed %d events for %d users"
        " (%d skipped)",
        len(results),
        len(users),
        skipped,
    )

    return summary
