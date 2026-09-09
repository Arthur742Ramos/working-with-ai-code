# Boolean-as-integer role handoff capture

This internal package preserves the verified Chapter 6 tester-to-implementer handoff. The before fixture accepts `True` for an `int` rule, the focused tester catches it, and the exact one-line patch selects strict built-in integer semantics.

The session originated from the earlier maintained role-relay validator at the commit recorded in `metadata.json`. Final packaging removed the retired chapter label and original support path from this copy. The origin commit, reconstructed-fixture status, agent version, commands, evidence checksums, and policy history remain recorded. Replay depends only on files inside the copied Chapter 6 package.

## Replay

Run from the final Chapter 6 package:

```bash
python3 captures/boolean_as_integer_role_handoff/run_capture.py
```

Default replay removes stale `.work/` state before preflight, checksum-verifies the before fixture, capture test, stored patch, evidence, every top-level executable support file, and the active independent-review receipt. It requires the resolved evidence root to remain under the resolved capture directory. It rebuilds disposable red and repaired states, runs the focused and broader checks with pytest caching disabled, compares the results with stored artifacts, and removes `.work/` on success or failure. It does not rewrite evidence or leave `.pytest_cache/` at the package root.

The `--record` flag intentionally refreshes reviewed patch and evidence files. Do not use it as a routine test option.

## Artifact ownership

- The tester artifact consists of the focused capture test, focused red output and status, and the contract through plan sections in `session.md`.
- The implementer artifact consists of the exact patch, focused and broader green evidence, and the action record through evidence-boundary sections in `session.md`.
- The tester and implementer artifacts come from one Claude Code session.
- The verifier role is represented by the later maintained integration-review receipt at `metadata.json` under `integration_review_receipt.verdict`, with its acceptance basis summarized in `parity.md`. No separate verifier transcript is claimed.

## Independent certification

A separate independent canonical review replayed the repaired package from a disposable copy, regenerated the state transition, challenged the one-line patch, checked command and chapter parity, and verified provenance, isolation, and the human-owned policy boundary. Its attributable receipt is `evidence/independent-review.md`.

Active package state is `complete_independently_reviewed`, review status is `completed`, and verdict is `Pass`. Replay rejects that state if the review becomes pending, the verdict changes, the evidence root resolves outside the capture package, or the package-local receipt is missing, external, or checksum-invalid. The shared session ledger was Pending during read-only package review and later moved to Pass during aggregate publication-control reconciliation.

## Dependencies and environment

The runner requires Python 3 and pytest. The recorded session used Python 3.14.6, pytest 9.1.1, Claude Code 2.1.210, and macOS. Replay removes ANSI color sequences and replaces only elapsed pytest timing with `<TIME>s`.

## Policy boundary

The captured selection uses exact built-in `int` semantics because the schema exposes `bool` separately and JSON distinguishes Booleans from numbers. The schema or application owner still owns that policy. Green checks confirm the selected contract; they do not choose it.

## Evidence boundary

The focused red proves that the reconstructed before predicate accepts `True` and that the independent test detects it. The patch and focused green prove the one-line repair. The broader green protects eight neighboring validator behaviors.

The capture does not exhaust numeric edge cases, establish semantics for another runtime, or prove every malformed schema shape. Its origin record remains honest; the final replay validates only the isolated Chapter 6 package.
