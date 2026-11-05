"""Fail-closed checks for the subsequent replay hardening."""

import json

import pytest

from importer_current import (
    ApiResult, TRANSIENT, build_request, parse_customer,
    request_fingerprint, run_import, send_with_retry,
)


RAW = {"source_id": "C-1", "email": "a@example.com", "name": "A"}
ROW = parse_customer(RAW)


def signal(row=ROW):
    return {
        "code": "idempotent_replay",
        "key": row.key,
        "request_sha256": request_fingerprint(build_request(row)),
    }


def test_matching_replay_returns_without_retry(monkeypatch):
    def no_sleep(_):
        pytest.fail("replay must not retry")

    monkeypatch.setattr("importer_current.time.sleep", no_sleep)
    calls = []

    def sender(request):
        calls.append(request)
        return ApiResult(409, json.dumps(signal()))

    assert send_with_retry(ROW, sender).status == 409
    assert len(calls) == 1


@pytest.mark.parametrize("body", [
    "", "already created", "{", "null", "[]", "true", "409",
    '{}', json.dumps({"code": "idempotent_replay"}),
    json.dumps({**signal(), "code": "different_conflict"}),
    json.dumps({**signal(), "key": "another-key"}),
    json.dumps({**signal(), "request_sha256": "wrong"}),
    json.dumps({**signal(), "request_sha256": None}),
    json.dumps({**signal(), "key": [ROW.key]}),
])
def test_unverified_conflict_fails_once(body, monkeypatch):
    monkeypatch.setattr(
        "importer_current.time.sleep",
        lambda _: pytest.fail("conflicts must not retry"),
    )
    calls = []

    def sender(request):
        calls.append(request)
        return ApiResult(409, body)

    with pytest.raises(RuntimeError):
        send_with_retry(ROW, sender)
    assert len(calls) == 1


def test_same_key_changed_payload_rejects_old_receipt():
    changed = parse_customer({**RAW, "email": "b@example.com"})
    assert changed.key == ROW.key
    with pytest.raises(RuntimeError):
        send_with_retry(changed, lambda _: ApiResult(
            409, json.dumps(signal()),
        ))


def test_fingerprint_binds_path_and_every_payload_field():
    request = build_request(ROW)
    digest = request_fingerprint(request)
    assert request_fingerprint({**request, "path": "/other"}) != digest
    for field in request["json"]:
        changed = {**request, "json": {**request["json"], field: "changed"}}
        assert request_fingerprint(changed) != digest


@pytest.mark.parametrize("status", sorted(TRANSIENT))
def test_retry_keeps_identity_and_backoff(status, monkeypatch):
    sleeps, calls = [], []
    monkeypatch.setattr("importer_current.time.sleep", sleeps.append)

    def sender(request):
        calls.append(request)
        return ApiResult(status if len(calls) < 3 else 201, "")

    assert send_with_retry(ROW, sender).status == 201
    assert sleeps == [1, 2]
    assert calls == [build_request(ROW)] * 3


def test_exhausted_transient_failure(monkeypatch):
    sleeps = []
    monkeypatch.setattr("importer_current.time.sleep", sleeps.append)
    with pytest.raises(RuntimeError):
        send_with_retry(ROW, lambda _: ApiResult(503, "busy"))
    assert sleeps == [1, 2]


def test_dry_run_and_live_counts():
    rows = [RAW, {**RAW, "source_id": ""}]
    def no_send(_):
        pytest.fail("dry run must not send")

    assert run_import(rows, no_send) == {
        "validated": 1, "sent": 0, "invalid": 1, "send_failed": 0,
    }
    assert run_import(rows, lambda _: ApiResult(409, ""), False) == {
        "validated": 1, "sent": 0, "invalid": 1, "send_failed": 1,
    }
    assert run_import(rows, lambda _: ApiResult(
        409, json.dumps(signal()),
    ), False) == {
        "validated": 1, "sent": 1, "invalid": 1, "send_failed": 0,
    }


def test_matching_signal_does_not_override_other_failure():
    with pytest.raises(RuntimeError):
        send_with_retry(ROW, lambda _: ApiResult(400, json.dumps(signal())))
