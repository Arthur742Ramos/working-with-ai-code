from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import pytest

from reminders.domain import Reminder, ReminderStatus
from reminders.service import (
    InvalidSnoozeDuration,
    ReminderCompleted,
    ReminderNotFound,
    SnoozeReminderService,
)


NOW = datetime(2030, 1, 2, 12, tzinfo=timezone.utc)
DUE = datetime(2030, 1, 2, 13, tzinfo=timezone.utc)


@dataclass
class FrozenClock:
    value: datetime
    calls: int = 0

    def now(self) -> datetime:
        self.calls += 1
        return self.value


class FakeRepository:
    def __init__(self, reminders: list[Reminder]) -> None:
        self.reminders = {
            (item.id, item.user_id): item
            for item in reminders
        }
        self.saved: list[Reminder] = []

    def get_for_user(
        self,
        reminder_id: str,
        user_id: str,
    ) -> Reminder | None:
        return self.reminders.get((reminder_id, user_id))

    def save(self, reminder: Reminder) -> Reminder:
        self.saved.append(reminder)
        self.reminders[
            (reminder.id, reminder.user_id)
        ] = reminder
        return reminder


def make_reminder(
    *,
    user_id: str = "user-7",
    status: ReminderStatus = ReminderStatus.PENDING,
    snoozed_until: datetime | None = None,
) -> Reminder:
    return Reminder(
        id="rem-1",
        user_id=user_id,
        due_at=DUE,
        status=status,
        snoozed_until=snoozed_until,
    )


def test_snooze_uses_current_time_and_saves_once() -> None:
    original = make_reminder()
    repository = FakeRepository([original])
    clock = FrozenClock(NOW)
    service = SnoozeReminderService(repository, clock)

    result = service.execute("user-7", "rem-1", 15)

    assert result.due_at == original.due_at
    assert result.snoozed_until == datetime(
        2030, 1, 2, 12, 15, tzinfo=timezone.utc,
    )
    assert repository.saved == [result]
    assert clock.calls == 1


def test_repeat_snooze_replaces_previous_value() -> None:
    original = make_reminder(
        snoozed_until=datetime(
            2030,
            1,
            2,
            15,
            tzinfo=timezone.utc,
        )
    )
    repository = FakeRepository([original])
    clock = FrozenClock(
        datetime(
            2030,
            1,
            2,
            12,
            30,
            tzinfo=timezone.utc,
        )
    )
    service = SnoozeReminderService(repository, clock)

    result = service.execute("user-7", "rem-1", 15)

    assert result.snoozed_until == datetime(
        2030,
        1,
        2,
        12,
        45,
        tzinfo=timezone.utc,
    )


def test_missing_reminder_does_not_save() -> None:
    repository = FakeRepository([])
    service = SnoozeReminderService(
        repository,
        FrozenClock(NOW),
    )

    with pytest.raises(ReminderNotFound):
        service.execute("user-7", "missing", 15)

    assert repository.saved == []


def test_other_users_reminder_looks_missing() -> None:
    repository = FakeRepository(
        [make_reminder(user_id="user-8")]
    )
    service = SnoozeReminderService(
        repository,
        FrozenClock(NOW),
    )

    with pytest.raises(ReminderNotFound):
        service.execute("user-7", "rem-1", 15)

    assert repository.saved == []


def test_completed_reminder_does_not_save() -> None:
    repository = FakeRepository(
        [
            make_reminder(
                status=ReminderStatus.COMPLETED
            )
        ]
    )
    service = SnoozeReminderService(
        repository,
        FrozenClock(NOW),
    )

    with pytest.raises(ReminderCompleted):
        service.execute("user-7", "rem-1", 15)

    assert repository.saved == []


@pytest.mark.parametrize(
    "minutes",
    [True, 15.0, "15", None, 0, 10, 61],
)
def test_invalid_duration_does_not_save(
    minutes: object,
) -> None:
    repository = FakeRepository([make_reminder()])
    service = SnoozeReminderService(
        repository,
        FrozenClock(NOW),
    )

    with pytest.raises(InvalidSnoozeDuration):
        service.execute("user-7", "rem-1", minutes)

    assert repository.saved == []


def test_naive_clock_is_a_programming_error() -> None:
    repository = FakeRepository([make_reminder()])
    service = SnoozeReminderService(
        repository,
        FrozenClock(datetime(2030, 1, 2, 12)),
    )

    with pytest.raises(ValueError, match="timezone-aware"):
        service.execute("user-7", "rem-1", 15)

    assert repository.saved == []


def test_clock_value_is_normalized_to_utc() -> None:
    offset = timezone(timedelta(hours=2))
    repository = FakeRepository([make_reminder()])
    service = SnoozeReminderService(
        repository,
        FrozenClock(
            datetime(2030, 1, 2, 14, tzinfo=offset)
        ),
    )

    result = service.execute("user-7", "rem-1", 15)

    assert result.snoozed_until == datetime(
        2030,
        1,
        2,
        12,
        15,
        tzinfo=timezone.utc,
    )
