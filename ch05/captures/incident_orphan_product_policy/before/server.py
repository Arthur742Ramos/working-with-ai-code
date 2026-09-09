"""A small order service with a planted bug.

GET /orders/{id}/summary
    Returns a JSON summary of one order: its line
    items, each item's product name and price, and
    the order total.

Run:
  python3 server.py            # listens on :8080
  python3 server.py 8081       # custom port

The service keeps an in-memory cache of assembled
summaries keyed by order id, so a repeated request
for the same order is served from memory.
"""
import json
import os
import sqlite3
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "shop.db")
LOG_PATH = os.path.join(HERE, "server.log")

# In-memory summary cache: order_id -> summary dict.
_cache = {}
_cache_lock = threading.Lock()

# Single shared log file handle, guarded by a lock.
_log_lock = threading.Lock()
_log_file = open(LOG_PATH, "a", buffering=1)


def log(line):
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    msg = "%s %s" % (ts, line)
    with _log_lock:
        _log_file.write(msg + "\n")
        sys.stderr.write(msg + "\n")


def log_block(lines):
    # Write a multi-line block atomically so a
    # traceback is not interleaved with other
    # threads' log lines.
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    out = "".join(
        "%s %s\n" % (ts, ln) for ln in lines
    )
    with _log_lock:
        _log_file.write(out)
        sys.stderr.write(out)


def connect():
    # One connection per request/thread.
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def load_order(con, order_id):
    cur = con.execute(
        "SELECT id, customer, created"
        " FROM orders WHERE id = ?",
        (order_id,),
    )
    return cur.fetchone()


def load_items(con, order_id):
    cur = con.execute(
        "SELECT id, code, qty FROM order_items"
        " WHERE order_id = ?",
        (order_id,),
    )
    return cur.fetchall()


def lookup_product(con, code):
    # Filters on products.code, which is NOT indexed,
    # so SQLite scans the whole products table.
    cur = con.execute(
        "SELECT code, name, price"
        " FROM products WHERE code = ?",
        (code,),
    )
    return cur.fetchone()


def build_summary(con, order_id):
    order = load_order(con, order_id)
    if order is None:
        return None

    items = load_items(con, order_id)
    lines = []
    total = 0.0

    # Classic N+1: one product query per line item,
    # each an unindexed full scan.
    for item in items:
        product = lookup_product(con, item["code"])
        price = product["price"]
        line_total = price * item["qty"]
        total += line_total
        lines.append(
            {
                "code": item["code"],
                "name": product["name"],
                "qty": item["qty"],
                "line_total": round(line_total, 2),
            }
        )

    return {
        "order_id": order["id"],
        "customer": order["customer"],
        "created": order["created"],
        "items": lines,
        "total": round(total, 2),
    }


def get_summary(order_id):
    with _cache_lock:
        cached = _cache.get(order_id)
    if cached is not None:
        return cached, True

    con = connect()
    try:
        summary = build_summary(con, order_id)
    finally:
        con.close()

    if summary is not None:
        with _cache_lock:
            _cache[order_id] = summary
    return summary, False


class Handler(BaseHTTPRequestHandler):
    # Silence the default per-request stderr logging;
    # we do our own structured logging.
    def log_message(self, fmt, *args):
        return

    def _send(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header(
            "Content-Type", "application/json"
        )
        self.send_header(
            "Content-Length", str(len(body))
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        start = time.time()
        parts = self.path.strip("/").split("/")
        # Expect: orders/{id}/summary
        ok_shape = (
            len(parts) == 3
            and parts[0] == "orders"
            and parts[2] == "summary"
        )
        if not ok_shape:
            self._send(404, {"error": "not found"})
            return

        try:
            order_id = int(parts[1])
        except ValueError:
            self._send(400, {"error": "bad id"})
            return

        try:
            summary, hit = get_summary(order_id)
        except Exception as exc:
            elapsed = (time.time() - start) * 1000
            tb = traceback.format_exc()
            block = [
                "ERROR order=%d %.1fms %s"
                % (order_id, elapsed, exc)
            ]
            for tl in tb.rstrip().split("\n"):
                block.append("  " + tl)
            log_block(block)
            self._send(
                500, {"error": "internal error"}
            )
            return

        elapsed = (time.time() - start) * 1000
        if summary is None:
            log(
                "INFO order=%d 404 %.1fms"
                % (order_id, elapsed)
            )
            self._send(
                404, {"error": "no such order"}
            )
            return

        tag = "HIT" if hit else "MISS"
        log(
            "INFO order=%d 200 %.1fms cache=%s items=%d"
            % (
                order_id,
                elapsed,
                tag,
                len(summary["items"]),
            )
        )
        self._send(200, summary)


def main():
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if not os.path.exists(DB_PATH):
        sys.stderr.write(
            "Missing %s. Run seed.py first.\n"
            % DB_PATH
        )
        sys.exit(1)
    server = ThreadingHTTPServer(
        ("127.0.0.1", port), Handler
    )
    log("STARTUP listening on :%d" % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        log("SHUTDOWN")


if __name__ == "__main__":
    main()
