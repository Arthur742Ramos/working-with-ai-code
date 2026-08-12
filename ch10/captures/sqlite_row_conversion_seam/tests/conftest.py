import sqlite3
from collections.abc import Callable, Iterator

import pytest

from reminders.repository import create_schema


@pytest.fixture
def connection() -> Iterator[sqlite3.Connection]:
    value = sqlite3.connect(":memory:")
    create_schema(value)
    yield value
    value.close()


@pytest.fixture
def seed_reminder(
    connection: sqlite3.Connection,
) -> Callable[..., None]:
    def seed(
        reminder_id: str = "rem-1",
        user_id: str = "user-7",
        due_at: str = "2030-01-02T13:00:00+00:00",
        status: str = "pending",
        snoozed_until: str | None = None,
    ) -> None:
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
                reminder_id,
                user_id,
                due_at,
                status,
                snoozed_until,
            ),
        )
        connection.commit()

    return seed
