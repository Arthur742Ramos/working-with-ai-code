# Parity map: fallback observability session

| Printed or captured item | Maintained source | Status |
|---|---|---|
| Printed filename | `app.py` | Same reader-facing filename in every state |
| Listing 1.1 state | `before/app.py` | Intentional before-state excerpt; the fallback hook exists but is not called and the logger assignment is absent |
| Top-level runnable state | Package-root `app.py` | Includes the accepted logger assignment and removes the now-unused historical fallback hook as a separate no-behavior cleanup |
| Listing 1.1 omitted scaffolding | `before/app.py` | Imports, Flask initialization, authentication stand-ins, `save_upload()`, runtime comments, and the `__main__` launcher are omitted because they do not change the shown rate-limiting seam |
| Listing 1.1 omitted helper docstring | `on_limiter_fallback()` in `before/app.py` | The helper docstring is omitted with the other non-executable scaffolding; selected executable behavior remains unchanged |
| Listing 1.1 warning wrap | `on_limiter_fallback()` in `before/app.py` | The one-line `app.logger.warning(...)` call is wrapped across three print lines; tokens and behavior are unchanged |
| Listing 1.1 storage wrap | `storage_uri` in `before/app.py` | The one-line `os.environ.get("REDIS_URL", "memory://")` expression is wrapped across four print lines; tokens and behavior are unchanged |
| Limiter key | `user_key()` in both capture states and package `app.py` | Unchanged |
| Limit policy | `@limiter.limit("10 per minute")` | Unchanged |
| Redis storage | `storage_uri` in all app states | Unchanged apart from print-only wrapping |
| Bounded fail-open policy | `in_memory_fallback_enabled=True` | Unchanged |
| Application-visible signal | Flask-Limiter's existing fallback warning via `limiter.logger = app.logger` | Present only in `after/app.py` and package-root `app.py`; the assignment changes logger visibility, not Flask-Limiter's ownership of the healthy-to-fallback transition |
| Top-level focused command | `python tests/focused_test.py` | Defaults to package-root green `app.py` |
| Top-level broader command | `python tests/broader_test.py` | Defaults to package-root green `app.py` |
| Capture focused command | `python tests/focused_test.py .work/app.py` | Replayed from disposable capture state |
| Focused test name | `test_redis_outage_routes_fallback_warning_to_app_logger` | Maintained in capture `tests/focused_test.py` |
| Red output | `evidence/focused-red.txt` | Genuine, exit `1` |
| Exact diff | `patches/production.diff` | One-line machine diff from normalized package before and after fixtures |
| Printed diff | Listing 1.3 | File headers and unchanged context are intentionally omitted; the added `limiter.logger = app.logger` line is exact |
| Patch application | `evidence/patch-apply.txt` | Genuine, exit `0` |
| Focused green | `evidence/focused-green.txt` | Genuine, exit `0` |
| Capture broader command | `python tests/broader_test.py .work/app.py` | Replayed from patched disposable state |
| Broader test name | `test_healthy_storage_emits_no_fallback_warning` | Maintained in capture `tests/broader_test.py` |
| Broader green | `evidence/broader-green.txt` | Genuine, exit `0` |
| Original agent actions | `session.md`, Agent action record | Subclass chronology retained and marked rejected by the historical repair review |
| Historical repair verdict | `session.md`, Independent repair plan | One-line logger assignment accepted as the strict smaller patch; retained as historical session chronology |
| Final independent certification | `evidence/independent-review.md` | Separate final-package review completed with verdict Pass after clean replay, minimality, provenance, isolation, printed-parity, and policy-boundary checks |
| Final-polish terminology | Capture `README.md` and this parity map | Current wording is application-visible fallback observability; the protected receipt's application-owned phrase remains unchanged as historical wording |
| Human policy boundary | `session.md`, Approval basis and Author inspection; `evidence/independent-review.md`, Policy boundary | Bounded fail-open approved; monitoring backend, multi-process validation, and escalation remain human-owned |
| Replay behavior | `run_capture.py` | Default compares only; `--record` writes command evidence; all executable inputs are package-local |
| Review gate | `run_capture.py`, `metadata.json`, and `evidence/independent-review.md` | `complete_independently_reviewed` is rejected unless active review status is `completed`, verdict is `Pass`, and the final review artifact exists with its recorded checksum |
| Origin provenance | `metadata.json`, `repository_commit_before` and `canonical_checksums_*` | Retained as historical capture facts; replay does not resolve or hash those repository paths |
| Package normalization | `metadata.json`, `package_normalization` | Obsolete section and turn-by-turn comments were replaced, and the active manifests pin Flask-Limiter 4.1.1; executable behavior is unchanged and original fixture hashes remain recorded as provenance |

The focused and broader outputs are retained verbatim. No timing or color normalization is applied. Successful worker runs intentionally expose only stable harness output; dependency stderr is reported only when a worker fails.

Commands in the chapter replace the internal disposable `.work/app.py` path with the reader-facing `app.py`. Internal capture paths and replay instructions do not belong in chapter prose. Run the two package-root test scripts explicitly; do not use broad discovery that could treat capture fixtures as top-level tests.
