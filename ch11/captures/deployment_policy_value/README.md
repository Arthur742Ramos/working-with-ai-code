# Deployment-policy value capture

This internal package preserves one complete coding-agent session for target Chapter 11, *Taking AI-assisted changes to production*. The selected behavior is a bounded rollout repair: a six-replica proposal with `max_unavailable: 2` is structurally accepted but violates the maintained policy, while `max_unavailable: 1` satisfies that policy.

## Provenance

`before/deployment_guard.py` and `before/deployment.json` are historical
byte-for-byte copies from the original Chapter 11 support at commit
`38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6`. `before/test_deployment_guard.py`
is a frozen copy of the package test immediately before the 2026-08-28 support
contract revision. It preserves the historical 24-test replay contract; it is
not claimed as an original-session byte copy. All checksums remain in
`metadata.json` as provenance. Replay does not resolve any original repository
path.

The initial inspect-red-plan contract is reconstructed and labeled because its standalone prompt was not retained. The retained completion direction, package-local harness correction, one-line production action, machine-generated diff, focused green, broader green, original canonical-support green, and action sequence come from the actual coding-agent session. The final-package green result was added later as separately labeled release evidence for this isolated package.

## Record and replay

Run from the final package directory:

```bash
python3 captures/deployment_policy_value/run_capture.py --record
python3 captures/deployment_policy_value/run_capture.py
```

The runner performs this sequence in disposable space inside the capture directory:

1. Verify before fixtures, capture inputs, preserved origin evidence, and every declared final-package checksum.
2. Reproduce focused red from the immutable before fixture.
3. Change only `rollout.max_unavailable` from `2` to `1` in the disposable configuration.
4. Regenerate and compare the exact unified diff.
5. Reproduce focused green and the original 24-test broader suite against the disposable after-state, using the historical test snapshot.
6. Run all 29 top-level final-package tests without collecting capture internals.
7. Verify stored artifact hashes, unchanged package checksums, and both parity ledgers.
8. Remove disposable files on success or failure.

Default replay never writes the patch or evidence. `--record` is reserved for an intentional evidence refresh after review and writes only capture-local patch and evidence artifacts.

## Direct commands

The focused red and green command is the same; only the disposable configuration differs:

```bash
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_policy.py::\
test_schema_valid_deployment_satisfies_policy
```

The captured broader command runs the 24 operational checks beside the
disposable after-state. Replay uses the historical top-level deployment test
snapshot so later CLI contract changes cannot rewrite this historical session:

```bash
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_guard.py \
  test_incident_triage.py \
  test_pipeline.py
```

The final-package command runs 29 local tests from the package directory:

```bash
python3 -m pytest -q -p no:cacheprovider
```

## Dependencies and environment

The recorded session used Claude Code 2.1.210.642, CPython 3.14.6, and pytest 9.1.1. No network access, cloud credential, provider command, or target-system write is required. The runner disables pytest color, third-party plugin auto-loading, bytecode output, and the pytest cache provider.

Stored command output preserves genuine pytest text and exit status, with only the machine-dependent elapsed-time value replaced by `<TIME>`. Default replay applies the same normalization while comparing fresh output and does not rewrite stored files.

## Capture-harness correction

The staged focused test originally asserted that the loaded value remained `2`. That assertion proved the unsafe fixture was still unsafe, but it also made a green run impossible after a production-only value repair. Before changing the disposable production configuration, the agent replaced that package-local assertion with loader-to-config parity and reran genuine red. The final focused test now discriminates the behavior with the same test in both states. No production or original canonical file changed during this correction.

## Origin evidence and executable boundary

`evidence/canonical-support-green.txt` preserves the original 24-test read-only canonical run. Its checksum, command, status, and original source hashes remain in `metadata.json` with replay status `preserved_not_executed`. This proves what ran during the original session; it does not make those old paths a dependency of the final package.

`evidence/final-package-green.txt` is separately labeled current evidence. Replay executes that package-local command and verifies all 29 top-level tests. The local checksum manifest covers the implementation, fixtures, tests, listing artifact, pytest configuration, README, requirements, and parity ledger.

## Approval basis and human-owned policy boundary

The standing direction authorized the coding agent to choose the best bounded implementation without another checkpoint. Acting under that direction, the agent selected `max_unavailable: 1` for the six-replica fixture because it is the largest value allowed by the maintained guard and preserves five ready replicas if one becomes unavailable. The record does not claim that the author named an option from a menu.

Live capacity evidence still controls a real deployment. The service owner or release team must determine whether five ready replicas can carry peak traffic, satisfy service objectives, and preserve rollback headroom. The fixture value is a captured policy decision, not a universal production default.

## What the checks prove

Focused red proves that `2` passes the narrow structural check, loads through the real parser, and reaches exactly one rollout-policy violation. Focused green proves that changing only the value to `1` removes that violation. Broader green proves that all 24 operational cases pass against the disposable after-state. Final-package green proves that those 24 checks and five exact listing-parity checks pass together in the isolated package.

## What the checks do not prove

The checks do not prove that five replicas can carry live traffic, that one unavailable replica is safe for every service, that provider-side plans match repository state, or that rollback works against a real target. They do not exercise credentials, cloud APIs, traffic, observability, or target drift. Those facts require current production evidence and a separately authorized deployment.

## Review status

The coding-agent session remains complete and reproducible. The independent review
receipt dated 2026-07-15 applies to the package state reviewed then. Later support
contract changes require recertification, so the current package stage is marked
`complete_pending_recertification` in `metadata.json`. The historical receipt is
preserved and is not presented as a review of the changed package.

`session.md` remains the historical coding-agent record and therefore retains the
pending-review language that was accurate when the session package was assembled.
The current recertification state is defined by this README, `metadata.json`, and
`parity.md`.
