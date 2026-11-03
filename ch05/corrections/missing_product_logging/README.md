# Follow-on correction: preserve the orphan diagnostic

Recorded 2026-11-03 against repository base
`66e73763491b875ab2a4ec22cb8cdd406b4b866a`.

## Defect and bounded change

The historical `MissingProductError` handler returned 422 without logging.
Because the service disables the default HTTP request logger, the captured
repair hid the data-integrity incident from the service's own logs. Its focused
and broader tests passed because they checked exception/response behavior, not
the diagnostic. The historical minimality decision removed instrumentation;
the later review found that omission was not safe.

`request-logging.diff` adds one ERROR log before the existing 422 response,
including the order identifier, status, elapsed milliseconds and exception
message containing the missing product code. The response body and status stay
unchanged. The generic 500 branch still retains its full traceback. There is no
new logger, exception type, response contract, cache policy or database repair.

## Evidence and scope

`tests/test_request_logging.py` uses a disposable SQLite fixture and the real
summary/handler/log functions. Only the unexpected-error control injects an
exception. A deterministic clock makes the request log assertion exact; both
the file and stderr sinks are checked for the orphan and unexpected error.
Neighboring checks protect 200/cache and missing-order 404 logging.

The following raw command outputs and exit statuses were recorded separately:

| Target source | Command from the Chapter 5 directory | Evidence | Result |
|---|---|---|---|
| Historical after-state reconstructed from the original patch | `python3 tests/test_request_logging.py HISTORICAL_DIR` | `evidence/logging-red.txt` and `.exitstatus` | 4 checks, exactly the orphan-log check fails; exit 1 |
| Corrected publication source | `python3 tests/test_request_logging.py` | `evidence/logging-green.txt` and `.exitstatus` | 4 checks pass; exit 0 |

The test command deliberately prints stable case names/counts. The evidence
files contain its output without postprocessing. For full unittest failure
details use `python3 -m unittest discover -s tests -p test_request_logging.py -v`.

`python3 run_checks.py` additionally executes the original focused and broader
tests against the corrected server. The broader run now emits an ERROR log,
so its new output is not presented as the original captured green output.
No actual socket, production dashboard, alert routing, concurrency or latency
claim is tested. The identifier correlates the diagnostic with the order in
the request; it is not a globally unique request ID.

## Historical versus current parity

Every file under `captures/incident_orphan_product_policy/` is unchanged,
including its runner, metadata, exact patch, before-state, transcript, raw
results, checksums and July independent-review receipt. Its references to the
"final" or "top-level" source describe the historical package.

`before/README.md` and `before/test_capture_inventory.py` retain the other
top-level files changed by this follow-on. The original server is reconstructed
from the old before-state plus its exact patch, not copied from the new server.
`run_checks.py` restores exactly the old metadata's inventory in temporary space
and invokes the untouched old runner there. That runner checks the historical
source, evidence and receipt against their original checksums.

The wrapper then requires the new logging regression to fail against that old
after-state, applies only `request-logging.diff`, requires byte equality with
the current `server.py`, and requires all current checks to pass. The current
`manifest.json` binds the entire expanded package except itself, including the
old capture and new evidence. The wrapper verifies both inventories without
rewriting either record and leaves the maintained package unchanged.

This follow-on record reports implementation checks. The historical Pass
receipt is not independent certification of the new correction. It does not
establish that any outside monitoring system will alert on this log.
