import re
from datetime import datetime

def parse_iso_timestamp(s: str) -> datetime:
    """Parse ISO 8601 timestamp with tz."""
    pattern = (
        r"^\d{4}-\d{2}-\d{2}"       #A
        r"T\d{2}:\d{2}:\d{2}"       #A
        r"([+-]\d{2}:\d{2}|Z)$"     #A
    )
    match = re.match(pattern, s)
    if not match:
        raise ValueError(
            f"Invalid timestamp: {s}"
        )
    
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    
    return datetime.fromisoformat(s)
