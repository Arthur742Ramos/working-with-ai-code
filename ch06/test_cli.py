"""Check the maintained command-line runner."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

import validate_config

RUNNER = Path(__file__).with_name("validate_config.py")


def _inputs(tmp_path):
    schema = tmp_path / "schema.json"
    config = tmp_path / "config.json"
    schema.write_text(
        json.dumps({
            "port": {"type": "int", "required": True},
        }),
        encoding="utf-8",
    )
    config.write_text('{"port": 8080}', encoding="utf-8")
    return schema, config


def _run(schema, config):
    return subprocess.run(
        [sys.executable, str(RUNNER),
         "--schema", str(schema), "--config", str(config)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_valid_config(tmp_path):
    result = _run(*_inputs(tmp_path))
    assert result.returncode == 0
    assert result.stdout == "ok\n"
    assert result.stderr == ""


def test_wrong_type_config(tmp_path):
    schema, config = _inputs(tmp_path)
    config.write_text('{"port": true}', encoding="utf-8")
    result = _run(schema, config)
    assert result.returncode == 1
    assert result.stdout == "port: expected int\n"
    assert result.stderr == ""


@pytest.mark.parametrize("target", ["schema", "config"])
@pytest.mark.parametrize("failure", [
    "missing", "malformed_json",
    "invalid_utf8", "directory",
])
def test_loading_error(tmp_path, target, failure):
    schema, config = _inputs(tmp_path)
    path = schema if target == "schema" else config
    if failure == "missing":
        path.unlink()
    elif failure == "malformed_json":
        path.write_text("{", encoding="utf-8")
    elif failure == "invalid_utf8":
        path.write_bytes(b"\xff")
    else:
        path.unlink()
        path.mkdir()

    result = _run(schema, config)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.startswith(f"cannot load {path}: ")
    assert "Traceback" not in result.stderr


def test_permission_error(monkeypatch, capsys):
    def deny_open(*args, **kwargs):
        raise PermissionError("permission denied")

    monkeypatch.setattr("builtins.open", deny_open)
    status = validate_config.main([
        "--schema", "schema.json",
        "--config", "config.json",
    ])
    output = capsys.readouterr()
    assert status == 2
    assert output.out == ""
    assert output.err == (
        "cannot load schema.json: permission denied\n"
    )


def test_missing_argument():
    result = subprocess.run(
        [sys.executable, str(RUNNER)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert "required" in result.stderr
    assert "Traceback" not in result.stderr
