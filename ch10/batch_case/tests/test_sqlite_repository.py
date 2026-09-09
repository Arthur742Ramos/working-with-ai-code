import sqlite3
from collections.abc import Callable
from contextlib import closing
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from reminders.domain import Reminder, ReminderStatus
from reminders.repository import (
    ReminderWriteError,
    SQLiteReminderRepository,
    create_schema,
)


Seed = Callable[..., None]
DUE = datetime(2030, 1, 2, 13, tzinfo=timezone.utc)
SNOOZED = datetime(
    2030, 1, 2, 12, 15, tzinfo=timezone.utc,
)


def test_schema_rejects_null_reminder_id(
    connection: sqlite3.Connection,
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            """
            INSERT INTO reminders (
                id,
                user_id,
                due_at,
                status,
                snoozed_until
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                None,
                "user-7",
                "2030-01-02T13:00:00+00:00",
                "pending",
                None,
            ),
        )


def test_get_for_user_maps_unsnoozed_reminder(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder()
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


def test_get_for_user_is_owner_scoped(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder(user_id="user-8")
    repository = SQLiteReminderRepository(connection)

    result = repository.get_for_user(
        "rem-1",
        "user-7",
    )

    assert result is None


def test_get_for_user_is_reminder_id_scoped(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder(
        reminder_id="rem-1",
        user_id="user-7",
    )
    repository = SQLiteReminderRepository(connection)

    result = repository.get_for_user(
        "rem-2",
        "user-7",
    )

    assert result is None


def test_snooze_timestamp_round_trips(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder()
    repository = SQLiteReminderRepository(connection)
    original = repository.get_for_user(
        "rem-1",
        "user-7",
    )
    assert original is not None
    updated = replace(
        original,
        snoozed_until=datetime(
            2030,
            1,
            2,
            12,
            15,
            tzinfo=timezone.utc,
        ),
    )

    repository.save(updated)
    reloaded = repository.get_for_user(
        "rem-1",
        "user-7",
    )

    assert reloaded == updated


def test_save_commits_for_another_connection(
    tmp_path: Path,
) -> None:
    database = tmp_path / "reminders.db"
    with closing(sqlite3.connect(database)) as writer:
        create_schema(writer)
        writer.execute(
            """
            INSERT INTO reminders (
                id,
                user_id,
                due_at,
                status,
                snoozed_until
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                "rem-1",
                "user-7",
                DUE.isoformat(),
                "pending",
                None,
            ),
        )
        writer.commit()
        repository = SQLiteReminderRepository(writer)
        original = repository.get_for_user(
            "rem-1",
            "user-7",
        )
        assert original is not None
        updated = replace(
            original,
            snoozed_until=SNOOZED,
        )

        repository.save(updated)

        with closing(sqlite3.connect(database)) as reader:
            row = reader.execute(
                """
                SELECT snoozed_until
                FROM reminders
                WHERE id = ? AND user_id = ?
                """,
                ("rem-1", "user-7"),
            ).fetchone()

    assert row is not None
    assert row[0] == SNOOZED.isoformat()


def test_unknown_status_is_rejected(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    connection.execute(
        "PRAGMA ignore_check_constraints = ON"
    )
    seed_reminder(status="paused")
    connection.execute(
        "PRAGMA ignore_check_constraints = OFF"
    )
    repository = SQLiteReminderRepository(connection)

    with pytest.raises(ValueError, match="paused"):
        repository.get_for_user("rem-1", "user-7")


def test_naive_stored_timestamp_is_rejected(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder(
        due_at="2030-01-02T13:00:00"
    )
    repository = SQLiteReminderRepository(connection)

    with pytest.raises(ValueError, match="timezone-aware"):
        repository.get_for_user("rem-1", "user-7")


def test_save_updates_only_the_owner_row(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    seed_reminder()
    repository = SQLiteReminderRepository(connection)
    reminder = Reminder(
        id="rem-1",
        user_id="user-7",
        due_at=datetime(
            2030,
            1,
            2,
            13,
            tzinfo=timezone.utc,
        ),
        status=ReminderStatus.PENDING,
        snoozed_until=datetime(
            2030,
            1,
            2,
            12,
            15,
            tzinfo=timezone.utc,
        ),
    )

    result = repository.save(reminder)

    assert result is reminder
    row = connection.execute(
        """
        SELECT snoozed_until
        FROM reminders
        WHERE id = ? AND user_id = ?
        """,
        ("rem-1", "user-7"),
    ).fetchone()
    assert row["snoozed_until"] == (
        "2030-01-02T12:15:00+00:00"
    )


def test_save_rejects_another_users_row(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    original = "2030-01-02T14:00:00+00:00"
    seed_reminder(
        user_id="user-8",
        snoozed_until=original,
    )
    repository = SQLiteReminderRepository(connection)
    wrong_owner = Reminder(
        id="rem-1",
        user_id="user-7",
        due_at=DUE,
        status=ReminderStatus.PENDING,
        snoozed_until=SNOOZED,
    )

    with pytest.raises(ReminderWriteError):
        repository.save(wrong_owner)

    row = connection.execute(
        """
        SELECT user_id, snoozed_until
        FROM reminders
        WHERE id = ?
        """,
        ("rem-1",),
    ).fetchone()
    assert row["user_id"] == "user-8"
    assert row["snoozed_until"] == original


def test_save_rejects_another_reminder_id(
    connection: sqlite3.Connection,
    seed_reminder: Seed,
) -> None:
    original = "2030-01-02T14:00:00+00:00"
    seed_reminder(
        reminder_id="rem-1",
        user_id="user-7",
        snoozed_until=original,
    )
    repository = SQLiteReminderRepository(connection)
    wrong_id = Reminder(
        id="rem-2",
        user_id="user-7",
        due_at=DUE,
        status=ReminderStatus.PENDING,
        snoozed_until=SNOOZED,
    )

    with pytest.raises(ReminderWriteError):
        repository.save(wrong_id)

    row = connection.execute(
        """
        SELECT id, snoozed_until
        FROM reminders
        WHERE id = ?
        """,
        ("rem-1",),
    ).fetchone()
    assert row["id"] == "rem-1"
    assert row["snoozed_until"] == original


def test_zero_row_update_fails_closed(
    connection: sqlite3.Connection,
) -> None:
    repository = SQLiteReminderRepository(connection)
    reminder = Reminder(
        id="missing",
        user_id="user-7",
        due_at=datetime(
            2030,
            1,
            2,
            13,
            tzinfo=timezone.utc,
        ),
        status=ReminderStatus.PENDING,
        snoozed_until=datetime(
            2030,
            1,
            2,
            12,
            15,
            tzinfo=timezone.utc,
        ),
    )

    with pytest.raises(ReminderWriteError):
        repository.save(reminder)
