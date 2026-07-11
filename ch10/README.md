# Chapter 10: Code Listings

This directory contains the runnable reminder-snooze example from Chapter 10,
"Software engineering: from idea to running code."

The project takes one vague ticket through accepted behavior, module boundaries,
focused checks, a controlled SQLite failure, and a review-ready local change.

## Get the code

The first recipe uses macOS, Linux, or Windows Subsystem for Linux (WSL)
with CPython 3.11 or newer:

```bash
git clone \
  https://github.com/Arthur742Ramos/working-with-ai-code.git
cd working-with-ai-code/ch10
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python manual_check.py
```

On native Windows PowerShell, use the Python launcher and the Windows virtual
environment path:

```powershell
git clone https://github.com/Arthur742Ramos/working-with-ai-code.git
cd working-with-ai-code/ch10
py -3 --version
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
.venv\Scripts\python manual_check.py
```

The full suite should report `44 passed`. Production code uses only the Python
standard library. [`requirements.txt`](requirements.txt) declares `pytest` for
the tests.

## Ticket and accepted behavior

> Let users snooze reminders.

The chapter fixes these decisions before implementation:

- The body contains exactly `{"minutes": value}`.
- The allowed exact integer values are 5, 15, 30, and 60.
- Authenticated identity comes from request context.
- Missing and other-user reminders both return `404`.
- Completed reminders return `409` without a write.
- Snooze preserves `due_at` and replaces `snoozed_until`.
- The new timestamp starts from injected current time in Coordinated Universal
  Time (UTC).

The example does not start a server or scheduler. It does not cover
authentication, notification delivery, migration rollout, deployment, or
simultaneous state changes.

## Printed listings

- Listing 10.1: [`reminders/service.py`](reminders/service.py) keeps policy behind
  clock and repository ports.
- Listing 10.2: [`tests/test_service.py`](tests/test_service.py) checks policy with
  a fake repository and frozen clock.
- Listing 10.3:
  [`tests/test_sqlite_repository.py`](tests/test_sqlite_repository.py) crosses
  the real SQLite row boundary.
- Listing 10.4: [`manual_check.py`](manual_check.py) produces the deterministic
  response-and-storage output printed in the chapter.

## Supporting files

- [`AGENTS.md`](AGENTS.md) gives a coding agent the path-scoped operating rules.
- [`PROMPTS.md`](PROMPTS.md) contains the chapter's prompt blocks.
- [`captures/README.md`](captures/README.md) reproduces the controlled service
  red-to-green path from a clean snapshot.
- [`reminders/domain.py`](reminders/domain.py) defines the immutable domain value.
- [`reminders/handler.py`](reminders/handler.py) validates transport data and maps
  domain outcomes.
- [`reminders/repository.py`](reminders/repository.py) owns SQL, row conversion,
  timestamps, and transactions.
- [`tests/test_handler.py`](tests/test_handler.py) checks request and response
  behavior.
- [`tests/test_snooze_flow.py`](tests/test_snooze_flow.py) composes the handler,
  service, and real adapter.
- [`manual_check.py`](manual_check.py) prints deterministic response and stored
  values.

## Local evidence ledger

| Behavior | Check |
|---|---|
| Exact request shape and duration rules | Handler and service tests |
| Owner-scoped lookup and state rules | Service, repository, and full-flow tests |
| Current-time and repeat semantics | Frozen-clock service tests |
| SQLite row and timestamp conversion | Real in-memory SQLite tests |
| Response and storage agree | Deterministic manual run |

Run a focused real-row check with:

```bash
.venv/bin/python -m pytest -q \
  tests/test_sqlite_repository.py::test_get_for_user_maps_unsnoozed_reminder
```

On native Windows PowerShell:

```powershell
& .\.venv\Scripts\python.exe -m pytest -q `
  tests/test_sqlite_repository.py::test_get_for_user_maps_unsnoozed_reminder
```

## Failure provenance

The organic build failure was a false-green ownership test. Its name claimed
that an update was owner-scoped, but both fixtures used the same owner. An
ID-only mutation therefore left 35 tests green. The permanent
`test_save_rejects_another_users_row` crosses the ownership boundary, expects
`ReminderWriteError`, and verifies that storage remains unchanged. That repair
raised the suite from 35 tests to 36. A later read-only pull-request review found
missing discriminators for accepted durations, UTC representation, fresh clock
reads, authenticated identities, and reminder IDs. The current suite has 44
tests.

The `sqlite3.Row.get` failure in the chapter is a controlled reproduction. The
capture temporarily replaces `row["snoozed_until"]` with the plausible but
unsupported `row.get("snoozed_until")`. A real SQLite row raises
`AttributeError`; indexed access is the verified repair. Never leave the
repository in the controlled failing state.

## Hosted evidence limit

A local green run and an inspected diff can make a branch ready to publish for
review. They do not prove that a hosted pull request has passed continuous
integration or human review. The chapter records those delivery states
separately and never calls this example merge-ready without those artifacts.

## Known limit

The teaching example does not solve a simultaneous snooze-versus-complete race.
A production design needs an explicit concurrency policy, such as a version
check or conditional update. That policy is outside this chapter's contract.

[Return to the companion repository index](../README.md).
