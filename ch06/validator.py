from dataclasses import dataclass

CHECKS = {
    "str": lambda value: isinstance(value, str),
    "int": lambda value: type(value) is int,
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
        present = isinstance(cfg, dict) and key in cfg  #A
        rule = rule if isinstance(rule, dict) else {}
        kind = rule.get("type")
        if kind not in CHECKS:  #B
            errors.append(E(path, "malformed schema rule"))
        elif not present and rule.get("required"):
            errors.append(E(path, "missing required key"))
        elif present and not CHECKS[kind](cfg[key]):
            errors.append(E(path, f"expected {kind}"))
        elif present and kind == "dict":
            _walk(
                cfg[key],
                rule.get("fields", {}),
                path + ".",
                errors,
            )  #C
    return errors
