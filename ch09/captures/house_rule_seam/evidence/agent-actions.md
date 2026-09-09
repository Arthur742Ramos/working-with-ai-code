# Observable agent action record

1. Read `AGENTS.md`, the real-session capture standard, and every text artifact in the staged `house_rule_seam` package. The requested `memory/polished-twelve-chapter-outcome.md` path was not present in the repository.
2. Reviewed the existing focused guard, alert behavior tests, three-line production patch, runner, evidence, session record, publication-ready session, parity map, metadata, and session ledger without editing canonical chapter or support files.
3. Identified that the old focused test proved only that `requests` was forbidden. The broader alert test contained the stronger chapter-native behavior: `send_alert` must route the exact method, URL, and JSON payload through the house client.
4. Strengthened `test_send_alert_routes_through_house_client` to intercept the `call` symbol used by `alerts.py`, invoke `send_alert`, and compare the exact `POST`, `ALERTS_URL`, and `{"text": message}` arguments.
5. Ran the new test manually against the before state. Collection first failed because `requests` was not installed, before the routing assertion could run.
6. Added an empty in-memory `requests` module in the package-local test so the immutable before fixture could load without a third-party dependency or network call.
7. Reran the focused test. The before state failed at the intended missing-`call` assertion, and the repaired state passed the exact routing assertions.
8. Replaced pytest's `monkeypatch` fixture with `unittest.mock.patch.object` after review showed the fixture representation leaked a process-specific memory address into red output. Reconfirmed stable focused red and focused green.
9. Kept `patches/house_rule_seam.patch` byte-identical. It remains the readable three-line import, call, and response-field substitution; `before/`, `after/`, and `http_client.py` were not changed.
10. Updated `run_capture.py` to focus on the routing behavior test, lock the strengthened test checksum, and require the missing-seam assertion in red semantics.
11. Updated `README.md`, `session.md`, `chapter-session.md`, and `parity.md` so the focused claim names exact method, URL, and JSON routing while the broader claim retains authentication, status, retry, fail-closed, and import-guard coverage.
12. Updated package checksums and metadata command surfaces so intentional record mode could validate all reviewed inputs before writing evidence.
13. Ran intentional `--record` mode only after reviewing the test's stable red and green behavior. It regenerated raw focused red, focused green, broader green, and canonical support green evidence in disposable space.
14. Inspected the recorded outputs and synchronized the session and publication-ready transcript to the genuine timing and traceback.
15. Updated runner, record, evidence, and test checksums in `metadata.json`, then ran default immutable replay and confirmed it did not rewrite evidence.
16. Verified JSON validity, runner compilation, the unchanged three-line patch, no leftover disposable work directory, canonical chapter and support checksum parity, and repository scope.
17. Updated the Chapter 9 session-ledger row only after record and immutable replay passed.
18. Retained the original broader setup failure as private history. It remains evidence of the earlier omitted guard fixture, not part of the focused routing workflow or publication transcript.

## Certification repair after first independent review

1. Read the complete first-review result and separated the intentionally Pending ledger state from package defects.
2. Replaced the `alerts.call` existence and patch requirement with an observer that patches `http_client.call` before loading the feature.
3. Added a positive module-qualified implementation test and confirmed both approved import shapes route the exact method, URL, and JSON through the shared seam.
4. Preserved the original before and after production fixtures, shared client, and three-line patch byte-for-byte.
5. Ran a no-color red probe before recording and removed a process-specific function address from the traceback path.
6. Added context-managed cleanup that removes disposable work after success or failure and rejects stale `.work-*` directories.
7. Added review-state validation that accepts active Pending re-review without calling it Pass and requires a checked package-local artifact for any completed Pass claim.
8. Mapped the intentional six-line printed red excerpt and current callout titles in `parity.md`, then updated only the current canonical and staged Chapter 9 sources.
9. Ran intentional record mode after the harness changes, synchronized the exact recorded timing and traceback, refreshed dependent checksums, and completed immutable replay with no leftover work directory.
