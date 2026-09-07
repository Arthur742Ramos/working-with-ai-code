"""Focused checks for auth, retries, and the fail-closed transport."""

import pytest

import http_client
from http_client import Response


@pytest.fixture(autouse=True)
def reset_client():
    http_client.reset_transport()
    yield
    http_client.reset_transport()


def test_call_requires_a_credential(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="API_TOKEN is required"):
        http_client.call("POST", "https://example.invalid")


def test_default_transport_makes_no_network_call(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "unit-test-token")

    with pytest.raises(RuntimeError, match="no HTTP transport configured"):
        http_client.call("POST", "https://example.invalid")


def test_call_retries_transient_responses(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "unit-test-token")
    statuses = iter([503, 429, 200])
    calls = []

    def fake(method, url, headers, body):
        calls.append((method, url, headers, body))
        status = next(statuses)
        return Response(status, {"ok": status == 200})

    http_client.set_transport(fake)

    response = http_client.call(
        "POST",
        "https://alerts.example.com",
        json={"text": "failed"},
    )

    assert response.status == 200
    assert len(calls) == 3


def test_call_does_not_retry_permanent_failure(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "unit-test-token")
    calls = []

    def fake(method, url, headers, body):
        calls.append((method, url, headers, body))
        return Response(400, {"ok": False})

    http_client.set_transport(fake)

    response = http_client.call("POST", "https://alerts.example.com")

    assert response.status == 400
    assert len(calls) == 1
