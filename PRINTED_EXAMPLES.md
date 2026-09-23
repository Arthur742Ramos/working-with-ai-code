# Current printed-example supplements

These additions accompany the September 2026 Ted-baseline revision. The captured sessions and their checksum-certified package records retain their earlier wording and evidence. This map supersedes earlier listing maps where the revised chapter changed a teaching surface.

| Chapter | Current printed surface | Runnable source and check |
|---|---|---|
| 3 | Initial baseline; Listings 3.7–3.11 plus the outside-window test | `ch03/test_baseline.py` preserves the initial happy path. The assembled printed final module and all six printed tests run in the book authoring regression. |
| 4 | Listing 4.6 dry-run discriminator | `ch04/test_skeleton.py`; checked against the assembled pre-replay Listings 4.2–4.5. The original package test count is unchanged. |
| 5 | Listings 5.2 and 5.3 | `teaching/ch05/timestamp_parser.py` and `teaching/ch05/test_order_assertions.py`. The latter intentionally reports one failure and one pass. These files sit outside the sealed incident-package inventory. |
| 6 | Four printed tests and minimal CLI input | Assembled from Listings 6.1, 6.2 and 6.5; three green/one red before the integer policy repair, four green after; valid and invalid CLI outputs checked. Existing packaged JSON fixtures remain the broader nested example. |
| 7 | New Listing 7.2 | `ch07/demo_agent.py` and `ch07/contract.txt`; the model adapter is scripted. Success, denied tool, and exhausted budget are tested. The unchanged captured float patch is now Listing 7.3. |
| 8 | Draft, conserving intermediate, repaired allocation | `ch08/teaching/`, final allocation package, and `tools/test_ch08_printed_examples.py`. |
| 9 | Complete Listings 9.4 and 9.5 | `ch09/teaching/retrieval_demo.py`; two sources give recall 1.0, one source fails the evidence requirement. `ch09/retrieval.py` and the sealed package parity record retain the earlier store/model interface as a tested extension, not the current print listing. |
| 10 | New Listing 10.4 | `ch10/teaching/row_probe.py`; reproduces SQLite Row keyed access and the missing `.get` method. The captured broader output is now Listing 10.5. |
| 11 | Listing 11.1 with its explicit setup | `ch11/teaching/policy_probe.py`; accepted 1 and rejected 2/Boolean checked. The sealed README describes the earlier complete capture package. |
| Appendix A | Complete parser and test listings | `appA/parser.py` and `appA/test_parser.py` are the printed starting fixture. `appA/verify_trial.py` checks its expected one-test failure and four unchanged tests passing after a temporary reference repair. |

Run each chapter's maintained commands from its README. For the additional standalone examples:

```sh
(cd ch04 && python3 -m pytest -q test_skeleton.py)
(cd ch07 && python3 demo_agent.py)
python3 ch09/teaching/retrieval_demo.py
python3 ch10/teaching/row_probe.py
python3 ch11/teaching/policy_probe.py
python3 appA/verify_trial.py
```

The Chapter 5 hollow-assertion example intentionally fails one test:

```sh
python3 -m pytest -q teaching/ch05/test_order_assertions.py
```

Expected: one failed and one passed test. The failure demonstrates the behavior that the weak assertions accepted. The book's separate authoring checks assemble and execute its printed listings, including the initial and final Chapter 3 suites and the Chapter 6 integer-policy transition. No live model or external service is needed by these supplements.

The Appendix A starting fixture also fails intentionally: direct
`python3 -m unittest -v test_parser` from `appA/` reports one failure in four
tests. Use its verifier above as the green check; it never modifies the printed
fixture.
