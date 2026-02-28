import json
from datetime import datetime

def process_events(input_path, output_path,
                   start_date, end_date):
    """Process user events from JSON."""
    f = open(input_path)                  #A
    data = json.load(f)

    results = []
    for event in data["events"]:
        event_date = datetime.strptime(   #B
            event["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )
        if event_date >= start_date and \
           event_date <= end_date:
            results.append(event)

    # Compute stats
    users = {}
    for event in results:
        user = event["user_id"]
        if user not in users:
            users[user] = {
                "count": 0,
                "types": []
            }
        users[user]["count"] += 1
        users[user]["types"].append(      #C
            event["type"]
        )

    summary = {
        "total_events": len(results),
        "unique_users": len(users),
        "per_user": users,
        "avg_events": (                   #D
            len(results) / len(users)
        )
    }

    out = open(output_path, "w")          #E
    json.dump(summary, out)
    out.close()
    return summary
