import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def parse_timestamp(
    raw: str,
) -> datetime | None:
    """Parse a timestamp, returning None
    on failure."""
    try:
        dt = datetime.fromisoformat(raw)  #A
        if dt.tzinfo is None:
            dt = dt.replace(              #B
                tzinfo=timezone.utc
            )
        return dt
    except (ValueError, TypeError):
        logger.warning(                   #C
            "Skipping unparseable "
            "timestamp: %s", raw
        )
        return None
