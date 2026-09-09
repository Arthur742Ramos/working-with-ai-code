# Chapter 8 final support package

This internal package keeps the promoted exact-rational allocator, its publication tests, and the verified exact-tie capture together. It runs without the repository root, staged chapters, canonical support files, or another chapter package.

## Files

- `allocation.py` is the green publication-state implementation. It converts stated numeric weights to exact rational values before largest-remainder ranking.
- `test_allocation.py` contains eight canonical-equivalent behavior checks plus the promoted exact-tie regression.
- `test_golden.py` contributes the ninth canonical-equivalent check by running the six trusted allocation rows.
- `pytest.ini` excludes capture internals from top-level discovery.
- `captures/lost_cent_allocation/` preserves the binary-float red before-state, exact patch, raw evidence, and package-local replay runner.

## Verify the final implementation

Run from this directory:

```bash
python3 -m pytest -q -p no:cacheprovider
```

The expected result is ten passing tests: nine canonical-equivalent checks plus the promoted exact-tie test. Pytest does not collect the copied capture tests during this run.

## Replay the captured repair

Run from this directory:

```bash
python3 captures/lost_cent_allocation/run_capture.py
```

Replay copies the float before-state into disposable space, reproduces the required focused red, applies the exact patch, reproduces focused and broader green, then runs all ten final-package tests against the promoted implementation. It verifies only files inside this package and removes temporary work on success or failure.

The canonical capture is independently reviewed with package verdict `Pass`. The review reproduced the red, exact patch, focused and broader green, and ten-test final package from clean canonical and mirror copies. Replay checksum-verifies the fixed package-local receipt, requires its exact attribution and completed `Pass` state, and locks all six certification files against mutation during execution. During that read-only review, the shared publication ledger was `Pending`; aggregate reconciliation later moved Chapter 8 to `Pass`. The historical receipt preserves the earlier state. Replay neither reads the ledger nor uses its workflow state as the package verdict.

The original nine-test maintained-baseline output remains under `evidence/canonical_support_green.txt` as origin provenance. Replay checksum-verifies that artifact but does not execute or locate the old repository-root files. The separately labeled `evidence/final_package_green.txt` records the package-local ten-test run.

## Verify isolation

A copied package supports the same commands:

```bash
cp -R . /tmp/ch08-final
cd /tmp/ch08-final
python3 -m pytest -q -p no:cacheprovider
python3 captures/lost_cent_allocation/run_capture.py
```

No command needs the source repository after the copy finishes.

## Remaining limitations

- Accepted weights are ordinary finite integers and floats; other numeric classes and non-finite values are not specified.
- Decimal-string rationalization is an explicit representation policy, not a universal rule for every numeric interface.
- Stable input order is the selected tie rule; domain owners must decide whether it is fair for their product.
- The tests do not cover every weight distribution, extreme magnitude, or performance boundary.
- The capture proves the bounded exact-tie repair. It does not establish the remaining policy choices.
