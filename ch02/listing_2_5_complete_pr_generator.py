import subprocess
import json
from jsonschema import validate, ValidationError
from llm_client import chat

SCHEMA = {                                            #A
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
    "required": ["title", "summary", "tests", "risks"],
    "additionalProperties": False
}

SYSTEM_PROMPT = (                                     #B
    "You are a senior software engineer writing pull request descriptions.\n"
    "You ALWAYS respond with valid JSON matching the requested schema.\n"
    "No markdown, no explanation, just the JSON object."
)
