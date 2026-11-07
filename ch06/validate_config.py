import argparse
import json
import sys

from validator import validate


def _load(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        message = f"cannot load {path}: {exc}"
        raise ValueError(message) from exc


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate config against a schema.",
    )
    parser.add_argument("--schema", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args(argv)

    try:
        schema = _load(args.schema)
        config = _load(args.config)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    errors = validate(config, schema)

    if not errors:
        print("ok")
        return 0
    for err in errors:
        print(f"{err.path}: {err.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
