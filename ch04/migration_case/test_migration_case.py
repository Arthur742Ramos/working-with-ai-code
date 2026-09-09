"""Tests for the package-local migration reconstruction."""

import hashlib
from pathlib import Path
import sqlite3

import pytest

from migration_case.migrate import (
    format_report,
    run_migration,
)
from migration_case.seed import build

HERE = Path(__file__).resolve().parent
EVIDENCE_PATH = HERE / "evidence" / "dry-run.txt"
EVIDENCE_SHA256 = (
    "a54895f15f960161be8eb8e82733fc3d"
    "edfb3aa5ae9fad31c6f63a2f68af3a58"
)


def seeded_connection(tmp_path: Path) -> sqlite3.Connection:
    path = build(tmp_path / "shop.db", announce=False)
    return sqlite3.connect(path)


def test_dry_run_matches_printed_evidence_and_rolls_back(tmp_path):
    with seeded_connection(tmp_path) as connection:
        report = run_migration(connection, dry_run=True)
        accounts = connection.execute(
            "SELECT COUNT(*) FROM accounts"
        ).fetchone()[0]
        audits = connection.execute(
            "SELECT COUNT(*) FROM account_migration_audit"
        ).fetchone()[0]

    assert (report.rows_read, report.rows_upserted) == (3, 3)
    assert (report.rows_skipped, report.audit_rows) == (0, 9)
    output = format_report(report)
    evidence = EVIDENCE_PATH.read_text()
    checksum = hashlib.sha256(evidence.encode()).hexdigest()

    assert report.committed is False
    assert (accounts, audits) == (0, 0)
    assert "`" not in output
    assert output == evidence
    assert checksum == EVIDENCE_SHA256


def test_apply_commits_normalized_rows_and_audits(tmp_path):
    with seeded_connection(tmp_path) as connection:
        report = run_migration(connection, dry_run=False)
        jane = connection.execute(
            "SELECT full_name, email, created_at, account_type "
            "FROM accounts WHERE id = 1"
        ).fetchone()
        audit_count = connection.execute(
            "SELECT COUNT(*) FROM account_migration_audit"
        ).fetchone()[0]

    assert report.committed is True
    assert tuple(jane) == (
        "Jane Doe",
        "jane@example.com",
        "2024-03-15T00:00:00",
        "individual",
    )
    assert audit_count == 9


def test_apply_is_idempotent_on_rerun(tmp_path):
    with seeded_connection(tmp_path) as connection:
        first = run_migration(connection, dry_run=False)
        second = run_migration(connection, dry_run=False)
        account_count = connection.execute(
            "SELECT COUNT(*) FROM accounts"
        ).fetchone()[0]
        audit_count = connection.execute(
            "SELECT COUNT(*) FROM account_migration_audit"
        ).fetchone()[0]

    assert first.rows_upserted == second.rows_upserted == 3
    assert (account_count, audit_count) == (3, 9)


def test_invalid_rows_are_skipped_and_reported(tmp_path):
    with seeded_connection(tmp_path) as connection:
        connection.execute(
            "INSERT INTO legacy_users "
            "(id, name, email, created, type) "
            "VALUES (?, ?, ?, ?, ?)",
            (4, "Bad Date", "bad@example.com", "tomorrow", "1"),
        )
        connection.commit()
        report = run_migration(connection, dry_run=True)

    assert report.rows_read == 4
    assert report.rows_upserted == 3
    assert report.rows_skipped == 1


def test_unexpected_error_rolls_back_the_transaction(tmp_path):
    with seeded_connection(tmp_path) as connection:
        connection.execute("DROP TABLE account_migration_audit")
        connection.commit()
        with pytest.raises(sqlite3.OperationalError):
            run_migration(connection, dry_run=False)
        account_count = connection.execute(
            "SELECT COUNT(*) FROM accounts"
        ).fetchone()[0]

    assert account_count == 0
