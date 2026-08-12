# SQLite row-conversion capture parity

| Session surface | Public companion source |
|---|---|
| Before adapter | `before/reminders/repository.py` |
| Real-row fixture | `before/reminders/domain.py`, `tests/conftest.py` |
| Focused discriminator | `tests/test_sqlite_repository.py::test_get_for_user_maps_unsnoozed_reminder` |
| Exact repair | `patches/sqlite_row_conversion.diff` |
| Command/output transcript | `session.md`, `evidence/` |
| Replay and cleanup | `run_capture.py` |

The capture is intentionally package-local and sanitized. It does not include
book workspace paths, historical repository identifiers, or private review
metadata.
