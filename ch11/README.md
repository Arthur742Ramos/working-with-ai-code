# Chapter 11 operations example

This directory contains the runnable example for Chapter 11, "AI for
Automation and Operations." It models a production deployment as a reviewable
proposal, deterministic policy checks, post-change verification, and a
source-linked incident timeline. It never connects to a cloud account or makes
a production change.

## Setup and checks

Use CPython 3.11 or newer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python pipeline.py
```

The provider-neutral pipeline compiles the tools, runs the tests, and builds a
read-only deployment plan. It stops at `READY_FOR_APPROVAL`; an actual write is
intentionally outside this example.

Inspect the approved plan and observed postconditions:

```bash
python3 deployment_guard.py plan deployment.json
python3 deployment_guard.py verify \
  deployment.json observation.json
```

Build a bounded incident timeline:

```bash
python3 incident_triage.py incident.jsonl deploy-104
```

## Files

- `deployment.json` is the maintained safe proposal.
- `deployment_guard.py` parses the proposal, checks policy, and verifies
  observed state.
- `pipeline.py` keeps compile, tests, and plan-and-policy as separate stages.
- `observation.json` records generic post-change facts.
- `incident.jsonl` contains sanitized structured events for one rollout.
- `incident_triage.py` selects a deployment timeline and keeps source
  identifiers beside each fact.
- `captures/deployment-before.json` preserves the one-line red state.
- `captures/session-transcript.md` preserves the sanitized real command record.
- The `test_*.py` files check policy, postconditions, and timeline selection.

## Real red-to-green capture

The real capture began with `deployment.json` equal to
`captures/deployment-before.json`. The focused test failed because
`max_unavailable` was `2`. The agent read the config and guard, proposed one
edit, changed the value to `1`, showed the exact diff, and reran the focused and
full suites.

The captured suite reported 10 passing tests. Later hardening added a
mixed-offset ordering test and a representative-request postcondition test, so
the maintained suite reports 12.

Use a disposable worktree to reproduce that state. Never leave the maintained
configuration red. The fixture and detailed provenance live in
`captures/README.md`.

## Limits

The policy values are teaching decisions, not universal production defaults.
A real service needs capacity measurements, provider-specific plans, protected
credentials, deployment approval, live observability, and a tested rollback.
The example demonstrates the control surfaces without pretending to supply
those systems.
