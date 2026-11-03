"""Follow-on regression: status mapping must not hide the integrity incident."""
import contextlib
import importlib.util
import io
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SOURCE_ROOT = Path(__file__).resolve().parents[1]
MISSING_MESSAGE = "order 7 references missing product 90233"


class RequestLoggingTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        root = Path(self.workspace.name)
        shutil.copy2(SOURCE_ROOT / "server.py", root / "server.py")
        spec = importlib.util.spec_from_file_location("logging_server", root / "server.py")
        self.server = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.server)
        self.addCleanup(self.server._log_file.close)
        with sqlite3.connect(self.server.DB_PATH) as con:
            con.executescript("""
                CREATE TABLE orders (id INTEGER, customer TEXT, created TEXT);
                CREATE TABLE order_items (id INTEGER, order_id INTEGER, code INTEGER, qty INTEGER);
                CREATE TABLE products (code INTEGER, name TEXT, price REAL);
                INSERT INTO orders VALUES (7, 'fixture', '2026-11-03');
                INSERT INTO order_items VALUES (1, 7, 90233, 2);
                INSERT INTO orders VALUES (1, 'valid', '2026-11-03');
                INSERT INTO order_items VALUES (2, 1, 42, 3);
                INSERT INTO products VALUES (42, 'Widget', 2.5);
            """)

    def request(self, path):
        handler = object.__new__(self.server.Handler)
        handler.path = path
        responses = []
        handler._send = lambda status, payload: responses.append((status, payload))
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), patch.object(
            self.server.time, "time", side_effect=[100.0, 100.125]
        ), patch.object(self.server.time, "strftime", return_value="TEST-TIME"):
            handler.do_GET()
        self.assertEqual(len(responses), 1)
        return responses[0], stderr.getvalue()

    def test_orphan_422_keeps_correlated_error_log(self):
        response, log = self.request("/orders/7/summary")
        self.assertEqual(response, (422, {"error": MISSING_MESSAGE}))
        self.assertEqual(
            log,
            "TEST-TIME ERROR order=7 422 125.0ms " + MISSING_MESSAGE + "\n",
            "the 422 response must retain the error, order, status, elapsed time and missing code",
        )
        self.assertEqual(Path(self.server.LOG_PATH).read_text(), log)
        self.assertNotIn(7, self.server._cache)

    def test_unexpected_500_keeps_traceback(self):
        with patch.object(self.server, "get_summary", side_effect=RuntimeError("fixture failure")):
            response, log = self.request("/orders/7/summary")
        self.assertEqual(response, (500, {"error": "internal error"}))
        self.assertTrue(log.startswith("TEST-TIME ERROR order=7 125.0ms fixture failure\n"))
        self.assertIn("Traceback (most recent call last):", log)
        self.assertIn("RuntimeError: fixture failure", log)
        self.assertEqual(Path(self.server.LOG_PATH).read_text(), log)

    def test_valid_200_keeps_cache_logs(self):
        first, log = self.request("/orders/1/summary")
        self.assertEqual(first[0], 200)
        self.assertEqual(first[1]["total"], 7.5)
        self.assertEqual(log, "TEST-TIME INFO order=1 200 125.0ms cache=MISS items=1\n")
        second, log = self.request("/orders/1/summary")
        self.assertEqual(second, first)
        self.assertEqual(log, "TEST-TIME INFO order=1 200 125.0ms cache=HIT items=1\n")

    def test_missing_order_404_keeps_log(self):
        response, log = self.request("/orders/99/summary")
        self.assertEqual(response, (404, {"error": "no such order"}))
        self.assertEqual(log, "TEST-TIME INFO order=99 404 125.0ms\n")


def main():
    global SOURCE_ROOT
    if len(sys.argv) > 2:
        print("usage: test_request_logging.py [SERVER_DIR]")
        return 2
    if len(sys.argv) == 2:
        SOURCE_ROOT = Path(sys.argv[1]).resolve()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RequestLoggingTests)
    result = unittest.TestResult()
    suite.run(result)
    # Deliberately stable command output; full details remain available through unittest.
    for test, _ in result.failures:
        print("FAIL: " + test._testMethodName)
    for test, error in result.errors:
        print("ERROR: " + test._testMethodName)
        print(error)
    print("CHECKS: %d; failures=%d; errors=%d" % (result.testsRun, len(result.failures), len(result.errors)))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
