# Controlled service-slice capture

The chapter's service implementation scene used a temporary, intentionally red
snapshot. The local capture revisions are provenance identifiers, not public Git
commits. This directory makes the same focused red-to-green path reproducible
from the published companion source.

The patch is generated from the final maintained files. It changes only
`reminders/service.py` and `tests/test_service.py`: the service returns
`NotImplementedError`, and the focused suite contains the 14 cases present at
capture time.

Use a clean clone or disposable branch. From the companion repository root:

```bash
git switch -c ch10-controlled-service

git apply --unidiff-zero \
  ch10/captures/service-slice-before.patch
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

On native Windows PowerShell, use `.venv\Scripts\python` in place of
`.venv/bin/python`. The Git commands are unchanged.
