# PR generator retry-wiring capture

This package preserves a real Chapter 2 coding-agent session for one bounded behavior: the command-line interface must use the existing conversational retry path when structured output fails JSON parsing or schema validation. The historical helper already allowed two retries, for three attempts total. The captured repair wires the command-line entry point to that helper without changing its policy.

The immutable `before/` and `after/` directories preserve the implementation used during the session, including its original live-adapter and third-party-validator boundaries. Those files are origin evidence, not the final package's default runtime. The promoted top-level package uses the staged chapter's offline fixture and the standards-compliant `jsonschema` validator.

## Exact record command

Run from the final Chapter 2 package directory after intentional review. Recording rewrites only the three output and exit-status pairs under `evidence/`.

```bash
python3 captures/pr_generator_retry_wiring/run_capture.py \
  --record
```

## Non-recording replay

Routine replay rebuilds from `before/`, applies the stored patch in disposable `.work/`, runs the focused and broader capture checks, compares raw output and exit statuses with stored evidence, and removes working files on success or failure. It also checksums the package-local green implementation, copies the complete package into disposable `.package-work/`, and runs the top-level suite from that isolated copy. It does not read repository-root chapter or support files.

```bash
python3 captures/pr_generator_retry_wiring/run_capture.py
```

The runner prints red, patch, focused-green, broader-green, package-green, review, cleanup, and parity statuses. Drift in an immutable source, patch, capture test, evidence file, action record, package record, promoted package file, review state, or review receipt stops replay. Replay also rejects generated `__pycache__`, `.pytest_cache`, and `.pyc` residue and confirms that its disposable `.work/` and `.package-work/` directories are removed.

## Review state

The first independent canonical review completed with verdict `Fail`. Its attributable receipt remains `evidence/first-independent-review.md`, and its three blocking findings remain part of the historical record. The stale publication mapping, omitted focused command, and lost patch-context space were repaired without rewriting the original red, patch, green, or session evidence.

A separate read-only reviewer replayed the repaired canonical package and final-code mirror, regenerated the exact patch, checked isolation, cleanup, provenance, Markdown and Word parity, and the human-owned policy boundary, then issued verdict `Pass`. The active receipt is `evidence/independent-review.md`.

Active package state is `complete_independently_reviewed`, independent review status is `completed`, and verdict is `Pass`. Default replay rejects this state unless both the retained failed-review receipt and the active Pass receipt exist under `evidence/` with their recorded checksums. It also rejects a missing active review, a non-Pass verdict, or any reported finding in the active review metadata.

## Final-polish recertification

`evidence/final-polish-recertification.json` separately certifies the promoted package after the standards-compliant validator, checklist, and provider-boundary changes. Replay verifies that receipt, its 18-test count, current support checksums, and preserved historical checksums. The receipt does not revise the captured retry session or either independent review.

## Dependencies and environment assumptions

Replay needs Python 3, the standard `patch` command, and `jsonschema` for the promoted top-level suite. The historical capture tests inject deterministic stand-ins for the original model adapter and validator dependency, so the preserved red/diff/green exchange itself does not call a provider or third-party validator. Replay needs no network, model credential, Git repository, or model SDK.

The raw capture evidence required no normalization. The output contains no timing, color codes, memory addresses, or machine-specific paths.

## Selected behavior and approval basis

The focused defect belongs in Chapter 2 because it turns the chapter's Contract, Conversation, and Checks progression into one machine-checkable workflow. The command-line path had the contract and checks, but skipped the conversation after the first invalid response.

The approval basis was the standing direction to choose the best implementation without another checkpoint. The agent selected the existing helper's policy unchanged: JSON syntax failures and schema failures are retryable, with two retries and three attempts total. This record does not claim that the author chose a named menu option.

## Human-owned policy boundary

A human owns which validation failures merit another model call and how many attempts the application may spend. This capture records the bounded policy selected for this slice. It does not generalize that policy to transport errors, rate limits, authentication failures, or other workflows.

## What the focused check proves

The focused red check proves that the historical before-state command-line path exits after one malformed reply even though a valid second reply is available. Focused green proves that the one-line wiring change reaches the existing conversational correction, preserves the malformed assistant reply, includes validation detail in the user correction, succeeds after two calls, and saves the valid structured output.

## What the broader check proves

The broader check protects three neighboring behaviors:

- Valid first-pass output still succeeds after one model call.
- Schema-invalid JSON receives feedback and succeeds after two calls.
- Repeated malformed output remains bounded at three calls and exits with failure.

The isolated package check separately proves that the promoted green package runs with only its copied files plus the documented `jsonschema` dependency, without repository context, network access, credentials, or a model SDK.

## What the checks do not prove

The checks do not prove that a live model will follow the correction, that generated pull-request claims are factually true, that two retries is the right cost policy for every application, or that transport failures should retry. Origin checksums preserve the historical session boundary; they do not make the old captured implementation the default runtime.
