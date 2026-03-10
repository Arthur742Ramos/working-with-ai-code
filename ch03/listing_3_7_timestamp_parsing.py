"""Listing 3.7: Robust timestamp parsing with safe fallback.

From "Working with AI as a Real Teammate" (Manning)
Chapter 3
"""

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def parse_timestamp(
    raw: str,
) -> datetime | None:
    """Parse a timestamp, returning None on failure."""
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=timezone.utc
            )
        return dt
    except (ValueError, TypeError):
        logger.warning(
            "Skipping unparseable timestamp: %s",
            raw,
        )
        return None
