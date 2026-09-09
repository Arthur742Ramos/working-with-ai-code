from collections.abc import Mapping
from dataclasses import dataclass

from reminders.service import (
    InvalidSnoozeDuration,
    ReminderCompleted,
    ReminderNotFound,
    SnoozeService,
)


@dataclass(frozen=True)
class Request:
    user_id: str
    reminder_id: str
    body: object


@dataclass(frozen=True)
class Response:
    status: int
    body: dict[str, str]


def _invalid_duration() -> Response:
    return Response(
        status=422,
        body={"error": "invalid_snooze_duration"},
    )


def handle_snooze(
    request: Request,
    service: SnoozeService,
) -> Response:
    if not isinstance(request.body, Mapping):
        return _invalid_duration()
    if set(request.body) != {"minutes"}:
        return _invalid_duration()

    minutes = request.body["minutes"]
    if type(minutes) is not int:
        return _invalid_duration()

    try:
        reminder = service.execute(
            user_id=request.user_id,
            reminder_id=request.reminder_id,
            minutes=minutes,
        )
    except InvalidSnoozeDuration:
        return _invalid_duration()
    except ReminderNotFound:
        return Response(404, {"error": "not_found"})
    except ReminderCompleted:
        return Response(
            409,
            {"error": "reminder_completed"},
        )

    if reminder.snoozed_until is None:
        raise RuntimeError(
            "service returned no snooze timestamp"
        )

    return Response(
        status=200,
        body={
            "id": reminder.id,
            "snoozed_until": (
                reminder.snoozed_until.isoformat()
            ),
        },
    )
