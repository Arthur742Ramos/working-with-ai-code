"""Listing 2.3 JSON schema for PR description validation.

The contract made the output consistent for humans; a CI/CD pipeline
needs machine-parseable structure. This schema is the Checks phase made
concrete: every response must satisfy it before your code is allowed to
trust the result.

The schema guarantees structure, not substance. A perfectly valid JSON
response can still contain lies, which is why schema validation is a
necessary check but not a sufficient one.
"""

SCHEMA = {                                          #A
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
    "required": ["title", "summary", "tests",       #B
                 "risks"],
    "additionalProperties": False                   #C
}
