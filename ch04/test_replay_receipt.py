"""The printed replay-receipt check against the maintained importer."""

import json

import pytest

from importer_current import (
    ApiResult, build_request, parse_customer,
    request_fingerprint, send_with_retry,
)


def test_replay_requires_matching_receipt():
    raw = {
        "source_id": "C-1", "email": "x@y.co",
        "name": "X",
    }
    original = parse_customer(raw)
    changed = parse_customer({**raw, "email": "z@y.co"})
    receipt = json.dumps({
        "code": "idempotent_replay",
        "key": original.key,
        "request_sha256": request_fingerprint(
            build_request(original)
        ),
    })

    def sender(_):
        return ApiResult(409, receipt)

    assert send_with_retry(original, sender).status == 409
    assert changed.key == original.key
    with pytest.raises(RuntimeError):
        send_with_retry(changed, sender)
    with pytest.raises(RuntimeError):
        send_with_retry(
            original, lambda _: ApiResult(409, ""),
        )
