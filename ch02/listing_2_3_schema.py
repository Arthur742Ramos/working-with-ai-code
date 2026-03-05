"""Listing 2.3: JSON schema for PR description validation

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "maxLength": 72
        },
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
    "required": ["title", "summary", "tests",
                 "risks"],
    "additionalProperties": False
}
