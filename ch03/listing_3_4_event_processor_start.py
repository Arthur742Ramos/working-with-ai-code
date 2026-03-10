"""Listing 3.4: The starting code: event processor with hidden issues.

From "Working with AI as a Real Teammate" (Manning)
Chapter 3
"""

import json
from datetime import datetime


def process_events(
    input_path,
    output_path,
    start_date,
    end_date,
):
    """Process user events from JSON."""
    f = open(input_path)
    data = json.load(f)

    results = []
    for event in data["events"]:
        event_date = datetime.strptime(
            event["timestamp"],
            "%Y-%m-%d %H:%M:%S",
        )
        if event_date >= start_date and event_date <= end_date:
            results.append(event)

    users = {}
    for event in results:
        user = event["user_id"]
        if user not in users:
            users[user] = {
                "count": 0,
                "types": [],
            }
        users[user]["count"] += 1
        users[user]["types"].append(event["type"])

    summary = {
        "total_events": len(results),
        "unique_users": len(users),
        "per_user": users,
        "avg_events": (
            len(results) / len(users)
        ),
    }

    out = open(output_path, "w")
    json.dump(summary, out)
    out.close()
    return summary
