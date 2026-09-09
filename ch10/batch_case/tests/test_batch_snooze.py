import sqlite3
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from reminders.batch_handler import (
    BatchRequest, handle_batch_snooze,
)
from reminders.batch_service import (
    BatchSnoozeService, InvalidReminderBatch,
)
from reminders.domain import Reminder, ReminderStatus
from reminders.repository import (
    ReminderWriteError, SQLiteReminderRepository,
)
from reminders.service import InvalidSnoozeDuration
from probe_atomicity import observe, seed

NOW = datetime(2030, 1, 2, 12, tzinfo=timezone.utc)


class CountingClock:
    def __init__(self, value=NOW):
        self.value = value
        self.calls = 0

    def now(self):
        self.calls += 1
        return self.value


@pytest.fixture
def storage(tmp_path):
    path = tmp_path / "batch.sqlite"
    writer = sqlite3.connect(path)
    observer = sqlite3.connect(path)
    seed(writer)
    repository = SQLiteReminderRepository(writer)
    try:
        yield writer, observer, repository
    finally:
        observer.close()
        writer.close()


def request(ids=None, minutes=15):
    return BatchRequest("user-7", {
        "reminder_ids": ["rem-1", "rem-2"] if ids is None else ids,
        "minutes": minutes,
    })


def test_handler_failure_rolls_back_both_rows(storage):
    writer, observer, repository = storage
    before = observe(observer)
    clock = CountingClock()
    service = BatchSnoozeService(repository, clock)
    with pytest.raises(
        sqlite3.IntegrityError, match="injected write failure",
    ):
        handle_batch_snooze(request(), service)
    assert observe(observer) == before
    assert not writer.in_transaction
    assert clock.calls == 1


@pytest.mark.parametrize("minutes", [5, 15, 30, 60])
def test_success_matches_committed_state(storage, minutes):
    writer, observer, repository = storage
    writer.execute("DROP TRIGGER fail_second")
    with writer:
        writer.execute(
            "UPDATE reminders SET snoozed_until = ?",
            ((NOW + timedelta(hours=2)).isoformat(),),
        )
        writer.execute(
            "INSERT INTO reminders SELECT 'sentinel', "
            "'other-user', due_at, status, snoozed_until "
            "FROM reminders WHERE id = 'rem-1'"
        )
    prior_due = observer.execute(
        "SELECT id, due_at FROM reminders ORDER BY id"
    ).fetchall()
    sentinel = observe(observer)[2]
    clock = CountingClock(NOW.astimezone(
        timezone(timedelta(hours=5, minutes=30)),
    ))
    response = handle_batch_snooze(
        request(["rem-2", "rem-1"], minutes),
        BatchSnoozeService(repository, clock),
    )
    until = (NOW + timedelta(minutes=minutes)).isoformat()
    assert response.status == 200
    assert response.body == {
        "ids": ["rem-2", "rem-1"], "snoozed_until": until,
    }
    assert observe(observer) == [
        ("rem-1", until), ("rem-2", until), sentinel,
    ]
    assert observer.execute(
        "SELECT id, due_at FROM reminders ORDER BY id"
    ).fetchall() == prior_due
    assert clock.calls == 1


class NoDependencies:
    def __getattr__(self, name):
        raise AssertionError(f"unexpected dependency: {name}")


@pytest.mark.parametrize("body", [
    None, [], {}, {"minutes": 15},
    {"reminder_ids": ["rem-1"]},
    {"reminder_ids": ["rem-1"], "minutes": 15,
     "user_id": "other-user"},
    {"reminder_ids": [], "minutes": 15},
    {"reminder_ids": "rem-1", "minutes": 15},
    {"reminder_ids": ["rem-1", "rem-1"], "minutes": 15},
    {"reminder_ids": [""], "minutes": 15},
    {"reminder_ids": ["  "], "minutes": 15},
    {"reminder_ids": [None], "minutes": 15},
    {"reminder_ids": [["rem-1"]], "minutes": 15},
    {"reminder_ids": [str(n) for n in range(21)], "minutes": 15},
    *[{"reminder_ids": ["rem-1"], "minutes": value}
      for value in [True, 15.0, "15", 0, 16, None]],
])
def test_bad_input_never_reaches_dependencies(body):
    service = BatchSnoozeService(
        NoDependencies(), NoDependencies(),
    )
    response = handle_batch_snooze(
        BatchRequest("user-7", body), service,
    )
    assert response.status == 422


@pytest.mark.parametrize("ids,minutes,error", [
    ([], 15, InvalidReminderBatch),
    (["rem-1"], True, InvalidSnoozeDuration),
])
def test_direct_service_validates(ids, minutes, error):
    service = BatchSnoozeService(
        NoDependencies(), NoDependencies(),
    )
    with pytest.raises(error):
        service.execute("user-7", ids, minutes)


@pytest.mark.parametrize("change,status", [
    ("DELETE FROM reminders WHERE id = 'rem-2'", 404),
    ("UPDATE reminders SET user_id = 'other-user' "
     "WHERE id = 'rem-2'", 404),
    ("UPDATE reminders SET status = 'completed' "
     "WHERE id = 'rem-2'", 409),
])
def test_later_rejection_never_changes_first(storage, change, status):
    writer, observer, repository = storage
    writer.execute("DROP TRIGGER fail_second")
    with writer:
        writer.execute(change)
    before = observe(observer)
    clock = CountingClock()
    response = handle_batch_snooze(
        request(), BatchSnoozeService(repository, clock),
    )
    assert response.status == status
    assert observe(observer) == before
    assert clock.calls == 0


def test_wrong_owner_write_rolls_back_earlier_update(storage):
    writer, observer, repository = storage
    writer.execute("DROP TRIGGER fail_second")
    before = observe(observer)
    first = repository.get_for_user("rem-1", "user-7")
    second = repository.get_for_user("rem-2", "user-7")
    with pytest.raises(ReminderWriteError):
        repository.save_many([
            replace(first, snoozed_until=NOW),
            replace(second, user_id="wrong", snoozed_until=NOW),
        ])
    assert observe(observer) == before


def test_caller_transaction_is_preserved(storage):
    writer, observer, repository = storage
    writer.execute("DROP TRIGGER fail_second")
    writer.execute(
        "UPDATE reminders SET snoozed_until = 'caller-work' "
        "WHERE id = 'rem-1'"
    )
    with pytest.raises(ReminderWriteError, match="idle"):
        repository.save_many([])
    assert writer.in_transaction
    assert observe(observer) == [("rem-1", None), ("rem-2", None)]
    writer.rollback()


def test_autocommit_is_rejected(storage):
    writer, observer, repository = storage
    writer.isolation_level = None
    with pytest.raises(ReminderWriteError, match="idle"):
        repository.save_many([])
    assert observe(observer) == [("rem-1", None), ("rem-2", None)]


def test_naive_clock_fails_before_write(storage):
    _, observer, repository = storage
    before = observe(observer)
    clock = CountingClock(NOW.replace(tzinfo=None))
    with pytest.raises(ValueError, match="timezone-aware"):
        handle_batch_snooze(
            request(), BatchSnoozeService(repository, clock),
        )
    assert observe(observer) == before


@pytest.mark.parametrize("count", [1, 20])
def test_valid_size_boundaries_read_clock_and_save_once(count):
    class RecordingRepository:
        def __init__(self):
            self.reads = []
            self.batches = []

        def get_for_user(self, reminder_id, user_id):
            self.reads.append((reminder_id, user_id))
            return Reminder(
                reminder_id, user_id, NOW,
                ReminderStatus.PENDING,
            )

        def save_many(self, reminders):
            self.batches.append(reminders)
            return reminders

    repository = RecordingRepository()
    clock = CountingClock()
    ids = [f"rem-{n}" for n in range(count)]
    response = handle_batch_snooze(
        request(ids), BatchSnoozeService(repository, clock),
    )
    assert response.status == 200
    assert repository.reads == [(rid, "user-7") for rid in ids]
    assert len(repository.batches) == 1
    assert clock.calls == 1
    assert len({r.snoozed_until for r in repository.batches[0]}) == 1
