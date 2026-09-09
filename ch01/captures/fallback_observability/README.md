# Fallback observability capture

This internal package records one real Chapter 1 coding-agent session. When Redis is unavailable and Flask-Limiter enters its configured in-memory fallback, its existing transition warning reaches the application logger without changing the `10 per minute` per-user limit policy.

The behavior belongs in Chapter 1 because the rate-limiting exchange is the chapter's canonical 3C Loop example. Flask-Limiter already emitted the required healthy-to-fallback warning, but it emitted through its own logger instead of the application's logger.

The historical repair review rejected the original subclass patch because a one-line logger assignment satisfies the same contract. After that repair and isolated recheck, a separate independent canonical review replayed the final package and certified it Pass. The attributable record is `evidence/independent-review.md`.

The final-polish terminology supersedes one phrase in that historical receipt without rewriting it. The current term is *application-visible fallback observability*: Flask-Limiter owns storage-transition detection and the warning's frequency, while `limiter.logger = app.logger` makes that library-owned record visible through the application logger. People still own the monitoring backend and alert, recovery, and escalation policy. The historical fixtures retain the helper so the captured one-line patch stays exact; the package root removes that obsolete helper as a later no-behavior cleanup. Separately, dependency hardening pins Flask-Limiter 4.1.1 in the active manifests. Neither cleanup changes runtime behavior, commands, outputs, the production patch, or historical receipts.

## Record and replay

Run these commands from this capture directory.

Create an ignored environment and install the packaged runtime dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r before/requirements.txt
```

Intentionally recreate the verified evidence:

```bash
.venv/bin/python run_capture.py --record
```

Replay without rewriting evidence:

```bash
.venv/bin/python run_capture.py
```

The runner verifies package-local input checksums, copies `before/` into disposable `.work/`, reproduces red, applies `patches/production.diff`, compares the patched file with the frozen `after/app.py`, verifies the separately cleaned package-root `app.py`, runs focused and broader green, compares raw output and exit statuses with `evidence/`, and removes `.work/` on success or failure. Default replay performs no persistent package or evidence writes.

## Dependencies and assumptions

The capture installs Flask-Limiter 4.1.1 from `before/requirements.txt` alongside Flask, redis-py, and Flask-Login. It also requires the standard `diff` and `patch` command-line tools.

No live Redis process is required. The focused test uses closed local TCP port `127.0.0.1:1` to produce a genuine Redis connection failure. The broader check uses Flask-Limiter's `memory://` storage to protect the healthy path.

The implementation routes Flask-Limiter 4.1.1's existing `Rate limit storage unreachable - falling back to in-memory storage` warning through `app.logger`. A future Flask-Limiter upgrade must rerun this package because the warning text and transition semantics may change.

## Human-owned policy boundary

The author explicitly retained bounded fail-open overload protection and requested one real fallback observability signal. The author did not name a subclass, logger assignment, monitoring backend, or alert frequency. The original agent selected a private-state subclass, but independent review found the smaller `limiter.logger = app.logger` implementation. Flask-Limiter already emits one warning when storage changes from healthy to fallback, so routing that warning satisfies the focused contract without emitting one warning per affected request.

A human still owns whether the application warning connects to a counter, alert, or page, plus recovery and escalation thresholds.

## What the checks prove

The focused check proves that a genuine Redis connection failure:

- routes exactly one existing Flask-Limiter fallback warning through the application logger;
- preserves ten successful requests followed by `429` for one user; and
- preserves an independent first successful request for a second user.

The broader check proves that the healthy in-memory storage path preserves the same per-user bound and emits no fallback warning on the application logger.

## What the checks do not prove

The checks do not prove that a real metrics backend receives an event, an operator receives a page, Redis-backed counters are shared across processes, fallback recovery works after Redis returns, Flask-Limiter's warning contract remains stable across upgrades, or one warning per transition is the right operations policy.

## Isolation and origin provenance

Replay reads only this capture directory plus the package-root `app.py` and `requirements.txt`. It has no repository-root, staged-chapter, canonical-code, or other-chapter dependency.

`metadata.json` retains the original repository commit and canonical hashes as historical provenance. It also records the original fixture hashes separately from the normalized final-package hashes. The final package replaced obsolete section and turn-by-turn comments, then pinned Flask-Limiter to the independently reviewed 4.1.1 runtime. The dependency pin narrows replay resolution; runtime behavior, stable evidence output, and the accepted one-line production change remain unchanged.

## Independent certification

Active package state is `complete_independently_reviewed`, review status is `completed`, and the final verdict is `Pass`. Default replay rejects that completed stage if the active review status or review artifact is missing, pending, or checksum-invalid.
