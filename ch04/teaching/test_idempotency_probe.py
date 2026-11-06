from http.client import HTTPConnection
import json
import threading

import pytest

from idempotency_probe import make_server, run_probe
from importer_current import request_fingerprint


def test_service_with_distinct_conflict_status_rejects_changed_payload():
    assert run_probe(422) == {
        "statuses": [201, 409, 422],
        "conflicting_payload_accepted": False,
        "stored_customers": 1,
    }


def test_service_that_reuses_409_rejects_changed_payload():
    assert run_probe(409) == {
        "statuses": [201, 409, 409],
        "conflicting_payload_accepted": False,
        "stored_customers": 1,
    }


@pytest.mark.parametrize("conflict_status", [409, 422])
@pytest.mark.parametrize("first_path, other_path", [
    ("/customers", "/other"), ("/other", "/customers"),
])
def test_different_path_is_not_a_replay(
    conflict_status, first_path, other_path,
):
    server, records = make_server(conflict_status)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    payload = {"external_id": "C-1", "email": "x@y.co", "name": "X"}
    key = "same-key"

    def post(path):
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=3)
        try:
            connection.request("POST", path, json.dumps(payload), {
                "Content-Type": "application/json", "Idempotency-Key": key,
            })
            response = connection.getresponse()
            return response.status, response.read().decode("utf-8")
        finally:
            connection.close()

    try:
        assert post(first_path) == (201, "created")
        assert post(other_path) == (conflict_status, "different request")
        status, body = post(first_path)
        assert status == 409
        assert json.loads(body) == {
            "code": "idempotent_replay", "key": key,
            "request_sha256": request_fingerprint({
                "path": first_path, "json": payload,
            }),
        }
        assert len(records) == 1
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
