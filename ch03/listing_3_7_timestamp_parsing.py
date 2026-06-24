"""Listing 3.7: Robust timestamp parsing with an explicit UTC contract

From "Working with AI as a Real Teammate" (Manning)
Chapter 3
"""

import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def _to_utc(dt):
    """Normalize to aware UTC; naive
    values are assumed UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_timestamp(value):
    """Parse an ISO 8601 timestamp to
    aware UTC. Raises on bad input."""
    if (isinstance(value, str)
            and value.endswith("Z")):
        value = value[:-1] + "+00:00"
    return _to_utc(
        datetime.fromisoformat(value)
    )
