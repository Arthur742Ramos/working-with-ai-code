# Appendix A: parser trial

`parser.py` and `test_parser.py` reproduce the two printed Python listings.
The starting parser deliberately accepts negative counts, so running
`python3 -m unittest -v test_parser` from this directory reports four tests
with one expected failure (`ValueError not raised`). This is an intentionally
red fixture, not a test to include in a green chapter suite.

From the companion repository root, run:

```sh
python3 appA/verify_trial.py
```

The verifier copies the listings into a temporary directory, checks that only
the negative-count test fails, then applies a reference repair to the temporary
parser. It reruns the same four tests unchanged and checks another negative
input. The checked-in starting fixture remains red. No book checkout, network
connection, model provider, or third-party Python package is needed.
