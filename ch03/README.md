# Chapter 3 support package

This internal package contains the full event-processor review example and two
rate-limiter branch artifacts. It also includes executable versions of the
printed focused and broader commands, with one verified missing-events capture.

The event-processor review is a reconstruction from the pre-reduction
manuscript and preserved source artifacts. The two rate-limiter branches are
illustrative synthesis. The nested capture verifies one repair in that review:
a missing top-level `events` key produces a stable `ValueError`, while an
explicit empty list remains an empty batch.

## Files

- `event_processor.py` is the green final implementation.
- `event_processor_initial.py` is the intentionally flawed starting module.
- `event_processor_ship_blockers.py` preserves Listing 3.6's intermediate
  after-state, including the previously accepted missing-events guard.
- `rate_limit_decorator.py` and `rate_limit_redis.py` are the illustrative
  Branch A and Branch B artifacts from the checkpoint-and-branch example.
- `focused_test.py` runs the focused checks against a named module.
- `full_capture_check.py` runs the broader three-case check against a named module.
- `test_event_processor.py` is the complete maintained top-level suite.
- `pytest.ini` keeps top-level pytest discovery out of `captures/`.
- `captures/event_processor_missing_events/` preserves the immutable red before-state, exact patch, raw evidence, and replay runner.

## Set up an isolated test environment

Start in `ch03/`, the directory containing this README. The standalone wrappers
use the standard library. The final suite and the capture runner's final-package
checks require pytest, so install it in a disposable environment before running
the suite or replay:

```bash
python3 -m venv ../.venv-ch03
source ../.venv-ch03/bin/activate
python3 -m pip install pytest
```

In PowerShell, create the environment with `py -m venv ..\.venv-ch03` and install
pytest with `..\.venv-ch03\Scripts\python.exe -m pip install pytest`. Use that
interpreter in place of `python3` below; activation is optional.
For bash commands continued with `\`, put all arguments on one line in PowerShell.

When finished, return to `ch03/`, deactivate the environment if activated,
and remove it with `rm -rf ../.venv-ch03` (bash) or
`Remove-Item -LiteralPath ..\.venv-ch03 -Recurse -Force` (PowerShell). Removing the
environment also removes its optional branch dependencies.

## Run the printed command shapes

Run from this directory:

```bash
python3 focused_test.py event_processor.py
python3 full_capture_check.py event_processor.py
```

Both commands check this package's final green implementation. The focused
command checks the exact missing-key error and the zero average for an explicit
empty batch. The broader command also checks a representative non-empty input
and its written summary.

The captured transcript predates the later final-state repairs. Its
explicit-empty case still reaches the arithmetic defect that was present then.
Capture replay reproduces that historical red and narrow green evidence;
the final-state wrappers check the later repairs.

## Verify the final implementation

Run from this directory:

```bash
python3 -m pytest -qq -p no:cacheprovider
```

`pytest.ini` limits discovery to `test_event_processor.py` and excludes
`captures/`. The expected result is eight passing tests: six behavior tests
plus one executable-command test for each wrapper.

The initial happy-path check is separate from the eight-test final suite. Run
it explicitly from this directory:

```bash
python3 -m pytest -q -p no:cacheprovider test_baseline.py
```

The historical capture suite is unchanged by this separate check.

The branch files are intentionally outside pytest discovery. Compile them with:

```bash
python3 -m py_compile \
    event_processor_initial.py \
    rate_limit_decorator.py \
    rate_limit_redis.py
```

## Replay the captured repair

Run from this directory:

```bash
python3 captures/event_processor_missing_events/run_capture.py
```

Replay rebuilds disposable red and repaired states and compares them with the
stored evidence. It verifies the exact patch and runs the package-local
top-level suite. A `finally` block removes the working directory after success
or failure. Default replay leaves the stored evidence unchanged.

## Dependencies

- Python 3 is available as `python3`.
- `pytest` is installed for the top-level suite and replay.
- `diff` is available for capture patch verification.

No command requires the repository root, canonical chapter code, another chapter, or Box.

## Remaining limitations

- File reads and writes do not select UTF-8 explicitly.
- Output replacement is not atomic.
- Unhashable or mutually unorderable event `type` values can fail during aggregation or sorting.
- The maintained suite does not cover every malformed per-event field, the naive-as-UTC policy, every skipped-event detail, summary logging, or every output failure.
- The capture proves only the bounded missing-versus-empty repair. It does not
  prove the later robustness changes by itself.
- The two branch files are design artifacts, not deployment-ready limiters.
  Branch A is process-local. Branch B needs a unique Redis sorted-set member
  per hit, explicit Redis failure policy, and a running service before use.

## Middleware response regression checks

The Redis branch returns a response directly when it denies a request. In the
original example, raising `HTTPException` from user middleware bypassed the
endpoint exception handler and produced HTTP 500. These checks use a real
FastAPI middleware stack with a fake shared-counter result. They verify 429
without entering the endpoint and 200 with the authenticated identity on an
allowed request. Redis execution, its downtime policy, and concurrent load
remain outside these checks.

```bash
python3 -m pip install -r requirements-branches.txt
python3 -m pytest -q -p no:cacheprovider branch_tests
```

Run these optional checks from `ch03/` in the isolated environment above.
To remove only the packages listed in the branch requirements while keeping
the environment, run `python3 -m pip uninstall -r requirements-branches.txt`.
This also uninstalls pytest; reinstall it before another final suite or replay.
Transitive dependencies remain until removed separately or the environment is
deleted.

The tests remain separate from the retained event-processor capture and its
historical test counts. The distinction between endpoint exceptions and direct
middleware responses follows the [Starlette exception documentation](https://starlette.dev/exceptions/#httpexception).
