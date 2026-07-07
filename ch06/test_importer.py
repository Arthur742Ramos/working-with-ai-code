"""Tests for the chapter 6 importer.

Each test maps to a slice's inspection question: parsing rejects bad
rows and derives a stable key, retry handles transient versus
nonretryable failures, and dry run sends nothing. The final test
encodes a fact discovered after the first plan: the API returns 409
Conflict for a duplicate source_id and means "already created."
"""

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


def test_retry_succeeds_after_transient_failures():
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
    # The API returns 409 for a duplicate source_id and treats it as
    # "already created." A 409 must count as a successful send, not a
    # failure, or a retried batch inflates the failure count.
    row = parse_customer({"source_id": "C-1", "email": "x@y.co", "name": "X"})
    result = send_with_retry(row, fake_sender(409), attempts=3)
    assert result.status == 409
