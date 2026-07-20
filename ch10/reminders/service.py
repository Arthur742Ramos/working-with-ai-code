from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Protocol

from reminders.domain import (
    Reminder,
    ReminderStatus,
    normalize_utc,
)


ALLOWED_MINUTES = frozenset({5, 15, 30, 60})


class ReminderNotFound(LookupError):
    pass


class ReminderCompleted(RuntimeError):
    pass


class InvalidSnoozeDuration(ValueError):
    pass


class Clock(Protocol):
    def now(self) -> datetime: ...


class ReminderRepository(Protocol):
    def get_for_user(
        self,
        reminder_id: str,
        user_id: str,
    ) -> Reminder | None: ...

    def save(self, reminder: Reminder) -> Reminder: ...


class SnoozeService(Protocol):
    def execute(
        self,
        user_id: str,
        reminder_id: str,
        minutes: int,
    ) -> Reminder: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class SnoozeReminderService:
    def __init__(
        self,
        repository: ReminderRepository,
        clock: Clock,
    ) -> None:
        self._repository = repository
        self._clock = clock

    def execute(
        self,
        user_id: str,
        reminder_id: str,
        minutes: int,
    ) -> Reminder:
        if (
            type(minutes) is not int
            or minutes not in ALLOWED_MINUTES
        ):
            raise InvalidSnoozeDuration(minutes)

        reminder = self._repository.get_for_user(
            reminder_id,
            user_id,
        )
        if reminder is None:
            raise ReminderNotFound(reminder_id)
        if reminder.status is ReminderStatus.COMPLETED:
            raise ReminderCompleted(reminder_id)

        now = normalize_utc(self._clock.now())
        updated = replace(
            reminder,
            snoozed_until=(
                now + timedelta(minutes=minutes)
            ),
        )
        return self._repository.save(updated)
