# SQLite row-conversion seam

This public fixture preserves the Chapter 10 adapter session in a disposable,
package-local form. The before state calls `sqlite3.Row.get`, the focused test
reaches a real row containing SQL `NULL`, and the stored patch changes only
that expression to keyed access.

## Replay

Run from `ch10/`:

```bash
python3 captures/sqlite_row_conversion_seam/run_capture.py
```

Replay runs the focused red, applies the one-line patch, then runs focused and
12-test broader green and the maintained package suite. Temporary `.work*` directories are removed on success
or failure.

`session.md` and the files under `evidence/` retain the generic command and
output transcript. No private book workspace path or historical identifier is
needed to reproduce the seam.

The captured test is a focused excerpt. Replay stages the maintained
`tests/test_sqlite_repository.py` as the full adapter suite instead of keeping
a second broad suite that could drift. It verifies the specific row-interface
failure and the normalized evidence summaries and exit statuses, rather than
trusting an arbitrary red exit. The patch must make exactly the one-line repair
and recreate the maintained repository and domain sources.

Evidence is a sanitized summary, not a byte-for-byte author log. Timings, private
paths, action logs, and independent-review metadata are intentionally omitted.
