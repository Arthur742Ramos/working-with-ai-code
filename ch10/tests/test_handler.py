from datetime import datetime, timezone

import pytest

from reminders.domain import Reminder, ReminderStatus
from reminders.handler import Request, handle_snooze
from reminders.service import (
    InvalidSnoozeDuration,
    ReminderCompleted,
    ReminderNotFound,
)


class StubService:
    def __init__(
        self,
        result: Reminder | None = None,
        error: Exception | None = None,
    ) -> None:
        self.result = result
        self.error = error
        self.calls: list[tuple[str, str, int]] = []

    def execute(
        self,
        user_id: str,
        reminder_id: str,
        minutes: int,
    ) -> Reminder:
        self.calls.append((user_id, reminder_id, minutes))
        if self.error is not None:
            raise self.error
        if self.result is None:
            raise AssertionError(
                "stub result was not configured"
            )
        return self.result


def snoozed_reminder(
    user_id: str = "user-7",
) -> Reminder:
    return Reminder(
        id="rem-1",
        user_id=user_id,
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


@pytest.mark.parametrize("user_id", ["user-7", "user-8"])
def test_success_uses_trusted_request_identity(
    user_id: str,
) -> None:
    service = StubService(
        result=snoozed_reminder(user_id)
    )
    request = Request(
        user_id=user_id,
        reminder_id="rem-1",
        body={"minutes": 15},
    )

    response = handle_snooze(request, service)

    assert response.status == 200
    assert response.body == {
        "id": "rem-1",
        "snoozed_until": (
            "2030-01-02T12:15:00+00:00"
        ),
    }
    assert service.calls == [(user_id, "rem-1", 15)]


@pytest.mark.parametrize(
    "body",
    [
        None,
        [],
        {},
        {"minutes": 15, "user_id": "user-8"},
        {"minutes": True},
        {"minutes": 15.0},
        {"minutes": "15"},
    ],
)
def test_invalid_body_does_not_call_service(
    body: object,
) -> None:
    service = StubService(result=snoozed_reminder())
    request = Request("user-7", "rem-1", body)

    response = handle_snooze(request, service)

    assert response.status == 422
    assert response.body == {
        "error": "invalid_snooze_duration"
    }
    assert service.calls == []


def test_unsupported_integer_maps_to_422() -> None:
    service = StubService(
        error=InvalidSnoozeDuration(10)
    )
    request = Request(
        "user-7",
        "rem-1",
        {"minutes": 10},
    )

    response = handle_snooze(request, service)

    assert response.status == 422


@pytest.mark.parametrize(
    ("error", "status", "body"),
    [
        (
            ReminderNotFound("rem-1"),
            404,
            {"error": "not_found"},
        ),
        (
            ReminderCompleted("rem-1"),
            409,
            {"error": "reminder_completed"},
        ),
    ],
)
def test_domain_error_maps_to_response(
    error: Exception,
    status: int,
    body: dict[str, str],
) -> None:
    service = StubService(error=error)
    request = Request(
        "user-7",
        "rem-1",
        {"minutes": 15},
    )

    response = handle_snooze(request, service)

    assert response.status == status
    assert response.body == body
