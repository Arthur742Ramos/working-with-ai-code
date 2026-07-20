"""Listing 4.2: Walking skeleton for a dry-run-capable importer

From "Working with AI as a Real Teammate" (Manning)
Chapter 4

Excerpt: `Sender`, `parse_customer`, and `send_with_retry` are defined
elsewhere in the importer; this listing shows the dry-run-capable runner.
"""

from collections.abc import Iterable


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
