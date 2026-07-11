"""Behavior checks for the alert feature through an injected transport."""

import pytest

import http_client
from alerts import ALERTS_URL, send_alert
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


def test_send_alert_routes_through_house_client():
    calls, fake = recording_transport()
    http_client.set_transport(fake)

    assert send_alert("disk 90% full") is True
    assert calls == [
        (
            "POST",
            ALERTS_URL,
            {"Authorization": "Bearer unit-test-token"},
            {"text": "disk 90% full"},
        )
    ]


def test_house_client_adds_auth_for_feature():
    calls, fake = recording_transport()
    http_client.set_transport(fake)

    send_alert("nightly export failed")

    assert calls[0][2]["Authorization"] == "Bearer unit-test-token"


def test_alert_reports_failure_status():
    _, fake = recording_transport(response_status=500)
    http_client.set_transport(fake)

    assert send_alert("anything") is False
