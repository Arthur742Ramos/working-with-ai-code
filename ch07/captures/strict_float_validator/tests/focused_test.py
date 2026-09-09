"""Focused strict-float behavior check."""
import importlib.util
import sys
from pathlib import Path


class DerivedFloat(float):
    """Float subclass that exact built-in policy rejects."""


CASES = (
    (
        "test_real_float_is_accepted",
        0.5,
        [],
    ),
    (
        "test_int_is_rejected_as_float",
        1,
        "expected float",
    ),
    (
        "test_bool_is_rejected_as_float",
        True,
        "expected float",
    ),
    (
        "test_string_is_rejected_as_float",
        "0.5",
        "expected float",
    ),
    (
        "test_float_subclass_is_rejected_as_float",
        DerivedFloat(0.5),
        "expected float",
    ),
)


def load_module(module_path):
    spec = importlib.util.spec_from_file_location(
        "captured_validator",
        module_path,
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render_errors(errors):
    return [
        (error.path, error.message)
        for error in errors
    ]


def main():
    if len(sys.argv) != 2:
        print("usage: focused_test.py VALIDATOR_PATH")
        return 2

    module = load_module(Path(sys.argv[1]))
    schema = {
        "ratio": {
            "type": "float",
            "required": True,
        },
    }
    failures = 0

    for name, value, expected in CASES:
        observed = render_errors(
            module.validate({"ratio": value}, schema)
        )
        wanted = (
            []
            if expected == []
            else [("ratio", expected)]
        )
        if observed == wanted:
            print(f"PASS: {name}")
            continue
        failures += 1
        print(f"FAIL: {name}")
        print(f"expected: {wanted!r}")
        print(f"observed: {observed!r}")

    print(f"{failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
