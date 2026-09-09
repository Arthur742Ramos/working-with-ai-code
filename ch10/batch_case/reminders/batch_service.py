from dataclasses import replace
from datetime import timedelta
from typing import Protocol

from reminders.domain import (
    Reminder, ReminderStatus, normalize_utc,
)
from reminders.service import (
    ALLOWED_MINUTES,
    Clock,
    InvalidSnoozeDuration,
    ReminderCompleted,
    ReminderNotFound,
)


class InvalidReminderBatch(ValueError):
    pass


def validate_batch(reminder_ids, minutes):
    if (
        type(minutes) is not int
        or minutes not in ALLOWED_MINUTES
    ):
        raise InvalidSnoozeDuration(minutes)
    if not isinstance(reminder_ids, list):
        raise InvalidReminderBatch()
    if not 1 <= len(reminder_ids) <= 20:
        raise InvalidReminderBatch()
    if any(
        not isinstance(rid, str) or not rid.strip()
        for rid in reminder_ids
    ):
        raise InvalidReminderBatch()
    if len(set(reminder_ids)) != len(reminder_ids):
        raise InvalidReminderBatch()


class BatchRepository(Protocol):
    def get_for_user(
        self, reminder_id: str, user_id: str,
    ) -> Reminder | None: ...

    def save_many(
        self, reminders: list[Reminder],
    ) -> list[Reminder]: ...


class BatchSnoozeService:
    def __init__(
        self, repository: BatchRepository, clock: Clock,
    ) -> None:
        self._repository = repository
        self._clock = clock

    def execute(
        self, user_id: str, reminder_ids: list[str],
        minutes: int,
    ) -> list[Reminder]:
        validate_batch(reminder_ids, minutes)
        selected = []
        for reminder_id in reminder_ids:
            reminder = self._repository.get_for_user(
                reminder_id, user_id,
            )
            if reminder is None:
                raise ReminderNotFound(reminder_id)
            if reminder.status is ReminderStatus.COMPLETED:
                raise ReminderCompleted(reminder_id)
            selected.append(reminder)
        now = normalize_utc(self._clock.now())
        until = now + timedelta(minutes=minutes)
        updated = [
            replace(reminder, snoozed_until=until)
            for reminder in selected
        ]
        return self._repository.save_many(updated)
