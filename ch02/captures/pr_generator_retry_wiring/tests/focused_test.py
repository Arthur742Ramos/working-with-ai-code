"""Check that the CLI uses conversational retry."""
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

TEST_NAME = "test_cli_retries_after_malformed_json"
MALFORMED = "not-json"
VALID = json.dumps({
    "title": "Wire CLI retry",
    "summary": ["Use existing retry path", "Keep output stable"],
    "tests": ["Malformed output retries", "Valid output succeeds"],
    "risks": ["Extra model call", "Retry budget remains bounded"],
})


class ValidationError(Exception):
    """Stand in for the dependency's validation error."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def validate(instance, schema):
    """Validate only the schema rules this fixture needs."""
    required = schema["required"]
    if not isinstance(instance, dict):
        raise ValidationError("response must be an object")
    for key in required:
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


def main():
    if len(sys.argv) != 2:
        print("usage: focused_test.py PR_GENERATOR_PATH")
        return 2

    source_path = Path(sys.argv[1]).resolve()
    schema = runpy.run_path(
        str(source_path.with_name("schema.py"))
    )["SCHEMA"]
    responses = iter((MALFORMED, VALID))
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

    try:
        subprocess.run = lambda *args, **kwargs: (
            types.SimpleNamespace(stdout="diff --git a/app.py b/app.py")
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

            if exit_code != 0:
                print(f"FAIL: {TEST_NAME}")
                print(
                    "expected: CLI recovers after malformed "
                    "JSON on the second chat call"
                )
                print(
                    f"observed: SystemExit: {exit_code} "
                    f"after {len(calls)} chat call"
                )
                detail = stderr.getvalue().strip()
                if detail:
                    print(f"stderr: {detail}")
                return 1

            if len(calls) != 2:
                print(f"FAIL: {TEST_NAME}")
                print("expected: 2 chat calls")
                print(f"observed: {len(calls)} chat calls")
                return 1

            retry_messages = calls[1]["messages"]
            if len(retry_messages) != 3:
                print(f"FAIL: {TEST_NAME}")
                print("expected: retry conversation has 3 messages")
                print(
                    "observed: retry conversation has "
                    f"{len(retry_messages)} messages"
                )
                return 1
            if retry_messages[1] != {
                "role": "assistant",
                "content": MALFORMED,
            }:
                print(f"FAIL: {TEST_NAME}")
                print("observed: malformed reply was not preserved")
                return 1
            if "invalid" not in retry_messages[2]["content"]:
                print(f"FAIL: {TEST_NAME}")
                print("observed: correction omitted validation detail")
                return 1

            saved = json.loads(
                Path("pr_description.json").read_text(
                    encoding="utf-8"
                )
            )
            if saved != json.loads(VALID):
                print(f"FAIL: {TEST_NAME}")
                print("observed: CLI saved unexpected structured output")
                return 1
    finally:
        subprocess.run = original_run
        sys.argv = original_argv
        os.chdir(original_cwd)
        restore_modules(saved_modules)

    print(f"PASS: {TEST_NAME}")
    print("observed: CLI succeeded after 2 chat calls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
