"""Behavior checks for the alert feature through an injected seam."""

import importlib
import importlib.util
from unittest.mock import patch

import pytest

import http_client
import alerts
from alerts import ALERTS_URL
from http_client import Response


@pytest.fixture(autouse=True)
def configured_client(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "unit-test-token")
    http_client.reset_transport()
    yield
    http_client.reset_transport()


def recording_transport(response_status=200):
    calls = []

    def fake(method, url, headers, body):
        calls.append((method, url, headers, body))
        return Response(response_status, {"ok": response_status < 400})

    return calls, fake


def observe_shared_call(module=None):
    calls = []

    def fake_call(method, url, *, json):
        calls.append((method, url, json))
        return Response(200, {"ok": True})

    with patch.object(http_client, "call", fake_call):
        if module is None:
            module = importlib.reload(alerts)
        accepted = module.send_alert("disk 90% full")
    return accepted, calls


def assert_exact_shared_call(accepted, calls):
    assert accepted is True
    assert calls == [
        (
            "POST",
            ALERTS_URL,
            {"text": "disk 90% full"},
        )
    ], (
        "send_alert must route method, URL, and JSON "
        "through http_client.call"
    )


def test_send_alert_routes_through_house_client():
    try:
        accepted, calls = observe_shared_call()
        assert_exact_shared_call(accepted, calls)
    finally:
        importlib.reload(alerts)


def test_module_qualified_shared_client_shape_is_accepted(tmp_path):
    source = tmp_path / "module_qualified_alerts.py"
    source.write_text(
        '"""Equivalent module-qualified shared-client use."""\n\n'
        "import http_client\n\n"
        f'ALERTS_URL = "{ALERTS_URL}"\n\n\n'
        "def send_alert(message: str) -> bool:\n"
        "    response = http_client.call(\n"
        '        "POST", ALERTS_URL, json={"text": message}\n'
        "    )\n"
        "    return response.status < 400\n",
        encoding="utf-8",
    )
    spec = importlib.util.spec_from_file_location(
        "module_qualified_alerts", source,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    accepted, calls = observe_shared_call(module)
    assert_exact_shared_call(accepted, calls)


def test_house_client_adds_auth_for_feature():
    calls, fake = recording_transport()
    http_client.set_transport(fake)

    alerts.send_alert("nightly export failed")

    assert calls[0][2]["Authorization"] == "******"


def test_alert_reports_failure_status():
    _, fake = recording_transport(response_status=500)
    http_client.set_transport(fake)

    assert alerts.send_alert("anything") is False
