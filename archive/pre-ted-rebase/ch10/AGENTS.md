# Chapter 10 working rules

- Use CPython 3.11 or newer.
- Keep production code under `reminders/` on the Python standard library.
- Keep transport validation in `handler.py`.
- Keep snooze policy and clock access in `service.py`.
- Keep SQL, row conversion, and transactions in `repository.py`.
- Read authenticated identity from request context, never from the body.
- Preserve `due_at`; write snooze state to `snoozed_until`.
- Scope repository reads and writes by reminder ID and user ID.
- Run the focused test for the current slice before the full suite.
- Do not add a server, scheduler, authentication system, migration framework,
  network call, AI provider dependency, or production concurrency policy.
- Do not commit, push, open a pull request, merge, or change an external system
  without separate approval.
