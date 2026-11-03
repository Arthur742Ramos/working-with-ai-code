# Chapter 9 current printed retrieval example

`retrieval_demo.py` contains the exact Python code from Listings 9.4 and 9.5 of the current Chapter 9, joined by one blank line. It uses only the Python standard library. It ranks three in-memory records by lexical overlap, retains source labels, assembles a prompt, and checks required-source recall. It does not call a model, an external store, or a network service.

From `ch09`, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 teaching/retrieval_demo.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  -p no:cacheprovider teaching/test_retrieval_demo.py
```

The example prints the two required source identifiers and `required-source recall@2: 1.0`. The four separate teaching tests check exact listing bytes, successful execution, stable tie order and prompt labels, and the intended negative control. That control changes only the selection argument from `k=2` to `k=1` in a temporary copy. It must exit with `AssertionError` after reporting recall 0.5. Its fixed `recall@2` display label remains unchanged because the control edits only `k`; this is not a new historical capture.

## Current reader versus historical capture

Use [the current reader map](parity.md) for the printed retrieval listings. The parent `ch09/parity.md` and `ch09/README.md` are checksum-locked records of the earlier staged package; their external-store/model description is not a map of the current printed Listings 9.4–9.5. The maintained `retrieval.py` module remains an extended example, not the printed file.

No file under `captures/`, no capture metadata, no historical package checksum, and no historical review receipt is changed. The original top-level discovery configuration still runs its 28-test suite. The four teaching tests run separately through the explicit command above and the CI workflow. A current teaching test result does not extend the scope or date of the historical capture review.
