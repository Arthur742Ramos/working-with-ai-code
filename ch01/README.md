# Chapter 1 final support package

This internal package keeps the accepted rate-limiting implementation, its focused and broader checks, and the verified fallback-observability capture together.

## Files

- `app.py` is the complete green book-state implementation. It retains the per-user, ten-per-minute bounded fallback and routes Flask-Limiter's existing fallback warning through the application logger.
- `tests/focused_test.py` exercises a genuine Redis connection failure and checks the application-visible warning plus neighboring per-user limits.
- `tests/broader_test.py` protects the healthy storage path and checks that it emits no fallback warning.
- `captures/fallback_observability/` preserves the immutable red before-state, accepted one-line patch, raw evidence, session record, and replay runner.

## Run the green checks

From the package root, create an isolated environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Then run both maintained top-level checks explicitly:

```bash
.venv/bin/python tests/focused_test.py
.venv/bin/python tests/broader_test.py
```

Each script defaults to this package's green `app.py`. Use these explicit commands instead of broad test discovery, which could collect the intentionally red fixtures under `captures/` as if they were top-level checks.

## Replay the captured repair

```bash
.venv/bin/python captures/fallback_observability/run_capture.py
```

Replay rebuilds disposable red and repaired states, compares them with the stored evidence, verifies the exact patch and package-local checksums, and removes its working directory. Default replay does not rewrite evidence or replace the top-level green implementation. It reads no repository-root, canonical-code, staged-chapter, or other-chapter file.

## Remaining limitations

- The checks cover one process. They do not prove that Redis counters are shared across application instances.
- The outage check uses a closed local port rather than stopping a live Redis deployment.
- The checks do not cover recovery after Redis returns or delivery to a monitoring or paging backend.
- The package pins Flask-Limiter 4.1.1 because the warning assertion depends on that release's message and transition behavior. Any dependency upgrade requires a fresh replay and review.
- The package retains the existing bounded fail-open policy. It does not decide production alert, recovery, or escalation thresholds.
