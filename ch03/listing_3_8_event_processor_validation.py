def process_events(input_path, output_path,
                   start_date, end_date):
    """Process events under the UTC contract."""
    with open(input_path) as f:
        data = json.load(f)

    if not isinstance(data, dict) or \
            "events" not in data:         # A
        raise ValueError(
            "input must be an object with "
            "an 'events' key"
        )
    if not isinstance(data["events"], list):
        raise ValueError("'events' must be a list")

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
