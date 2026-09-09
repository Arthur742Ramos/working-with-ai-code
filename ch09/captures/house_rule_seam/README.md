# House-rule seam capture

## Scope

This package preserves a complete Chapter 9 coding-agent session for one bounded behavior: feature modules must route outbound HTTP through `http_client.call` rather than import a transport such as `requests` directly.

The behavior belongs in Chapter 9 because a short project contract changes an otherwise plausible implementation at a trust boundary. The approved client owns credentials, bounded transient retries, fail-closed behavior, and transport injection for tests.

The immutable before and after states are package-local. The after state changes only `alerts.py`; `http_client.py` remains byte-identical.

## Record command

Run from the Chapter 9 final package directory after intentional review:

```bash
python3 captures/house_rule_seam/run_capture.py --record
```

Record mode copies `before/` and `tests/` into disposable space inside this capture, reproduces focused red, applies the stored machine-generated patch, runs focused and broader green, runs the package-local top-level suite, and refreshes command evidence and its checksums. It does not access repository-root chapter or support files.

## Non-recording replay

Run from the Chapter 9 final package directory:

```bash
python3 captures/house_rule_seam/run_capture.py
```

Default replay performs the same disposable red, patch, focused green, broader green, and package-green sequence. It compares output, exit status, patch content, capture checksums, package checksums, and stored origin evidence with the recorded values. It does not rewrite evidence or metadata. A context-managed work directory is removed on success and failure, and replay refuses to start or finish with a stale `.work-*` directory.

## Exact commands represented by the runner

Focused red and focused green use the same command against the disposable before and repaired states:

```bash
PYTHONPATH=before HOUSE_RULE_ROOT=before \
  PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -q -p no:cacheprovider \
  tests/test_alerts.py::test_send_alert_routes_through_house_client
```

The broader capture check runs all copied capture tests:

```bash
PYTHONPATH=before HOUSE_RULE_ROOT=before \
  PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -q -p no:cacheprovider tests
```

The final package check runs from the copied package root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  -p no:cacheprovider
```

`pytest.ini` excludes `captures/`, so the final green suite does not accidentally collect the retained red fixture or duplicate capture test modules.

## Dependencies and environment

The completed session used Claude Code `2.1.210.642`, model `gpt-5.6-sol[1m]`, Python 3.14.6, pytest 9.1.1, and the system `patch` and `diff` commands. The checks use only Python's standard library plus pytest. They disable pytest color, inherited pytest options, bytecode output, and pytest's cache provider. The focused test installs an in-memory `requests.post` stub only so the before fixture can complete without that third-party dependency or a live network call. It patches `http_client.call` before loading the feature, so direct and module-qualified shared-client imports are both valid while a transport bypass records no seam call.

Stored files retain raw combined command output. Replay normalizes only pytest's elapsed-time value for comparison. No stored output is normalized.

## Origin provenance

`metadata.json` retains the repository commit, canonical chapter and support checksums, and canonical-support green output captured during the original session. Those fields establish where the copied fixture and publication transcript came from. They are historical records, not live replay inputs.

The localized runner verifies the stored canonical-support output and its checksum but never resolves or executes the former `chapters/ch09.md` or `code/ch09/` paths. The top-level final package is now the maintained executable parity surface.

## Approval basis

The author's standing direction delegated the exact implementation choice for this bounded slice and set the approval policy: outbound HTTP must use the required shared client seam with no exception. The agent selected the three-line substitution as the smallest reviewable diff because it preserves the endpoint, payload, success threshold, response-variable idiom, and shared client unchanged. Collapsing `send_alert()` into one return expression would change readable surrounding structure and hide the response-interface adaptation without narrowing behavior. This package does not claim that the author selected a named menu option.

## Human-owned policy boundary

Service maintainers own the trust policy for outbound HTTP. For this slice, the policy is settled: alert delivery remains behind `http_client.call`, and no direct-transport exception is allowed. The agent selected the narrowest behaviorally complete change that fits the existing function. The evidence does not authorize the same decision for a different project or service boundary.

## What the checks prove

The focused red check proves that the before implementation can return success without routing through `http_client.call`: the shared seam records no method, URL, or JSON. Focused green proves that the repaired `send_alert` sends the exact `POST` method, alert URL, and JSON through that seam while preserving the success result. The same observer accepts both `from http_client import call` and `import http_client; http_client.call(...)`; a separate positive case locks that distinction.

The broader ten-test check proves that the repaired feature also receives injected authentication, reports success and failure through `Response.status`, preserves bounded transient retries, fails closed without a configured transport, rejects direct transport imports, keeps the guard's direct-transport fixture live, and accepts module-qualified shared-client use. The 28-test package-local green check proves the maintained alert, retrieval, MCP, parity, isolation, cleanup, and review-state surfaces pass together.

## What the checks do not prove

The checks do not prove live endpoint availability, real credential validity, production transport behavior, timing or backoff policy, observability, or that every future outbound protocol belongs behind this seam. They also do not make the trust policy portable to another service. Those remain system-owner decisions.

## Independent review state

The first independent review returned `Fail` for import-shape overfitting, unmapped printed condensation, and the then-active historical mapping. Those package defects were repaired without changing the production fixtures, patch, or historical session record.

The independent canonical re-review completed with verdict `Pass`. Active package stage is `complete_independently_reviewed`, active review status is `completed`, and the checksum-locked receipt is `evidence/independent-review.md`. Replay rejects a completed claim when the receipt is missing, outside `evidence/`, pending, checksum-invalid, paired with a non-Pass verdict, or paired with blocking findings.

The shared ledger was `Pending` during the read-only package review and later moved to aggregate `Pass` during whole-book reconciliation. That current aggregate state does not rewrite `session.md`, `metadata.json`, or `evidence/independent-review.md`, which retain the workflow state observed when each historical record was created. Replay neither reads nor edits the ledger. Current certification is carried by this README, `metadata.json`, `parity.md`, and the active review receipt.

The first broader attempt failed because the disposable test tree omitted the guard's own `fixtures/direct_requests/alerts.py` input. That raw setup failure is preserved in `evidence/broader_green_setup_failure.txt` with exit status `1`. The agent copied the byte-identical fixture into the package and reran the unchanged broader command to obtain genuine green.
