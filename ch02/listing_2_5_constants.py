"""Listing 2.5: PR generator constants: schema and system prompt.

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "maxLength": 72,
        },
        "summary": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
        },
        "tests": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
        },
        "risks": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
        },
    },
    "required": ["title", "summary", "tests", "risks"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are a senior software engineer writing pull "
    "request descriptions.\n"
    "You ALWAYS respond with valid JSON matching the "
    "requested schema.\n"
    "No markdown, no explanation, just the JSON object."
)
