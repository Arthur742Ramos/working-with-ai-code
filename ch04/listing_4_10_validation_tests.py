"""Listing 4.10 Behavior-focused tests for the validation module."""
import pytest
from listing_4_9_validation_module import (
    validate_email,
    validate_password,
    validate_registration
)

class TestEmailValidation:
    def test_valid_email(self):
        assert validate_email(
            "user@example.com"
        )

    def test_missing_at(self):
        assert not validate_email(
            "userexample.com"
        )

    def test_plus_addressing(self):         # Plus addressing is valid per RFC but some regexes reject it
        assert validate_email(
            "user+tag@example.com"
        )

    def test_international_domain(self):    # International domains expose regex limitations
        assert validate_email(
            "user@münchen.de"
        )

class TestPasswordValidation:
    def test_short_password(self):
        errors = validate_password("Ab1")
        assert "8+ characters" in errors[0]

    def test_no_uppercase(self):
        errors = validate_password(
            "abcdefg1"
        )
        assert any(
            "uppercase" in e for e in errors
        )

    def test_strong_password(self):
        errors = validate_password(
            "Str0ngP@ss"
        )
        assert errors == []
