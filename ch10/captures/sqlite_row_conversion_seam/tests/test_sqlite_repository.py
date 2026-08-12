import sqlite3
from collections.abc import Callable
from datetime import datetime, timezone

from reminders.domain import Reminder, ReminderStatus


Seed = Callable[..., None]
DUE = datetime(2030, 1, 2, 13, tzinfo=timezone.utc)


def test_get_for_user_maps_unsnoozed_reminder(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder()
    from reminders.repository import SQLiteReminderRepository

    repository = SQLiteReminderRepository(connection)

    result = repository.get_for_user(
        "rem-1",
        "user-7",
    )

    assert result == Reminder(
        id="rem-1",
        user_id="user-7",
        due_at=DUE,
        status=ReminderStatus.PENDING,
        snoozed_until=None,
    )
