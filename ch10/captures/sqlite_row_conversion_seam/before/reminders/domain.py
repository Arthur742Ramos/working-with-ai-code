from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class ReminderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


def normalize_utc(value: datetime) -> datetime:
    if value.utcoffset() is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True)
class Reminder:
    id: str
    user_id: str
    due_at: datetime
    status: ReminderStatus
    snoozed_until: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ReminderStatus):
            raise TypeError("status must be ReminderStatus")

        object.__setattr__(
            self,
            "due_at",
            normalize_utc(self.due_at),
        )
        if self.snoozed_until is not None:
            object.__setattr__(
                self,
                "snoozed_until",
                normalize_utc(self.snoozed_until),
            )
