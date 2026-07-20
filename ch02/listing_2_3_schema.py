"""Listing 2.3: JSON Schema for a PR description

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 72
        },
        "summary": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            },
            "minItems": 2
        },
        "tests": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            },
            "minItems": 2
        },
        "risks": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            },
            "minItems": 2
        }
    },
    "required": ["title", "summary", "tests",
                 "risks"],
    "additionalProperties": False
}
