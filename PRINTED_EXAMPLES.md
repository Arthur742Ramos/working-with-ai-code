# Current printed-example supplements

These additions accompany the current chapter packages. Captured sessions
retain their original wording and evidence; this map identifies the current
printed examples where a teaching surface changed.

| Chapter | Current printed surface | Runnable source and check |
|---|---|---|
| 3 | Initial baseline; Listings 3.4–3.8 plus the outside-window test | `ch03/test_baseline.py` preserves the initial happy path; `ch03/event_processor.py` and `ch03/test_event_processor.py` check the final package. |
| 4 | Listing 4.6 dry-run discriminator and optional endpoint probe | `ch04/test_skeleton.py` checks the assembled pre-replay Listings 4.2–4.5. `ch04/teaching/idempotency_probe.py` compares replay and conflicting-payload behavior on local HTTP fixtures. The original capture stays unchanged. |
| 5 | Listings 5.2 and 5.3 | `teaching/ch05/timestamp_parser.py` and `teaching/ch05/test_order_assertions.py`. The latter intentionally reports one failure and one pass. These files sit outside the sealed incident-package inventory. |
| 6 | Four printed tests and minimal CLI input | Assembled from Listings 6.1, 6.2 and 6.3; three green/one red before the integer policy repair, four green after; valid and invalid CLI outputs checked. Existing packaged JSON fixtures remain the broader nested example. |
| 7 | Listing 7.2 and optional worker orchestration | `ch07/demo_agent.py` and `ch07/contract.txt` use a scripted model. `ch07/teaching/orchestrate_adapters.py` runs separate worker requests with a scripted offline mode or an optional live model endpoint. The captured float patch is Listing 7.3. |
| 8 | Draft, conserving intermediate, repaired allocation | `ch08/teaching/draft_allocation.py`, `ch08/test_allocation.py`, `ch08/test_golden.py`, and `ch08/captures/lost_cent_allocation/run_capture.py`. |
| 9 | Source-selection trace in section 9.3 | `ch09/teaching/retrieval_demo.py` runs the trace as an optional supplement, using the same records, dates and query. Two required sources give recall 1.0; one gives 0.5 and fails the evidence check. `ch09/retrieval.py` and the sealed package parity record retain the earlier store/model extension. |
| 10 | Listings 10.4–10.10 | `ch10/teaching/row_probe.py` (10.4, SQLite row probe); `ch10/batch_case/probe_atomicity.py` (10.5, second-write failure trigger); `ch10/batch_case/reminders/repository.py` (10.6, transaction); `ch10/batch_case/reminders/batch_service.py` (10.7–10.8, validation and service); `ch10/batch_case/reminders/batch_handler.py` (10.9, request boundary); `ch10/manual_check.py` (10.10, response and storage). |
| 11 | Listing 11.1 with its explicit setup | `ch11/teaching/policy_probe.py`; accepted 1 and rejected 2/Boolean checked. The sealed README describes the earlier complete capture package. |
| Appendix A | Complete parser and test listings | `appA/parser.py` and `appA/test_parser.py` are the printed starting fixture. `appA/verify_trial.py` checks its expected one-test failure and four unchanged tests passing after a temporary reference repair. |

Run each chapter's maintained commands from its README. For the additional standalone examples:

```sh
(cd ch04 && python3 -m pytest -q test_skeleton.py)
(cd ch04 && python3 teaching/idempotency_probe.py)
(cd ch07 && python3 demo_agent.py)
(cd ch07 && python3 teaching/orchestrate_adapters.py --demo)
python3 ch09/teaching/retrieval_demo.py
python3 ch10/teaching/row_probe.py
python3 ch11/teaching/policy_probe.py
python3 appA/verify_trial.py
```

The Chapter 5 hollow-assertion example intentionally fails one test:

```sh
python3 -m pytest -q teaching/ch05/test_order_assertions.py
```

Expected: one failed and one passed test. The failure demonstrates the behavior
that the weak assertions accepted. The commands above need no live model or
external service.

The Appendix A starting fixture also fails intentionally: direct
`python3 -m unittest -v test_parser` from `appA/` reports one failure in four
tests. Use its verifier above as the green check; it never modifies the printed
fixture.
