# Incident orphan-product policy capture

This internal package preserves one complete coding-agent session for the Chapter 5 diagnosis slice. It records inspection, genuine red, the approved bounded policy, the exact smallest reviewable production diff, genuine focused and broader green, and replay checks.

## Selected behavior

The deterministic incident seed creates an order item whose product code is absent from the catalog. The focused check requires that path to raise a named `MissingProductError` with stable order and product context instead of an accidental `TypeError`.

The API must fail the whole summary closed while the orphaned reference is repaired upstream. The author approved that policy boundary but did not name an HTTP status. Under the standing direction to choose the best implementation, the agent selected `422` for the well-formed request whose current resource state cannot produce a valid summary.

This behavior belongs in Chapter 5 because it turns a deterministic reproduction and falsifiable hypothesis into one bounded repair with explicit evidence limits.

## Origin provenance

The immutable before fixture is a byte-identical retained copy of the incident demo used for the original session before the twelve-chapter restructure. The origin is historical provenance only. Replay does not locate, import, checksum, or execute that earlier repository path.

The reviewed green after-state now lives at the top of this final package. The stored patch must reproduce top-level `server.py`; the retained seed and both capture tests must match their package-local maintained copies.

## Smallest-reviewable-diff decision

The final handler catch keeps `self._send(...)` and `return` on separate lines. This matches the surrounding early-exit idiom and keeps the response side effect distinct from control flow. Collapsing them into `return self._send(...)` would change one fewer line, but it would not narrow behavior or scope. The recorded patch is minimal by responsibility and readable in context; it is not optimized for changed-line count.

## Record and replay

Run either command from the final Chapter 5 package root.

Intentionally recreate the stored evidence:

```bash
python3 captures/incident_orphan_product_policy/run_capture.py --record
```

Replay without rewriting evidence:

```bash
python3 captures/incident_orphan_product_policy/run_capture.py
```

The runner verifies the package-local before fixture, tests, patch, evidence, final green source, final seed, maintained top-level tests, publication transcript, package documents, parity checksums, and the active independent-review receipt. It copies the immutable before fixture into `.work`, requires the focused red exit status, applies and compares the stored patch, and runs both capture greens. It copies the final implementation and maintained tests into disposable space for the final-package greens, so `shop.db`, `server.log`, bytecode, and test caches never need to be created at the package root. Cleanup removes those runtime artifacts and `.work` on success, failure, and preflight failure. Default replay never writes evidence.

The runner also verifies the exact maintained-file inventory. Runtime artifacts are excluded because replay must remove them. Any added, removed, or renamed maintained file requires an intentional inventory update.

## Independent review state

The independent canonical certification completed with verdict `Pass` on 2026-07-15. Active package stage is `complete_independently_reviewed`, review status is `completed`, and the attributable checksum-locked receipt is `evidence/independent-review.md`.

Default replay rejects a completed stage if the active status is not `completed`, the verdict is not `Pass`, the exact receipt is missing or checksum-invalid, or the receipt's attribution and PASS markers contradict `metadata.json`. The historical session record remains unchanged. The shared ledger is a separate publication-control surface and is not part of this package verdict.

## Dependencies and assumptions

- Python 3.8 or later
- Python standard library with SQLite support
- POSIX `patch` and `diff`
- Files contained in this final Chapter 5 package

No network service, package installation, repository root, or other chapter is required.

## Human-owned policy boundary

The approved product policy is to reject the whole summary with a stable contextual `MissingProductError` and fail closed at the API while upstream data is repaired. The coding agent selected the concrete `422` mapping; the author did not name that status.

The owning team still decides how to repair or reject orphaned references, whether the API contract should retain `422`, what client-facing detail is safe outside this sanitized fixture, and what monitoring or migration closes the upstream integrity gap. The patch does not price the missing line at zero, omit it, or substitute a placeholder.

## What the checks prove

The focused red proves that deterministic order `7` reaches missing product code `90233` and that the before implementation exposes `TypeError: 'NoneType' object is not subscriptable`.

The focused green proves that the exported exception class and the runtime exception type are both named `MissingProductError`, with the stable message `order 7 references missing product 90233`, before total calculation. The observed type in the evidence is derived from `type(exc).__name__` rather than a hardcoded label.

The broader green pins the deterministic summary for valid order `1` and drives the real `Handler.do_GET()` path to prove that the orphan returns `422` with the stable contextual message. The final-package checks prove the same outputs from the maintained top-level files.

## What the checks do not prove

The checks do not prove that `422` is the final public contract, that every possible orphan is detected, that concurrent cache behavior is correct, that diagnostic context is safe for a production client, that latency improves, or that upstream referential integrity has been repaired. They also do not replace integration, load, security, or migration testing.

## Evidence handling

All command output and exit statuses are stored raw under `evidence/`. No output normalization was applied. The production change remains the exact patch under `patches/`; replay applies it only to disposable `.work` and verifies that result against the package-local final `server.py`.
