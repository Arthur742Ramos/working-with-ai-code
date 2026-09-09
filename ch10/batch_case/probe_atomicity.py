"""Fixed real-storage oracle; run with 'legacy' or 'batch'."""
import sqlite3
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from reminders.repository import (
    SQLiteReminderRepository,
    create_schema,
)

STAMP = datetime(2030, 1, 2, 12, 15, tzinfo=timezone.utc)


def seed(connection):
    create_schema(connection)
    with connection:
        connection.executemany(
            "INSERT INTO reminders VALUES (?, ?, ?, ?, ?)",
            [
                (rid, "user-7", STAMP.isoformat(),
                 "pending", None)
                for rid in ("rem-1", "rem-2")
            ],
        )
        connection.execute("""
            CREATE TRIGGER fail_second
            BEFORE UPDATE ON reminders
            WHEN NEW.id = 'rem-2'
            BEGIN
              SELECT RAISE(ABORT, 'injected write failure');
            END
        """)


def observe(connection):
    return connection.execute(
        "SELECT id, snoozed_until FROM reminders ORDER BY id"
    ).fetchall()


def run(route):
    with TemporaryDirectory() as directory:
        path = Path(directory) / "reminders.sqlite"
        writer = sqlite3.connect(path)
        observer = sqlite3.connect(path)
        try:
            seed(writer)
            repository = SQLiteReminderRepository(writer)
            before = observe(observer)
            reminders = [
                replace(repository.get_for_user(rid, "user-7"),
                        snoozed_until=STAMP)
                for rid in ("rem-1", "rem-2")
            ]
            try:
                if route == "legacy":
                    with writer:
                        for reminder in reminders:
                            repository.save(reminder)
                elif route == "batch":
                    repository.save_many(reminders)
                else:
                    raise ValueError(route)
            except sqlite3.IntegrityError as error:
                print(f"storage_error={error}")
            else:
                raise AssertionError("fault did not fire")
            after = observe(observer)
            print(f"before={before!r}")
            print(f"after={after!r}")
            assert after == before, "batch partially committed"
            print("atomicity=PASS")
        finally:
            observer.close()
            writer.close()


if __name__ == "__main__":
    run(sys.argv[1])
