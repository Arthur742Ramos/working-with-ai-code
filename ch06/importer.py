"""CSV customer importer (chapter 6 running example).

Built slice by slice in a planner-executor flow: parse one row and
derive a stable idempotency key, build and retry the API request, then
run a dry import that counts outcomes. The sender is injected so retry
behavior is testable without real network calls.
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
import hashlib
import time

REQUIRED = ("source_id", "email", "name")
TRANSIENT = {429, 500, 502, 503, 504}
IDEMPOTENT_REPLAY = {409}


@dataclass(frozen=True)
class CustomerRow:
    source_id: str
    email: str
    name: str
    key: str


@dataclass(frozen=True)
class ApiResult:
    status: int
    body: str


Request = dict[str, object]
Sender = Callable[[Request], ApiResult]


def parse_customer(raw: dict[str, str]) -> CustomerRow:
    cleaned = {
        field: (raw.get(field) or "").strip()
        for field in REQUIRED
    }
    missing = [field for field in REQUIRED if not cleaned[field]]
    if missing:
        raise ValueError(f"missing fields: {missing}")

    digest = hashlib.sha256(
        cleaned["source_id"].encode("utf-8")
    ).hexdigest()

    return CustomerRow(
        source_id=cleaned["source_id"],
        email=cleaned["email"].lower(),
        name=cleaned["name"],
        key=digest[:32],
    )


def build_request(row: CustomerRow) -> Request:
    return {
        "path": "/customers",
        "json": {
            "external_id": row.source_id,
            "email": row.email,
            "name": row.name,
        },
        "headers": {
            "Idempotency-Key": row.key,
        },
    }


def send_with_retry(
    row: CustomerRow,
    sender: Sender,
    attempts: int = 3,
) -> ApiResult:
    request = build_request(row)

    for attempt in range(1, attempts + 1):
        result = sender(request)
        if result.status < 400:
            return result
        if result.status in IDEMPOTENT_REPLAY:
            return result
        if result.status not in TRANSIENT:
            raise RuntimeError(result.body)
        if attempt == attempts:
            raise RuntimeError(result.body)
        time.sleep(2 ** (attempt - 1))

    raise AssertionError("unreachable")


def run_import(
    rows: Iterable[dict[str, str]],
    sender: Sender,
    dry_run: bool = True,
) -> dict[str, int]:
    counts = {
        "validated": 0,
        "sent": 0,
        "invalid": 0,
        "send_failed": 0,
    }

    for raw in rows:
        try:
            row = parse_customer(raw)
        except ValueError:
            counts["invalid"] += 1
            continue

        counts["validated"] += 1
        if dry_run:
            continue
        try:
            send_with_retry(row, sender)
            counts["sent"] += 1
        except RuntimeError:
            counts["send_failed"] += 1

    return counts
