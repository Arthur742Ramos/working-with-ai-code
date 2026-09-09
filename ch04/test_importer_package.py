"""Tests for the package-local staged customer importer."""

from importer import (
    ApiResult,
    parse_customer,
    run_import,
    send_with_retry,
)


def fake_sender(*statuses):
    """Return a sender that yields the given statuses in order."""
    calls = iter(statuses)

    def sender(request):
        return ApiResult(status=next(calls), body="")

    return sender


def test_parse_rejects_missing_fields():
    try:
        parse_customer({"source_id": "", "email": "a@b.co", "name": "A"})
    except ValueError:
        return
    raise AssertionError("expected ValueError for missing source_id")


def test_parse_strips_whitespace_and_lowercases_email():
    row = parse_customer(
        {"source_id": " C-1 ", "email": " X@Y.CO ", "name": " Ann "}
    )
    assert row.source_id == "C-1"
    assert row.email == "x@y.co"
    assert row.name == "Ann"


def test_key_is_stable_for_same_source_id():
    a = parse_customer({"source_id": "C-1", "email": "x@y.co", "name": "X"})
    b = parse_customer({"source_id": "C-1", "email": "z@y.co", "name": "X"})
    assert a.key == b.key


def test_retry_succeeds_after_transient_failures(monkeypatch):
    monkeypatch.setattr("importer.time.sleep", lambda _: None)
    row = parse_customer({"source_id": "C-1", "email": "x@y.co", "name": "X"})
    result = send_with_retry(row, fake_sender(500, 500, 201), attempts=3)
    assert result.status == 201


def test_retry_stops_on_nonretryable():
    row = parse_customer({"source_id": "C-1", "email": "x@y.co", "name": "X"})
    try:
        send_with_retry(row, fake_sender(400), attempts=3)
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError for 400")


def test_dry_run_sends_nothing():
    rows = [{"source_id": "C-1", "email": "x@y.co", "name": "X"}]

    def exploding_sender(request):
        raise AssertionError("dry run must not call the sender")

    counts = run_import(rows, exploding_sender, dry_run=True)
    assert counts["validated"] == 1
    assert counts["sent"] == 0


def test_conflict_is_idempotent_replay():
    row = parse_customer({"source_id": "C-1", "email": "x@y.co", "name": "X"})
    result = send_with_retry(row, fake_sender(409), attempts=3)
    assert result.status == 409
