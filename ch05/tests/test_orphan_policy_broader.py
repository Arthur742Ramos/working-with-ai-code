"""Broader checks for the orphan-product policy slice."""
import importlib.util
import sqlite3
import subprocess
import sys
from pathlib import Path

ORDER_ID = 7
EXPECTED_MESSAGE = (
    "order 7 references missing product 90233"
)
VALID_SUMMARY = {
    "order_id": 1,
    "customer": "cust-1031",
    "created": "2026-06-16T10:00:00",
    "items": [
        {
            "code": 5472,
            "name": "Widget-05472",
            "qty": 1,
            "line_total": 91.25,
        },
        {
            "code": 10343,
            "name": "Widget-10343",
            "qty": 3,
            "line_total": 1156.32,
        },
        {
            "code": 1914,
            "name": "Widget-01914",
            "qty": 4,
            "line_total": 292.2,
        },
        {
            "code": 35554,
            "name": "Widget-35554",
            "qty": 2,
            "line_total": 739.68,
        },
    ],
    "total": 2279.45,
}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def seed_database(work_dir):
    return subprocess.run(
        [sys.executable, "seed.py"],
        cwd=work_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def check_valid_summary(server, work_dir):
    con = sqlite3.connect(work_dir / "shop.db")
    con.row_factory = sqlite3.Row
    try:
        observed = server.build_summary(con, 1)
    finally:
        con.close()
    if observed != VALID_SUMMARY:
        print("FAIL: test_neighboring_valid_order_unchanged")
        print(f"expected: {VALID_SUMMARY}")
        print(f"observed: {observed}")
        return False
    print("PASS: test_neighboring_valid_order_unchanged")
    return True


def check_api_boundary(server):
    handler = object.__new__(server.Handler)
    handler.path = f"/orders/{ORDER_ID}/summary"
    responses = []
    handler._send = lambda status, payload: responses.append(
        (status, payload)
    )
    server.Handler.do_GET(handler)
    expected = (422, {"error": EXPECTED_MESSAGE})
    observed = responses[0] if responses else None
    if observed != expected:
        print("FAIL: test_orphan_fails_closed_at_api_boundary")
        print(f"expected: {expected}")
        print(f"observed: {observed}")
        return False
    print("PASS: test_orphan_fails_closed_at_api_boundary")
    return True


def main():
    if len(sys.argv) > 2:
        print("usage: test_orphan_policy_broader.py [WORK_DIR]")
        return 2

    work_dir = (
        Path(sys.argv[1])
        if len(sys.argv) == 2
        else Path(__file__).resolve().parents[1]
    ).resolve()
    seed_result = seed_database(work_dir)
    if seed_result.returncode != 0:
        print("SETUP ERROR: deterministic seed failed")
        print(seed_result.stdout, end="")
        return 2

    server = load_module(
        "captured_incident_server_broader",
        work_dir / "server.py",
    )
    try:
        valid_passed = check_valid_summary(server, work_dir)
        boundary_passed = check_api_boundary(server)
    finally:
        server._log_file.close()

    return 0 if valid_passed and boundary_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
