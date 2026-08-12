import sqlite3
from datetime import datetime

from reminders.domain import (
    Reminder,
    ReminderStatus,
    normalize_utc,
)


class ReminderWriteError(RuntimeError):
    pass


def create_schema(connection: sqlite3.Connection) -> None:
    with connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id TEXT PRIMARY KEY NOT NULL,
                user_id TEXT NOT NULL,
                due_at TEXT NOT NULL,
                status TEXT NOT NULL CHECK (
                    status IN ('pending', 'completed')
                ),
                snoozed_until TEXT NULL
            )
            """
        )


def _parse_optional_timestamp(
    value: str | None,
) -> datetime | None:
    if value is None:
        return None
    return normalize_utc(datetime.fromisoformat(value))


def _parse_required_timestamp(value: str) -> datetime:
    parsed = _parse_optional_timestamp(value)
    if parsed is None:
        raise ValueError("required timestamp was NULL")
    return parsed


def _format_optional_timestamp(
    value: datetime | None,
) -> str | None:
    if value is None:
        return None
    return normalize_utc(value).isoformat()


def _row_to_reminder(row: sqlite3.Row) -> Reminder:
    return Reminder(
        id=row["id"],
        user_id=row["user_id"],
        due_at=_parse_required_timestamp(row["due_at"]),
        status=ReminderStatus(row["status"]),
        snoozed_until=_parse_optional_timestamp(
            row.get("snoozed_until")
        ),
    )


class SQLiteReminderRepository:
    def __init__(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        self._connection = connection
        self._connection.row_factory = sqlite3.Row

    def get_for_user(
        self,
        reminder_id: str,
        user_id: str,
    ) -> Reminder | None:
        row = self._connection.execute(
            """
            SELECT
                id,
                user_id,
                due_at,
                status,
                snoozed_until
            FROM reminders
            WHERE id = ? AND user_id = ?
            """,
            (reminder_id, user_id),
        ).fetchone()
        if row is None:
            return None
        return _row_to_reminder(row)

    def save(self, reminder: Reminder) -> Reminder:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE reminders
                SET snoozed_until = ?
                WHERE id = ? AND user_id = ?
                """,
                (
                    _format_optional_timestamp(
                        reminder.snoozed_until
                    ),
                    reminder.id,
                    reminder.user_id,
                ),
            )
            if cursor.rowcount != 1:
                raise ReminderWriteError(reminder.id)
        return reminder
