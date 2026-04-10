"""Listing 4.11: AI-generated validation: username check and combined
registration validator

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""
import re

from listing_4_10_validation_module import (
    ValidationResult,
    validate_email,
    validate_password,
)


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


def validate_registration(
    email: str,
    password: str,
    username: str
) -> ValidationResult:
    """Validate full registration input."""
    errors = []
    if not validate_email(email):
        errors.append("Invalid email format")
    errors.extend(
        validate_password(password)
    )
    errors.extend(
        validate_username(username)
    )
    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors
    )
