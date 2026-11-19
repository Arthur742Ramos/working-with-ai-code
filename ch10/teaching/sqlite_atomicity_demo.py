import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory


def observe_batch(batch):
    with TemporaryDirectory() as directory:
        path = Path(directory) / "reminders.db"
        writer = sqlite3.connect(path)
        observer = sqlite3.connect(path)
        try:
            writer.executescript("""
                CREATE TABLE reminders (
                  id TEXT PRIMARY KEY, snoozed_until TEXT
                );
                INSERT INTO reminders VALUES ('r1', NULL);
                INSERT INTO reminders VALUES ('r2', NULL);
                CREATE TRIGGER fail_second
                BEFORE UPDATE ON reminders
                WHEN NEW.id = 'r2'
                BEGIN
                  SELECT RAISE(ABORT, 'injected failure');
                END;
            """)

            def update(reminder_id):
                writer.execute(
                    "UPDATE reminders "
                    "SET snoozed_until = ? "
                    "WHERE id = ?",
                    ("12:15", reminder_id),
                )

            try:
                with writer:
                    for reminder_id in ("r1", "r2"):
                        if batch:
                            update(reminder_id)
                        else:
                            with writer:
                                update(reminder_id)
            except sqlite3.IntegrityError as error:
                if str(error) != "injected failure":
                    raise
            else:
                raise AssertionError("failure did not fire")
            return observer.execute(
                "SELECT id, snoozed_until FROM reminders "
                "ORDER BY id"
            ).fetchall()
        finally:
            observer.close()
            writer.close()


print("legacy:", observe_batch(False))
print("batch:", observe_batch(True))
