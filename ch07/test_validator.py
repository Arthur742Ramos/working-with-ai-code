"""Maintained tests for the JSON config validator.

The suite covers happy paths, required keys, wrong types, nesting,
empty schemas, strict integer handling, malformed rules, and float
support.
"""

from validator import validate


def test_happy_path():
    schema = {"name": {"type": "str", "required": True}}
    config = {"name": "alice"}
    assert validate(config, schema) == []


def test_missing_required_key():
    schema = {"name": {"type": "str", "required": True}}
    errors = validate({}, schema)
    assert len(errors) == 1
    assert errors[0].path == "name"
    assert "missing" in errors[0].message


def test_wrong_type_at_top_level():
    schema = {"port": {"type": "int", "required": True}}
    errors = validate({"port": "8080"}, schema)
    assert len(errors) == 1
    assert errors[0].path == "port"
    assert "int" in errors[0].message


def test_nested_missing_required_key():
    schema = {
        "db": {
            "type": "dict",
            "required": True,
            "fields": {
                "host": {"type": "str", "required": True},
            },
        },
    }
    errors = validate({"db": {}}, schema)
    assert len(errors) == 1
    assert errors[0].path == "db.host"


def test_empty_schema_accepts_anything():
    assert validate({"anything": 1}, {}) == []


def test_bool_is_not_accepted_as_int():
    schema = {"port": {"type": "int", "required": True}}
    errors = validate({"port": True}, schema)
    assert len(errors) == 1
    assert errors[0].path == "port"
    assert "int" in errors[0].message


def test_malformed_schema_rule_reports_error():
    errors = validate({"name": "alice"}, {"name": "str"})
    assert len(errors) == 1
    assert errors[0].path == "name"
    assert "malformed schema" in errors[0].message


def test_float_type_is_supported():
    # New contract: floats are a supported type. A valid float must
    # pass, and a non-float must be rejected with an "expected float"
    # error, not a "malformed schema rule".
    schema = {"ratio": {"type": "float", "required": True}}
    assert validate({"ratio": 0.5}, schema) == []
    errors = validate({"ratio": "half"}, schema)
    assert len(errors) == 1
    assert errors[0].path == "ratio"
    assert "float" in errors[0].message


def test_float_subclass_is_rejected_by_policy():
    class DerivedFloat(float):
        pass

    schema = {"ratio": {"type": "float", "required": True}}
    errors = validate({"ratio": DerivedFloat(0.5)}, schema)
    assert len(errors) == 1
    assert errors[0].path == "ratio"
    assert errors[0].message == "expected float"
