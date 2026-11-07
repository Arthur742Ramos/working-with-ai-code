# Current printed-example supplements

These additions accompany the current chapter packages. Captured sessions
retain their original wording and evidence; this map identifies the current
printed examples where a teaching surface changed.

| Chapter | Current printed surface | Runnable source and check |
|---|---|---|
| 3 | Initial baseline; Listings 3.4–3.8 plus the outside-window and UTC-overflow tests | `ch03/test_baseline.py` preserves the initial happy path; `ch03/event_processor.py` and `ch03/test_event_processor.py` check the final package, including both UTC normalization limits. |
| 4 | Listing 4.6 dry-run discriminator and optional endpoint probe | `ch04/test_skeleton.py` checks the assembled pre-replay Listings 4.2–4.5. `ch04/teaching/idempotency_probe.py` compares replay and conflicting-payload behavior on local HTTP fixtures. The original capture stays unchanged. |
| 5 | Listings 5.2, 5.3 and the separate logging follow-up in 5.6 | `teaching/ch05/timestamp_parser.py` and `teaching/ch05/test_order_assertions.py` supply the parser and intentionally failing weak-assertion example. `ch05/corrections/missing_product_logging/request-logging.diff` and `ch05/tests/test_request_logging.py` preserve the logging correction and its four-check result separately from the captured policy repair. |
| 6 | Four printed validator tests and maintained runner in Listing 6.3 | Listings 6.1 and 6.2 give three green/one red before the integer policy repair and four green after. `ch06/validate_config.py` is the maintained runner; `ch06/test_cli.py` checks validation and loading-error outputs. Existing packaged JSON fixtures remain the broader nested example; `ch06/cli.py` stays unchanged for capture replay. |
| 7 | Listing 7.2 and optional worker orchestration | `ch07/demo_agent.py` and `ch07/contract.txt` use a scripted model. `ch07/teaching/orchestrate_adapters.py` validates worker JSON, generates temporary adapters, and checks local and shared behavior before retrying a rejected worker. Offline responses are scripted; live mode can call a configured endpoint. The captured float patch is Listing 7.3. |
| 8 | Draft, conserving intermediate, repaired allocation | `ch08/teaching/draft_allocation.py`, `ch08/test_allocation.py`, `ch08/test_golden.py`, and `ch08/captures/lost_cent_allocation/run_capture.py`. |
| 9 | Source-selection trace in section 9.3 | `ch09/teaching/retrieval_demo.py` runs the trace as an optional supplement, using the same records, dates and query. Two required sources give recall 1.0; one gives 0.5 and fails the evidence check. `ch09/retrieval.py` and the sealed package parity record retain the earlier store/model extension. |
| 10 | Listings 10.4–10.10 | `ch10/teaching/row_probe.py` (10.4, SQLite row probe); `ch10/batch_case/probe_atomicity.py` (10.5, second-write failure trigger); `ch10/batch_case/reminders/repository.py` (10.6, transaction); `ch10/batch_case/reminders/batch_service.py` (10.7–10.8, validation and service); `ch10/batch_case/reminders/batch_handler.py` (10.9, request boundary); `ch10/manual_check.py` (10.10, response and storage). |
| 11 | Complete standalone policy probe in Listing 11.1 | `ch11/teaching/policy_probe.py` includes the setup, policy branch, and printed result. Accepted 1 and rejected 2/Boolean are checked. `ch11/teaching/README.md` describes the current probe; the sealed top-level ledger retains the branch-only capture-era presentation. |
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
