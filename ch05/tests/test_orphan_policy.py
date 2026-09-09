"""Focused red check for the seeded orphan-product path."""
import importlib.util
import sqlite3
import subprocess
import sys
from pathlib import Path

ORDER_ID = 7
EXPECTED_CODE = 90233
EXPECTED_QTY = 2
EXPECTED_MESSAGE = (
    "order 7 references missing product 90233"
)
TEST_NAME = (
    "test_seeded_orphan_uses_explicit_missing_product_policy"
)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def print_failure(observed):
    print(f"FAIL: {TEST_NAME}")
    print(
        "expected: MissingProductError: "
        f"{EXPECTED_MESSAGE}"
    )
    print(f"observed: {observed}")


def main():
    if len(sys.argv) > 2:
        print("usage: test_orphan_policy.py [WORK_DIR]")
        return 2

    work_dir = (
        Path(sys.argv[1])
        if len(sys.argv) == 2
        else Path(__file__).resolve().parents[1]
    ).resolve()
    seed_result = subprocess.run(
        [sys.executable, "seed.py"],
        cwd=work_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if seed_result.returncode != 0:
        print("SETUP ERROR: deterministic seed failed")
        print(seed_result.stdout, end="")
        return 2

    server = load_module(
        "captured_incident_server",
        work_dir / "server.py",
    )
    con = sqlite3.connect(work_dir / "shop.db")
    con.row_factory = sqlite3.Row
    try:
        orphan_rows = con.execute(
            "SELECT oi.code, oi.qty"
            " FROM order_items oi"
            " LEFT JOIN products p ON p.code = oi.code"
            " WHERE oi.order_id = ? AND p.code IS NULL",
            (ORDER_ID,),
        ).fetchall()
        observed_rows = [
            (row["code"], row["qty"])
            for row in orphan_rows
        ]
        expected_rows = [(EXPECTED_CODE, EXPECTED_QTY)]
        if observed_rows != expected_rows:
            print("SETUP ERROR: deterministic orphan drifted")
            print(f"expected rows: {expected_rows}")
            print(f"observed rows: {observed_rows}")
            return 2

        print(
            "DETERMINISTIC SEED: "
            f"order={ORDER_ID} "
            f"code={EXPECTED_CODE} "
            f"qty={EXPECTED_QTY}"
        )
        try:
            server.build_summary(con, ORDER_ID)
        except Exception as exc:
            expected_type = getattr(
                server,
                "MissingProductError",
                None,
            )
            exported_type_name = getattr(
                expected_type,
                "__name__",
                None,
            )
            observed_type = type(exc).__name__
            if (
                exported_type_name == "MissingProductError"
                and isinstance(expected_type, type)
                and isinstance(exc, expected_type)
                and observed_type == "MissingProductError"
                and str(exc) == EXPECTED_MESSAGE
            ):
                print(f"PASS: {TEST_NAME}")
                print(
                    f"observed: {observed_type}: {exc}"
                )
                return 0
            print_failure(f"{observed_type}: {exc}")
            return 1

        print_failure("no exception")
        return 1
    finally:
        con.close()
        server._log_file.close()


if __name__ == "__main__":
    raise SystemExit(main())
