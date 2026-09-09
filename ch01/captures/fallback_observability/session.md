# Session record: fallback observability

## Provenance

This record comes from a real Claude Code session completed on 2026-07-15 against repository commit `38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6`. It is condensed from tool logs. The source inspection, commands, outputs, exit statuses, original plan and action sequence, independent verdict, repair sequence, and accepted exact diff are retained; routine tool framing is omitted.

## Human contract

The earlier red-stage contract was reconstructed from the approved architecture because the original prompt was not retained. The completion direction was retained and is condensed here rather than presented as a quotation:

Inspect the staged fallback-observability package and run genuine red before editing. Keep the approved bounded fail-open overload policy. Choose the best implementation without another approval checkpoint, wire and test one real fallback observability signal, apply the strict smallest production diff only to a disposable or after-state copy, record exact machine evidence, add non-recording replay, and leave canonical Chapter 1 prose and code unchanged. Stop honestly if red, minimality, or reproducible green fails.

## Inspection before editing

The agent read `AGENTS.md`, `session-capture-standard.md`, and every staged package file. `before/app.py` and `before/requirements.txt` were byte-identical to canonical Chapter 1 support at the recorded commit.

The limiter used the current user ID as its key, read Redis from `REDIS_URL`, enabled Flask-Limiter's in-memory fallback, and applied `10 per minute` to `/api/upload`. The module also defined `on_limiter_fallback()`, but no caller referenced it.

The package-local virtual environment was initially absent. The first replay attempt failed before running the test with shell exit `127`. The agent created `.venv`, installed `before/requirements.txt`, and reran the unchanged capture.

## Genuine focused red

Command executed by the runner against the disposable before copy:

```bash
python tests/focused_test.py .work/app.py
```

Exit status: `1`

Raw output:

```text
FAIL: test_redis_outage_routes_fallback_warning_to_app_logger
expected: 1 fallback warning on application logger
observed: 0 fallback warnings on application logger
neighbor retained: user-1 first 10=200, 11th=429; user-2 first=200
```

## Agent observation

The red result isolates logger ownership from fallback policy. A genuine Redis failure still gives the first user ten successful requests followed by `429`, and the second user's first request still succeeds. Flask-Limiter emits its healthy-to-fallback warning through its own logger, so the application logger observes zero copies of that warning.

## Original one-sentence plan

The original agent plan is preserved because it drove the captured actions: add a minimal `Limiter` subclass that observes the existing `_storage_dead` transition around `_check_request_limit()`, calls the existing hook once when the state changes from healthy to fallback, and instantiate that subclass without changing the key, limit, Redis URI, or `in_memory_fallback_enabled=True`.

## Approval basis

The author's retained direction authorized the agent to choose the best bounded implementation without another checkpoint and explicitly fixed the policy as bounded fail-open with one real observability signal. The author did not name a subclass, approve dependence on `_storage_dead`, select a logger assignment, or choose a monitoring backend.

The original agent selected one signal per healthy-to-fallback transition. This was narrower than signaling every affected request, but independent review later showed that Flask-Limiter already supplied the transition frequency and warning. The subclass was therefore not the strict smallest implementation.

## Agent action record

1. Read the governing instructions, capture standard, staged source, test, runner, metadata, evidence, and narrative files.
2. Attempted default replay. The package-local Python executable did not exist, so no test or production edit ran.
3. Created the ignored virtual environment and installed the staged requirements.
4. Replayed the focused test from the immutable before fixture and reproduced the stored red output with exit `1`.
5. Inspected Flask-Limiter 4.1.1's `_check_request_limit()` and storage recovery paths. The library sets `_storage_dead = True` before recursively evaluating the configured fallback and later clears it only after a successful backend health check.
6. Copied `before/app.py` to `after/app.py` and made only the originally planned subclass plus constructor-name change.
7. Generated a unified diff with `diff -u`. The first shell wrapper used zsh's read-only variable name `status` and exited after the diff command; the agent reran the same machine diff with a different variable name and verified the stored patch.
8. Ran focused green, broader green, and Python compilation against the after copy. All exited `0`.
9. Applied the stored patch to a fresh disposable copy with `patch -p1`, compared it byte-for-byte with `after/app.py`, and removed the disposable copy.
10. Replaced the red-only runner with full record and non-recording replay behavior, then recorded red, patch application, focused green, and broader green raw evidence with exit statuses.
11. Completed package metadata, parity, and evidence-boundary records, then ran default replay to verify that no evidence was rewritten.
12. Independent review replayed the package, challenged minimality, and rejected the subclass because `limiter.logger = app.logger` routes Flask-Limiter's existing healthy-to-fallback warning to the application-owned logger in one line.
13. The repair regenerated `after/app.py` from immutable `before/app.py`, added only the logger assignment, and machine-generated a new patch.
14. The focused contract was narrowed to the exact Flask-Limiter 4.1.1 warning on `app.logger`; the broader contract was updated to require no such warning on healthy storage.
15. The runner recorded fresh red, patch, focused green, and broader green evidence, then the package records were synchronized to the accepted implementation.

## Independent repair plan

Replace the rejected subclass with `limiter.logger = app.logger`, assert Flask-Limiter's existing healthy-to-fallback warning on the application logger, and leave every limiter policy setting unchanged.

## Exact accepted diff

```diff
--- a/app.py
+++ b/app.py
@@ -101,6 +101,7 @@
     # unreachable (overload protection, not a security gate).
     in_memory_fallback_enabled=True,
 )
+limiter.logger = app.logger
 
 
 @app.route("/api/upload", methods=["POST"])
```

The block above preserves the original machine-generated accepted diff. For the final support package, obsolete section and turn-by-turn comments were replaced identically in both fixtures. `patches/production.diff` was then regenerated from those normalized copies and retains the same one-line production change:

```diff
--- a/app.py
+++ b/app.py
@@ -78,6 +78,7 @@
     # Keep uploads bounded if shared storage is unavailable.
     in_memory_fallback_enabled=True,
 )
+limiter.logger = app.logger
 
 
 @app.route("/api/upload", methods=["POST"])
```

The accepted production change is one added line. It changes logger ownership only: the key function, route limit, Redis URI, and `in_memory_fallback_enabled=True` remain byte-identical. The independent verdict established that the rejected subclass was not minimal; the one-line assignment uses Flask-Limiter's existing warning and transition behavior instead of duplicating them. Metadata retains both original and normalized fixture and patch hashes so packaging cleanup is not presented as part of the captured production edit.

## Genuine focused green

Command:

```bash
python tests/focused_test.py .work/app.py
```

Exit status: `0`

Raw output:

```text
PASS: test_redis_outage_routes_fallback_warning_to_app_logger
observed: 1 fallback warning on application logger
neighbor retained: user-1 first 10=200, 11th=429; user-2 first=200
```

## Genuine broader green

Command:

```bash
python tests/broader_test.py .work/app.py
```

Exit status: `0`

Raw output:

```text
PASS: test_healthy_storage_emits_no_fallback_warning
observed: 0 fallback warnings on application logger
neighbor retained: user-1 first 10=200, 11th=429; user-2 first=200
```

## Evidence boundary

The focused run proves that the staged after state routes Flask-Limiter 4.1.1's existing warning through the application logger once on a genuine Redis connection failure while retaining the existing per-user fallback bound. The broader run proves that the healthy storage path emits no matching warning on the application logger and retains the same neighboring limit behavior.

The checks do not prove delivery to a real metrics or paging backend, multi-process Redis behavior, recovery after Redis returns, compatibility with a future Flask-Limiter warning contract, or the operational correctness of one warning per transition.

## Author inspection and human-owned decision

The author fixed the product policy for this slice: keep bounded fail-open overload protection and add one real fallback observability signal. Independent review selected the strict smaller implementation for that policy. The remaining human-owned choices are the production monitoring backend and the alert, recovery, and escalation thresholds.

Canonical `chapters/ch01.md` and canonical `code/ch01/rate_limiting/` files remained unchanged.
