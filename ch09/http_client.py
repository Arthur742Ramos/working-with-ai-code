"""Approved outbound HTTP boundary with auth and bounded transient retries."""

import os
from dataclasses import dataclass
from typing import Callable, Mapping, Optional


@dataclass(frozen=True)
class Response:
    status: int
    body: dict


TRANSIENT_STATUSES = frozenset({429, 502, 503, 504})
Transport = Callable[[str, str, Mapping[str, str], dict], Response]


def _unconfigured_transport(
    method: str,
    url: str,
    headers: Mapping[str, str],
    body: dict,
) -> Response:
    raise RuntimeError(
        "no HTTP transport configured; inject one with set_transport"
    )


_transport: Transport = _unconfigured_transport


def set_transport(transport: Transport) -> None:
    """Set the single transport used by the approved client."""
    global _transport
    _transport = transport


def reset_transport() -> None:
    """Restore the fail-closed transport after an injected test transport."""
    set_transport(_unconfigured_transport)


def call(
    method: str,
    url: str,
    *,
    json: Optional[dict] = None,
    headers: Optional[Mapping[str, str]] = None,
    max_retries: int = 2,
) -> Response:
    """Apply auth and bounded transient retries."""
    if max_retries < 0:
        raise ValueError("max_retries must be non-negative")

    request_headers = dict(headers or {})
    if "Authorization" not in request_headers:
        token = os.environ.get("API_TOKEN")
        if not token:
            raise RuntimeError("API_TOKEN is required for outbound HTTP")
        request_headers["Authorization"] = f"Bearer {token}"

    body = dict(json or {})
    response = _transport(method, url, request_headers, body)
    attempts = 0
    while (
        response.status in TRANSIENT_STATUSES
        and attempts < max_retries
    ):
        attempts += 1
        response = _transport(method, url, request_headers, body)
    return response
