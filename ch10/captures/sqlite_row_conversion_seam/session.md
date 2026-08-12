# SQLite row-conversion seam session

This public transcript preserves the bounded adapter repair without depending
on private repository paths or historical workspace metadata.

## Reconstructed contract

Inspect `reminders/repository.py` and the focused SQLite test. Run
`test_get_for_user_maps_unsnoozed_reminder` against the before state before
editing. The adapter must convert a real `sqlite3.Row` for an unsnoozed
reminder without calling an unsupported mapping method. Keep tests and all
other production files unchanged.

## Genuine focused red

```text
$ python3 -m pytest -q --tb=short -p no:cacheprovider \
  tests/test_sqlite_repository.py::test_get_for_user_maps_unsnoozed_reminder
F                                                                        [100%]
E   AttributeError: 'sqlite3.Row' object has no attribute 'get'
1 failed
```

The query returned a real `sqlite3.Row`, but the converter treated it like a
dictionary. The smallest plan was to replace only the unsupported call with
keyed access and rerun the focused and full adapter checks.

## Exact repair

```diff
 snoozed_until=_parse_optional_timestamp(
-    row.get("snoozed_until")
+    row["snoozed_until"]
 ),
```

## Green evidence

```text
$ python3 -m pytest -q --tb=short -p no:cacheprovider \
  tests/test_sqlite_repository.py::test_get_for_user_maps_unsnoozed_reminder
.                                                                        [100%]
1 passed

$ python3 -m pytest -q --tb=short -p no:cacheprovider \
  tests/test_sqlite_repository.py
............                                                             [100%]
12 passed
```

Focused green proves that a present SQL `NULL` maps to Python `None`.
The broader adapter run checks owner scope, identifier scope, timestamp
round-trips, commit visibility, and zero-row failure. It does not define a
future policy for a query that omits the projected column.
