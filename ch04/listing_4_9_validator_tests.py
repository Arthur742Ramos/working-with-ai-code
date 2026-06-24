"""Listing 4.9: Behavior-focused tests the agent generated for the validator

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""

from validation import validate_email


def test_valid_email():
    assert validate_email(
        "user@example.com"
    )


def test_missing_at():
    assert not validate_email(
        "userexample.com"
    )


def test_plus_addressing():
    assert validate_email(
        "user+tag@example.com"
    )


def test_non_ascii_domain_is_allowed():
    assert validate_email(
        "user@münchen.de"
    )
