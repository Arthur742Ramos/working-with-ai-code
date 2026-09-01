    users = {}
    skipped_events = 0
    for event in results:
        if (not isinstance(event, dict)
                or "user_id" not in event
                or "type" not in event):         # B
            skipped_events += 1
            continue
        user = event["user_id"]
        if user not in users:
            users[user] = {
                "count": 0,
                "types": set(),
            }
        users[user]["count"] += 1
        users[user]["types"].add(event["type"])

    for stats in users.values():
        stats["types"] = sorted(stats["types"])

    counted = len(results) - skipped_events
    summary = {
        "total_events": counted,              # C
        "unique_users": len(users),
        "per_user": users,
        "skipped_events": skipped_events,
        "avg_events": (
            counted / len(users) if users else 0
        ),
    }
    logger.info(
        "Summary: %d counted, %d skipped, %d users",
        counted, skipped_events, len(users),
    )
    with open(output_path, "w") as out:
        json.dump(summary, out)
    return summary
