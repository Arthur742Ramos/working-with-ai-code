# Controlled red-to-green captures

The current row-conversion session is preserved under
[`sqlite_row_conversion_seam/`](sqlite_row_conversion_seam/). Its public
replay uses a real `sqlite3.Row`, the maintained adapter test file, a stored
one-line patch, and a sanitized command/output transcript. Run it from `ch10/`
with:

```bash
python3 captures/sqlite_row_conversion_seam/run_capture.py
```

The older service and SQLite patch walkthroughs below remain useful as
standalone exercises. The package-local fixture is the current Chapter 10
session surface.

## Service implementation slice

The chapter's service implementation scene used a temporary, intentionally red
snapshot. The local capture revisions are provenance identifiers, not public Git
commits. This directory makes the same focused red-to-green path reproducible
from the published companion source.

The patch is generated from the final maintained files. It changes only
`reminders/service.py` and `tests/test_service.py`. The pre-state retains the
later `SnoozeService` protocol, so restoring the final service remains the
captured 28-insertion, 3-deletion repair. The service returns
`NotImplementedError`, and the focused suite contains the 14 cases present at
capture time.

Use a clean clone or disposable branch. From the companion repository root:

```bash
git switch -c ch10-controlled-service

git apply --unidiff-zero ch10/captures/service-slice-before.patch
cd ch10
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q tests/test_service.py
```

Expected red summary:

```text
14 failed
```

Restore only the final service implementation while leaving the captured tests
in place, then rerun:

```bash
git restore reminders/service.py
.venv/bin/python -m pytest -q tests/test_service.py
```

Expected green summary:

```text
14 passed
```

Finally restore the captured test file and confirm the public snapshot remains
clean:

```bash
git restore tests/test_service.py
git status --short
```

On native Windows PowerShell, use the Windows launcher and virtual-environment
path:

```powershell
git switch -c ch10-controlled-service
git apply --unidiff-zero ch10/captures/service-slice-before.patch
cd ch10
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q tests/test_service.py
git restore reminders/service.py
.venv\Scripts\python -m pytest -q tests/test_service.py
git restore tests/test_service.py
git status --short
```

## SQLite row repair

The SQLite capture starts from the corrected maintained adapter and changes one
line back to the plausible but unsupported `sqlite3.Row.get` call. The existing
real-row test then reproduces the captured failure.

Use another clean clone or disposable branch. From the companion repository
root on macOS, Linux, or Windows Subsystem for Linux:

```bash
git switch -c ch10-controlled-sqlite-row
git apply --unidiff-zero ch10/captures/sqlite-row-before.patch
cd ch10
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
target="tests/test_sqlite_repository.py::"\
"test_get_for_user_maps_unsnoozed_reminder"
.venv/bin/python -m pytest -q -p no:cacheprovider "$target"
git restore reminders/repository.py
.venv/bin/python -m pytest -q -p no:cacheprovider "$target"
git status --short
```

The red run should report `1 failed` with `AttributeError`. The run after the
one-line restore should report `1 passed`.

On native Windows PowerShell:

```powershell
git switch -c ch10-controlled-sqlite-row
git apply --unidiff-zero ch10/captures/sqlite-row-before.patch
cd ch10
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
$target = (
  "tests/test_sqlite_repository.py::" +
  "test_get_for_user_maps_unsnoozed_reminder"
)
.venv\Scripts\python -m pytest -q -p no:cacheprovider $target
git restore reminders/repository.py
.venv\Scripts\python -m pytest -q -p no:cacheprovider $target
git status --short
```
