"""Listing 2.3: JSON schema for PR description validation."""

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2
        },
        "tests": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2
        },
        "risks": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2
        }
    },
    "required": ["title", "summary", "tests", "risks"],
    "additionalProperties": False
}
