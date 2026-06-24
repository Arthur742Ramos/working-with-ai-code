"""Listing 4.8: AI-generated validation module to be verified

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""

import re


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@"
    pattern += r"[a-zA-Z0-9.-]+\."
    pattern += r"[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(
    password: str
) -> list[str]:
    """Check password strength."""
    errors = []
    if len(password) < 8:
        errors.append(
            "Password must be 8+ characters"
        )
    if not re.search(r"[A-Z]", password):
        errors.append("Need one uppercase")
    if not re.search(r"[0-9]", password):
        errors.append("Need one digit")
    return errors


def validate_username(
    username: str
) -> list[str]:
    """Validate username format."""
    errors = []
    if len(username) < 3:
        errors.append("Username too short")
    if len(username) > 30:
        errors.append("Username too long")
    if not re.match(
        r"^[a-zA-Z0-9_]+$", username
    ):
        errors.append(
            "Only letters, numbers, _"
        )
    return errors
