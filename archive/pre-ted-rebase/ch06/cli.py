import argparse
import json
import sys

from validator import validate


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate config against a schema.",
    )
    parser.add_argument("--schema", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args(argv)

    schema = _load(args.schema)
    config = _load(args.config)
    errors = validate(config, schema)

    if not errors:
        print("ok")
        return 0
    for err in errors:
        print(f"{err.path}: {err.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
