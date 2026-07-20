"""Focused test for the strict integer boundary."""

import importlib.util
import sys
from pathlib import Path

TEST_NAME = "test_bool_is_not_accepted_as_int"


def load_validator(module_path):
    spec = importlib.util.spec_from_file_location(
        "captured_validator",
        module_path,
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main():
    if len(sys.argv) != 2:
        print(
            "usage: test_bool_is_not_accepted_as_int.py "
            "VALIDATOR_PATH"
        )
        return 2

    validator = load_validator(Path(sys.argv[1]))
    schema = {
        "port": {
            "type": "int",
            "required": True,
        },
    }
    errors = validator.validate({"port": True}, schema)

    if (
        len(errors) == 1
        and errors[0].path == "port"
        and "int" in errors[0].message
    ):
        print(f"PASS: {TEST_NAME}")
        print("observed: port: expected int")
        return 0

    if not errors:
        observed = "no validation errors; True was accepted"
    else:
        observed = repr(errors)

    print(f"FAIL: {TEST_NAME}")
    print("expected: port: expected int")
    print(f"observed: {observed}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
