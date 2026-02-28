"""Listing 4.1 AI-generated timestamp parser — looks correct, misses edge cases."""
import re
from datetime import datetime, timezone

def parse_iso_timestamp(s: str) -> datetime:
    """Parse ISO 8601 timestamp with tz."""
    pattern = (
        r"^\d{4}-\d{2}-\d{2}"       # Regex matches common ISO 8601 format
        r"T\d{2}:\d{2}:\d{2}"       # Regex matches common ISO 8601 format
        r"([+-]\d{2}:\d{2}|Z)$"     # Regex matches common ISO 8601 format
    )
    match = re.match(pattern, s)
    if not match:
        raise ValueError(
            f"Invalid timestamp: {s}"
        )
    
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    
    return datetime.fromisoformat(s)
