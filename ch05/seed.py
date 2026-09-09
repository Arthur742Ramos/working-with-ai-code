"""Seed a reproducible SQLite DB for the demo.

Builds three tables:
  products     - LARGE table, no index on `code`
  orders       - one row per order
  order_items  - many rows per order (line items)

Run:
  python3 seed.py
"""
import os
import random
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "shop.db")

# Fixed seed so every run produces the same DB.
RANDOM_SEED = 1729

# A large product catalog. Codes run 1..N_PRODUCTS.
# There is NO index on products.code, so a lookup by
# code is a full table scan.
N_PRODUCTS = 40000

# Order ids run 1..N_ORDERS.
N_ORDERS = 200

# Product codes >= ORPHAN_BASE never exist in products.
# An order_item pointing at one of these is "orphaned"
# and will crash the per-item lookup.
ORPHAN_BASE = 90000


def build_schema(con):
    cur = con.cursor()
    cur.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;

        CREATE TABLE products (
            id    INTEGER PRIMARY KEY,
            code  INTEGER NOT NULL,
            name  TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            id       INTEGER PRIMARY KEY,
            customer TEXT NOT NULL,
            created  TEXT NOT NULL
        );

        CREATE TABLE order_items (
            id       INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            code     INTEGER NOT NULL,
            qty      INTEGER NOT NULL
        );
        """
    )
    con.commit()


def seed_products(con, rng):
    rows = []
    for code in range(1, N_PRODUCTS + 1):
        name = "Widget-%05d" % code
        price = round(rng.uniform(1.0, 500.0), 2)
        rows.append((code, code, name, price))
    con.executemany(
        "INSERT INTO products (id, code, name, price)"
        " VALUES (?, ?, ?, ?)",
        rows,
    )
    con.commit()


def seed_orders(con, rng):
    order_rows = []
    item_rows = []
    item_id = 1

    for oid in range(1, N_ORDERS + 1):
        cust = "cust-%04d" % rng.randint(1, 9999)
        created = "2026-06-%02dT10:00:00" % rng.randint(
            1, 28
        )
        order_rows.append((oid, cust, created))

        # Mix of sizes. Every 5th order is "large".
        if oid % 5 == 0:
            n_items = rng.randint(40, 80)
        else:
            n_items = rng.randint(2, 6)

        # Roughly every 7th order has one orphaned
        # line item that points at a missing product.
        orphan = (oid % 7 == 0)
        orphan_slot = rng.randint(0, n_items - 1)

        for slot in range(n_items):
            if orphan and slot == orphan_slot:
                code = ORPHAN_BASE + rng.randint(0, 999)
            else:
                code = rng.randint(1, N_PRODUCTS)
            qty = rng.randint(1, 4)
            item_rows.append(
                (item_id, oid, code, qty)
            )
            item_id += 1

    con.executemany(
        "INSERT INTO orders (id, customer, created)"
        " VALUES (?, ?, ?)",
        order_rows,
    )
    con.executemany(
        "INSERT INTO order_items"
        " (id, order_id, code, qty)"
        " VALUES (?, ?, ?, ?)",
        item_rows,
    )
    con.commit()
    return len(order_rows), len(item_rows)


def main():
    rng = random.Random(RANDOM_SEED)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    try:
        build_schema(con)
        seed_products(con, rng)
        n_orders, n_items = seed_orders(con, rng)
    finally:
        con.close()

    print("Seeded %s" % DB_PATH)
    print("  products: %d" % N_PRODUCTS)
    print("  orders:   %d" % n_orders)
    print("  items:    %d" % n_items)


if __name__ == "__main__":
    main()
