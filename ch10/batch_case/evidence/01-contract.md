# Batch snooze experiment: contract and first route

Recorded by Codex on 2026-09-08 before the probe and feature edits.
The author authorized the agent to drive a larger captured case. These
are agent-selected teaching rules, not a transcript of product approval.
The existing single-reminder implementation is copied unchanged here.
The original chapter case and its historical capture remain separate.

Accept a body containing exactly reminder_ids and minutes. reminder_ids
is a list of 1 through 20 distinct, nonempty strings; whitespace-only
identifiers are invalid. minutes is an exact int in {5,15,30,60}.
Reject malformed input with 422 before reads or clock access. Identity
comes from trusted request context. Read and validate every selected
reminder before preparing updates. Missing or other-owner rows yield 404;
completed rows yield 409; for mixed semantic failures the first in request
order wins. Neither rejection writes or reads the clock. A valid batch
reads an aware clock once, resets every snooze to that instant plus the
duration, preserves due_at, and returns IDs in request order with one
shared timestamp. Every update commits, or none does. Storage errors
propagate after rollback. Existing single-reminder behavior is preserved.

Out of scope: HTTP server/authentication, notifications, deployment, and
concurrent complete-versus-snooze policy. The adapter owns an idle SQLite
connection with normal transaction mode; reject batch calls inside an
existing transaction or with isolation_level=None. This makes transaction
ownership explicit instead of accidentally committing caller work.

First route to test: reuse the single-save API inside an outer connection
context. Inspection shows save() itself uses a connection context. Before
choosing this route, test whether those contexts nest atomically. Inject a
SQLite trigger that aborts the second update; observe committed data from
a second connection. The oracle requires both original values unchanged.
This is an intentional fault experiment, not a discovered live incident.

Run the 49 existing behavior checks first, then the fixed probe. If the
probe shows a partial commit, stop the composition route and move the
transaction into a batch adapter operation. Keep the fault and observer
assertions fixed; do not weaken the oracle to make the new route pass.
