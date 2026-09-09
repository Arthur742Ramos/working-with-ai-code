"""Listing 5.2: A timestamp parser that passes common examples

From "Working with AI as a Real Teammate" (Manning)
Chapter 5
"""

import re
from datetime import datetime


def parse_timestamp(value: str) -> datetime:
    pattern = (
        r"^\d{4}-\d{2}-\d{2}"
        r"T\d{2}:\d{2}:\d{2}"
        r"([+-]\d{2}:\d{2}|Z)$"
    )
    if not re.match(pattern, value):
        raise ValueError("invalid timestamp")
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)
