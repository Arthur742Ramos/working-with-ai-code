import sqlite3
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from reminders.handler import Request, handle_snooze
from reminders.repository import SQLiteReminderRepository
from reminders.service import SnoozeReminderService


Seed = Callable[..., None]
NOW = datetime(2030, 1, 2, 12, tzinfo=timezone.utc)


@dataclass
class FrozenClock:
    value: datetime

    def now(self) -> datetime:
        return self.value


def make_service(
    connection: sqlite3.Connection,
) -> SnoozeReminderService:
    return SnoozeReminderService(
        SQLiteReminderRepository(connection),
        FrozenClock(NOW),
    )


def stored_snooze(
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


def test_owner_snoozes_pending_reminder(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder()
    service = make_service(connection)
    request = Request(
        "user-7",
        "rem-1",
        {"minutes": 15},
    )

    response = handle_snooze(request, service)

    assert response.status == 200
    assert response.body == {
        "id": "rem-1",
        "snoozed_until": (
            "2030-01-02T12:15:00+00:00"
        ),
    }
    assert stored_snooze(connection, "rem-1") == (
        "2030-01-02T12:15:00+00:00"
    )


def test_second_identity_id_and_duration_compose(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder(
        reminder_id="rem-2",
        user_id="user-8",
    )
    service = make_service(connection)
    request = Request(
        "user-8",
        "rem-2",
        {"minutes": 60},
    )

    response = handle_snooze(request, service)

    assert response.status == 200
    assert response.body == {
        "id": "rem-2",
        "snoozed_until": (
            "2030-01-02T13:00:00+00:00"
        ),
    }
    assert stored_snooze(connection, "rem-2") == (
        "2030-01-02T13:00:00+00:00"
    )


def test_completed_reminder_stays_unchanged(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder(status="completed")
    service = make_service(connection)
    request = Request(
        "user-7",
        "rem-1",
        {"minutes": 15},
    )

    response = handle_snooze(request, service)

    assert response.status == 409
    assert response.body == {
        "error": "reminder_completed"
    }
    assert stored_snooze(connection, "rem-1") is None


def test_other_user_sees_not_found_and_no_write(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder(user_id="user-8")
    service = make_service(connection)
    request = Request(
        "user-7",
        "rem-1",
        {"minutes": 15},
    )

    response = handle_snooze(request, service)

    assert response.status == 404
    assert response.body == {"error": "not_found"}
    assert stored_snooze(connection, "rem-1") is None
