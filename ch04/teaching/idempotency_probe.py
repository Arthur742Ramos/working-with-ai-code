"""Compare two endpoint contracts against the maintained importer.

Both servers are local fixtures. Their behavior is chosen for the exercise and
does not establish the contract of any real customer service.
"""

from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from importer_current import (
    ApiResult, parse_customer, send_with_retry,
)


def run_probe(conflict_status):
    """Send a create, a replay, and a conflicting request over local HTTP."""
    if conflict_status not in (409, 422):
        raise ValueError("conflict status must be 409 or 422")
    records = {}
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size))
            key = self.headers["Idempotency-Key"]
            with lock:
                if key not in records:
                    records[key] = payload
                    status, message = 201, "created"
                elif records[key] == payload:
                    identity = {
                        "method": "POST", "path": self.path,
                        "json": records[key],
                    }
                    encoded = json.dumps(
                        identity, sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=True, allow_nan=False,
                    ).encode("utf-8")
                    status = 409
                    message = json.dumps({
                        "code": "idempotent_replay", "key": key,
                        "request_sha256": hashlib.sha256(
                            encoded
                        ).hexdigest(),
                    })
                else:
                    status, message = conflict_status, "different payload"
            body = message.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    observed = []

    def sender(request):
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=3)
        try:
            headers = dict(request["headers"])
            headers["Content-Type"] = "application/json"
            connection.request(
                "POST", request["path"],
                body=json.dumps(request["json"]), headers=headers,
            )
            response = connection.getresponse()
            body = response.read().decode("utf-8")
            observed.append(response.status)
            return ApiResult(response.status, body)
        finally:
            connection.close()

    original = parse_customer({
        "source_id": "customer-1", "email": "a@example.test", "name": "A"
    })
    changed = parse_customer({
        "source_id": "customer-1", "email": "b@example.test", "name": "A"
    })
    try:
        send_with_retry(original, sender)
        send_with_retry(original, sender)
        try:
            send_with_retry(changed, sender)
            conflict_accepted = True
        except RuntimeError:
            conflict_accepted = False
    finally:
        server.shutdown()
        server.server_close()
        thread.join()

    return {
        "statuses": observed,
        "conflicting_payload_accepted": conflict_accepted,
        "stored_customers": len(records),
    }


if __name__ == "__main__":
    print("Distinct status for conflicting payload:")
    print(json.dumps(run_probe(422), indent=2))
    print("Same 409 for both meanings:")
    print(json.dumps(run_probe(409), indent=2))
