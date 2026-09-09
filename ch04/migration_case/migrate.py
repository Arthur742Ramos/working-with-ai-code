"""Package-local implementation of the staged SQLite migration case.

This implementation is reconstructed from the accepted contract and printed
dry-run evidence. It is runnable support, not a retained historical capture.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sqlite3

from migration_case.seed import DB_PATH

ACCOUNT_TYPES = {
    "1": "individual",
    "2": "business",
}


@dataclass(frozen=True)
class AuditRecord:
    account_id: int
    field_name: str
    old_value: str
    new_value: str


@dataclass(frozen=True)
class MigrationReport:
    rows_read: int
    rows_upserted: int
    rows_skipped: int
    audit_records: tuple[AuditRecord, ...]
    committed: bool

    @property
    def audit_rows(self) -> int:
        return len(self.audit_records)


def normalize_row(row: sqlite3.Row) -> tuple[tuple[object, ...], tuple[AuditRecord, ...]]:
    account_id = row["id"]
    name = (row["name"] or "").strip()
    email = (row["email"] or "").strip().lower()
    created = (row["created"] or "").strip()
    source_type = (row["type"] or "").strip()

    if not name or not email or not created:
        raise ValueError("name, email, and created are required")
    if "@" not in email:
        raise ValueError("email must contain @")
    if source_type not in ACCOUNT_TYPES:
        raise ValueError("unknown account type")

    created_at = datetime.strptime(
        created,
        "%m/%d/%Y",
    ).isoformat()
    account_type = ACCOUNT_TYPES[source_type]
    account = (
        account_id,
        name,
        email,
        created_at,
        account_type,
    )
    audits = (
        AuditRecord(account_id, "email", row["email"], email),
        AuditRecord(account_id, "created", created, created_at),
        AuditRecord(
            account_id,
            "account type",
            source_type,
            account_type,
        ),
    )
    return account, audits


def run_migration(
    connection: sqlite3.Connection,
    *,
    dry_run: bool,
) -> MigrationReport:
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        "SELECT id, name, email, created, type "
        "FROM legacy_users ORDER BY id"
    ).fetchall()
    upserted = 0
    skipped = 0
    audit_records: list[AuditRecord] = []

    connection.execute("BEGIN")
    try:
        for row in rows:
            try:
                account, audits = normalize_row(row)
            except (TypeError, ValueError):
                skipped += 1
                continue

            connection.execute(
                "INSERT INTO accounts "
                "(id, full_name, email, created_at, account_type) "
                "VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET "
                "full_name = excluded.full_name, "
                "email = excluded.email, "
                "created_at = excluded.created_at, "
                "account_type = excluded.account_type",
                account,
            )
            connection.execute(
                "DELETE FROM account_migration_audit "
                "WHERE account_id = ?",
                (row["id"],),
            )
            connection.executemany(
                "INSERT INTO account_migration_audit "
                "(account_id, field_name, old_value, new_value) "
                "VALUES (?, ?, ?, ?)",
                [
                    (
                        audit.account_id,
                        audit.field_name,
                        audit.old_value,
                        audit.new_value,
                    )
                    for audit in audits
                ],
            )
            upserted += 1
            audit_records.extend(audits)

        report = MigrationReport(
            rows_read=len(rows),
            rows_upserted=upserted,
            rows_skipped=skipped,
            audit_records=tuple(audit_records),
            committed=not dry_run,
        )
        if dry_run:
            connection.rollback()
        else:
            connection.commit()
        return report
    except Exception:
        connection.rollback()
        raise


def format_report(report: MigrationReport) -> str:
    outcome = (
        "Migration committed."
        if report.committed
        else "Dry run rolled back."
    )
    lines = [
        outcome,
        "",
        f"- {report.rows_read} legacy rows read",
        f"- {report.rows_upserted} rows upserted",
        f"- {report.rows_skipped} rows skipped",
        f"- {report.audit_rows} audit rows produced",
        f"- committed: {report.committed}",
    ]

    if report.audit_records:
        lines.extend(["", "Sample audit evidence:"])
        labels = {
            "email": "email",
            "created": "created",
            "account type": "account type",
        }
        for audit in report.audit_records[:3]:
            label = labels[audit.field_name]
            lines.append(
                f"- {label}: {audit.old_value} to "
                f"{audit.new_value}"
            )

    lines.extend(
        [
            "",
            "Decisions for approval: the source date has no timezone, so",
            "the proposed value is naive midnight. Validation failures are",
            "skipped and reported; unexpected errors roll back the run.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=DB_PATH)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with sqlite3.connect(args.database) as connection:
        report = run_migration(
            connection,
            dry_run=args.dry_run,
        )
    print(format_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
