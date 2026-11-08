# Appendix A: comparison trials

`parser.py` and `test_parser.py` reproduce the first printed trial. The
starting parser deliberately accepts negative counts, so running
`python3 -m unittest -v test_parser` from this directory reports four tests
with one expected failure (`ValueError not raised`).

`access_trial/` reproduces the printed store, service, and tests for a
cross-module owner check. From that directory, run
`python3 -m unittest -v test_access`: three tests pass and the cross-owner
case fails. Both trials are intentionally red starting fixtures.

From the companion repository root, run:

```sh
python3 appA/verify_trial.py
python3 appA/verify_access_trial.py
```

Each verifier copies its fixture into a temporary directory, checks the
expected failure, applies a reference repair, and runs the unchanged tests.
It also checks another input. The starting files remain red. The trials use
only Python's standard library; no model provider, network access, or book
checkout is needed. The access fixture assumes a trusted actor ID and does
not implement authentication, a database, or concurrent access.
