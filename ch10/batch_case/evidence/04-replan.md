# Replan after the observed partial commit

The baseline passed 49 tests. The fixed legacy probe exited 1: rem-1 had
a committed timestamp and rem-2 remained NULL. The inner save context
committed the first update; the outer context could not undo that commit.

Reject composing save() calls for the all-or-nothing claim. Keep save()
for single-item clients. Extract its update statement into a non-committing
helper and add save_many(), which owns one connection transaction around
all updates. Reject an already active or autocommit connection before writes.

Add a batch service: validate shape and duration before dependencies, read
and validate all selected reminders, read the clock once, prepare every
update, then call save_many() exactly once. Add a batch handler: validate
body keys and pass trusted identity; translate contract errors consistently.
Storage exceptions propagate. Keep the earlier single-item interfaces intact.

Evidence required: the unchanged trigger/observer oracle passes with the
batch route; a handler-to-file-backed-SQLite failure rolls back both writes;
a successful handler response matches both committed rows; rejection never
writes or reads the clock; an unmatched later update rolls back an earlier
update; existing single-item tests still pass. A second connection must see
the committed state, not just values cached by the writer.
