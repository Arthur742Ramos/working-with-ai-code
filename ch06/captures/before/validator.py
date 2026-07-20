"""JSON config validator (role-relay running example).

Built by four narrow roles: the architect fixed the contract (a
dotted-path ValidationError, a list return that never raises, a small
set of supported types), the coder implemented it, the tester broke it,
and the explainer wrote the CLI and README. `validate` walks the schema
and returns a list of errors, possibly empty.
"""

from dataclasses import dataclass

CHECKS = {
    "str": lambda value: isinstance(value, str),
    "int": lambda value: isinstance(value, int),
    "bool": lambda value: isinstance(value, bool),
    "dict": lambda value: isinstance(value, dict),
    "float": lambda value: type(value) is float,
}


@dataclass(frozen=True)
class ValidationError:
    path: str
    message: str


def validate(config, schema) -> list[ValidationError]:
    return _walk(config, schema, "", [])


def _walk(cfg, sch, prefix, errors):
    E = ValidationError
    for key, rule in sch.items():
        path = f"{prefix}{key}"
        present = isinstance(cfg, dict) and key in cfg
        rule = rule if isinstance(rule, dict) else {}
        kind = rule.get("type")
        if kind not in CHECKS:
            errors.append(E(path, "malformed schema rule"))
        elif not present and rule.get("required"):
            errors.append(E(path, "missing required key"))
        elif present and not CHECKS[kind](cfg[key]):
            errors.append(E(path, f"expected {kind}"))
        elif present and kind == "dict":
            _walk(cfg[key], rule.get("fields", {}),
                  path + ".", errors)
    return errors
