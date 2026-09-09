"""Protect neighboring CLI retry behavior."""
import contextlib
import io
import json
import os
import runpy
import subprocess
import sys
import tempfile
import types
from pathlib import Path

VALID = json.dumps({
    "title": "Wire CLI retry",
    "summary": ["Use existing retry path", "Keep output stable"],
    "tests": ["Malformed output retries", "Valid output succeeds"],
    "risks": ["Extra model call", "Retry budget remains bounded"],
})
SCHEMA_INVALID = json.dumps({
    "title": "Missing risks",
    "summary": ["First item", "Second item"],
    "tests": ["First check", "Second check"],
})


class ValidationError(Exception):
    """Stand in for the dependency's validation error."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def validate(instance, schema):
    """Validate only the schema rules this fixture needs."""
    if not isinstance(instance, dict):
        raise ValidationError("response must be an object")
    for key in schema["required"]:
        if key not in instance:
            raise ValidationError(f"'{key}' is required")
    for key in ("summary", "tests", "risks"):
        if len(instance[key]) < 2:
            raise ValidationError(
                f"{key} must contain at least two items"
            )


def install_module(name, module, saved):
    saved[name] = sys.modules.get(name)
    sys.modules[name] = module


def restore_modules(saved):
    for name, module in saved.items():
        if module is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = module


def run_cli(source_path, response_values):
    schema = runpy.run_path(
        str(source_path.with_name("schema.py"))
    )["SCHEMA"]
    responses = iter(response_values)
    calls = []

    llm_module = types.ModuleType("llm_client")

    def chat(**kwargs):
        calls.append(kwargs)
        return next(responses)

    llm_module.chat = chat
    schema_module = types.ModuleType("schema")
    schema_module.SCHEMA = schema
    jsonschema_module = types.ModuleType("jsonschema")
    jsonschema_module.validate = validate
    jsonschema_module.ValidationError = ValidationError

    saved_modules = {}
    install_module("llm_client", llm_module, saved_modules)
    install_module("schema", schema_module, saved_modules)
    install_module(
        "jsonschema",
        jsonschema_module,
        saved_modules,
    )

    original_run = subprocess.run
    original_argv = sys.argv[:]
    original_cwd = Path.cwd()
    stdout = io.StringIO()
    stderr = io.StringIO()
    exit_code = 0
    saved_output = None

    try:
        subprocess.run = lambda *args, **kwargs: (
            types.SimpleNamespace(
                stdout="diff --git a/app.py b/app.py"
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            sys.argv = [str(source_path)]
            with contextlib.redirect_stdout(stdout):
                with contextlib.redirect_stderr(stderr):
                    try:
                        runpy.run_path(
                            str(source_path),
                            run_name="__main__",
                        )
                    except SystemExit as exc:
                        exit_code = int(exc.code or 0)
            output_path = Path("pr_description.json")
            if output_path.exists():
                saved_output = json.loads(
                    output_path.read_text(encoding="utf-8")
                )
    finally:
        subprocess.run = original_run
        sys.argv = original_argv
        os.chdir(original_cwd)
        restore_modules(saved_modules)

    return {
        "exit_code": exit_code,
        "calls": calls,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "saved_output": saved_output,
    }


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def test_valid_first_response(source_path):
    result = run_cli(source_path, [VALID])
    require(result["exit_code"] == 0, result["stderr"])
    require(len(result["calls"]) == 1, "expected 1 chat call")
    require(
        result["saved_output"] == json.loads(VALID),
        "unexpected saved output",
    )
    print("PASS: test_valid_first_response_stays_single_attempt")
    print("observed: CLI succeeded after 1 chat call")


def test_schema_failure_retries(source_path):
    result = run_cli(source_path, [SCHEMA_INVALID, VALID])
    require(result["exit_code"] == 0, result["stderr"])
    require(len(result["calls"]) == 2, "expected 2 chat calls")
    messages = result["calls"][1]["messages"]
    require(messages[1]["content"] == SCHEMA_INVALID,
            "schema-invalid reply was not preserved")
    require("'risks' is required" in messages[2]["content"],
            "schema detail was not included")
    print("PASS: test_schema_failure_retries_with_feedback")
    print("observed: CLI succeeded after 2 chat calls")


def test_retry_exhaustion(source_path):
    result = run_cli(
        source_path,
        ["not-json", "still-not-json", "bad-again"],
    )
    require(result["exit_code"] == 1, "expected exit status 1")
    require(len(result["calls"]) == 3, "expected 3 chat calls")
    require("Failed after 3 attempts" in result["stderr"],
            "bounded exhaustion detail missing")
    print("PASS: test_retry_exhaustion_stays_bounded")
    print("observed: CLI failed after 3 chat calls")


def main():
    if len(sys.argv) != 2:
        print("usage: broader_test.py PR_GENERATOR_PATH")
        return 2

    source_path = Path(sys.argv[1]).resolve()
    tests = (
        test_valid_first_response,
        test_schema_failure_retries,
        test_retry_exhaustion,
    )
    try:
        for test in tests:
            test(source_path)
    except AssertionError as exc:
        print(f"FAIL: {test.__name__}")
        print(f"observed: {exc}")
        return 1

    print("3 passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
