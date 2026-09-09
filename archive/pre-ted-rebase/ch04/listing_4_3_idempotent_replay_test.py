from importer import (
    ApiResult,
    parse_customer,
    send_with_retry,
)


def fake_sender(status):
    def sender(request):
        return ApiResult(status=status, body="")
    return sender


def test_conflict_is_idempotent_replay():
    raw = {
        "source_id": "C-1",
        "email": "x@y.co",
        "name": "X",
    }
    row = parse_customer(raw)
    result = send_with_retry(
        row,
        fake_sender(409),
        attempts=3,
    )
    assert result.status == 409
