import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone

from reminders.handler import Request, handle_snooze
from reminders.repository import (
    SQLiteReminderRepository,
    create_schema,
)
from reminders.service import SnoozeReminderService


@dataclass
class FrozenClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def _insert_reminder(
    connection: sqlite3.Connection,
    reminder_id: str,
    status: str,
) -> None:
    connection.execute(
        """
        INSERT INTO reminders (
            id,
            user_id,
            due_at,
            status,
            snoozed_until
        ) VALUES (?, ?, ?, ?, NULL)
        """,
        (
            reminder_id,
            "user-7",
            "2030-01-02T13:00:00+00:00",
            status,
        ),
    )
    connection.commit()


def _stored_value(
    connection: sqlite3.Connection,
    reminder_id: str,
) -> str | None:
    row = connection.execute(
        """
        SELECT snoozed_until
        FROM reminders
        WHERE id = ?
        """,
        (reminder_id,),
    ).fetchone()
    return row["snoozed_until"]


def main() -> None:
    connection = sqlite3.connect(":memory:")
    create_schema(connection)
    _insert_reminder(
        connection,
        "rem-pending",
        "pending",
    )
    _insert_reminder(
        connection,
        "rem-complete",
        "completed",
    )

    repository = SQLiteReminderRepository(connection)
    service = SnoozeReminderService(
        repository,
        FrozenClock(
            datetime(
                2030,
                1,
                2,
                12,
                0,
                tzinfo=timezone.utc,
            )
        ),
    )

    pending = handle_snooze(
        Request(
            user_id="user-7",
            reminder_id="rem-pending",
            body={"minutes": 15},
        ),
        service,
    )
    completed = handle_snooze(
        Request(
            user_id="user-7",
            reminder_id="rem-complete",
            body={"minutes": 15},
        ),
        service,
    )

    print(
        "pending_response="
        + json.dumps(
            {
                "status": pending.status,
                "body": pending.body,
            },
            sort_keys=True,
            indent=2,
        )
    )
    print(
        "pending_stored="
        + json.dumps(
            _stored_value(connection, "rem-pending")
        )
    )
    print(
        "completed_response="
        + json.dumps(
            {
                "status": completed.status,
                "body": completed.body,
            },
            sort_keys=True,
            indent=2,
        )
    )
    print(
        "completed_stored="
        + json.dumps(
            _stored_value(connection, "rem-complete")
        )
    )
    connection.close()


if __name__ == "__main__":
    main()
