# Chapter 9 retrieval supplement

`retrieval_demo.py` runs the source-selection trace in section 9.3. The chapter presents the records, query and recall results; this optional supplement supplies the full implementation. It uses only the Python standard library. It ranks three in-memory records by lexical overlap, retains source labels, assembles a prompt, and checks required-source recall. It does not call a model, an external store, or a network service.

From `ch09`, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 teaching/retrieval_demo.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  -p no:cacheprovider teaching/test_retrieval_demo.py
```

The example prints the two required source identifiers and `required-source recall@2: 1.0`. The four separate teaching tests check the retained implementation bytes, successful execution, stable tie order and prompt labels, and the intended negative control. That control changes only the selection argument from `k=2` to `k=1` in a temporary copy. It must exit with `AssertionError` after reporting recall 0.5. Its fixed `recall@2` display label remains unchanged because the control edits only `k`; this is not a new historical capture.

## Current reader versus historical capture

Use [the current reader map](parity.md) for section 9.3. The parent `ch09/parity.md` retains the earlier staged package's listing labels and store/model example. Replay uses the archived README from `corrections/guard_description/historical/README.md`; the maintained parent README describes the current package. `retrieval.py` remains an extended example.

No file under `captures/`, no capture metadata, no historical package checksum, and no historical review receipt is changed. The original top-level discovery configuration still runs its 28-test suite. The four teaching tests run separately through the explicit command above and the CI workflow. A current teaching test result does not extend the scope or date of the historical capture review.
