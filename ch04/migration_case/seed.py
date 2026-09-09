"""Build the deterministic package-local SQLite migration fixture."""

from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "shop.db"

LEGACY_ROWS = [
    (1, "Jane Doe", "Jane@Example.com", "03/15/2024", "1"),
    (2, "Acme LLC", "  ops@acme.io ", "12/01/2023", "2"),
    (3, "Bob Smith", "bob@example.com", "07/04/2024", "1"),
]


def load_schema(name: str) -> str:
    return (HERE / name).read_text(encoding="utf-8")


def build(
    db_path: Path = DB_PATH,
    *,
    announce: bool = True,
) -> Path:
    db_path = Path(db_path)
    db_path.unlink(missing_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.executescript(load_schema("schema_legacy.sql"))
        connection.executescript(load_schema("schema_target.sql"))
        connection.executemany(
            "INSERT INTO legacy_users "
            "(id, name, email, created, type) "
            "VALUES (?, ?, ?, ?, ?)",
            LEGACY_ROWS,
        )
        connection.commit()
        count = connection.execute(
            "SELECT COUNT(*) FROM legacy_users"
        ).fetchone()[0]

    if announce:
        print(f"Built {db_path}")
        print(f"legacy_users seeded with {count} rows")
        print(
            "Target tables ready: accounts, "
            "account_migration_audit (empty)"
        )
    return db_path


if __name__ == "__main__":
    build()
