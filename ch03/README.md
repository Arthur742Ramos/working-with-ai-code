# Chapter 3 support package

This internal package keeps the full event-processor review example, the two
rate-limiter branch artifacts, executable versions of the printed focused and
broader commands, and one verified missing-events capture together.

The event-processor review is a reconstruction from the pre-reduction
manuscript and preserved source artifacts. The two rate-limiter branches are
illustrative synthesis. The nested capture proves one repair inside the
reconstructed review: a missing top-level `events` key becomes a stable
`ValueError` without conflating it with an explicit empty list.

## Files

- `event_processor.py` is the green final implementation.
- `event_processor_initial.py` is the intentionally flawed starting module.
- `event_processor_ship_blockers.py` preserves Listing 3.6's intermediate
  after-state, including the previously accepted missing-events guard.
- `rate_limit_decorator.py` and `rate_limit_redis.py` are the compile-only
  Branch A and Branch B artifacts from the checkpoint-and-branch example.
- `focused_test.py` runs the focused checks against a named module.
- `full_capture_check.py` runs the broader three-case check against a named module.
- `test_event_processor.py` is the complete maintained top-level suite.
- `pytest.ini` keeps top-level pytest discovery out of `captures/`.
- `captures/event_processor_missing_events/` preserves the immutable red before-state, exact patch, raw evidence, and replay runner.

## Run the printed command shapes

Run from this directory:

```bash
python3 focused_test.py event_processor.py
python3 full_capture_check.py event_processor.py
```

Both commands target the final green implementation in this package. The focused command checks the exact missing-key error and the final zero-average behavior for an explicit empty batch. The broader command adds one representative non-empty input and verifies its written summary.

The captured transcript predates later final-state repairs. Its explicit-empty case intentionally reaches the then-unrepaired arithmetic defect. Use capture replay, not the final-state wrappers, to reproduce that historical red and narrow green evidence.

## Verify the final implementation

Run from this directory:

```bash
python3 -m pytest -qq -p no:cacheprovider
```

`pytest.ini` limits discovery to `test_event_processor.py` and excludes
`captures/`. The expected result is eight passing tests: six behavior tests
plus one executable-command test for each wrapper.

The authoring regression suite additionally checks printed intermediate and
final listing parity, guard retention, empty and non-empty behavior, offset
normalization, deduplication, and handle contexts. Run it from the book root:

```bash
python3 -m unittest discover -s code/tools \
    -p test_chapter_editorial_regressions.py -v
```

That authoring check does not alter the historical eight-test capture suite.

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

Replay rebuilds the disposable red and repaired states, compares them with the stored evidence, verifies the exact patch, runs the package-local top-level suite, and removes its working directory. Default replay does not rewrite evidence.

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
