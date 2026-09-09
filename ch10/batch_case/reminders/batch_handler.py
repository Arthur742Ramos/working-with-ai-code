from collections.abc import Mapping
from dataclasses import dataclass

from reminders.batch_service import (
    BatchSnoozeService, InvalidReminderBatch,
)
from reminders.service import (
    InvalidSnoozeDuration,
    ReminderCompleted,
    ReminderNotFound,
)


@dataclass(frozen=True)
class BatchRequest:
    user_id: str
    body: object


@dataclass(frozen=True)
class BatchResponse:
    status: int
    body: dict[str, object]


def handle_batch_snooze(
    request: BatchRequest, service: BatchSnoozeService,
) -> BatchResponse:
    if (
        not isinstance(request.body, Mapping)
        or set(request.body) != {"reminder_ids", "minutes"}
    ):
        return BatchResponse(
            422, {"error": "invalid_batch"},
        )
    try:
        reminders = service.execute(
            request.user_id,
            request.body["reminder_ids"],
            request.body["minutes"],
        )
    except (InvalidReminderBatch, InvalidSnoozeDuration):
        return BatchResponse(
            422, {"error": "invalid_batch"},
        )
    except ReminderNotFound:
        return BatchResponse(404, {"error": "not_found"})
    except ReminderCompleted:
        return BatchResponse(
            409, {"error": "reminder_completed"},
        )
    until = reminders[0].snoozed_until
    if until is None or any(
        reminder.snoozed_until != until
        for reminder in reminders
    ):
        raise RuntimeError("inconsistent batch result")
    return BatchResponse(200, {
        "ids": [reminder.id for reminder in reminders],
        "snoozed_until": until.isoformat(),
    })
