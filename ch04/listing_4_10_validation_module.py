"""Listing 4.10: AI-generated validation: data model, email, and password checks

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""
import re
from dataclasses import dataclass


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@"     # Email regex handles common cases but not all valid addresses
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
