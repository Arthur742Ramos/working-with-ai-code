# Chapter 11 — Automation and operations: from proposal to production evidence

A production deployment modeled as a reviewable proposal: deterministic
policy checks, a provider-neutral pipeline that stops at the approval
boundary, a source-linked incident timeline, and a post-change evidence
packet. It never connects to a cloud account or makes a production change.

- **`deployment_guard.py`** — Listing 11.1: Rollout-policy branch for unavailable capacity, plus plan and post-change verification
- **`pipeline.py`** — Listing 11.2: Stopping the pipeline at the approval boundary
- **`incident_triage.py`** — Listing 11.3: Selecting one deployment's events in time order (and printing Listing 11.4)
- **`listing_11_5.txt`** — Listing 11.5: A post-change evidence packet
- **`deployment.json`** — the maintained safe deployment proposal
- **`observation.json`** — sanitized post-change observations
- **`incident.jsonl`** — sanitized structured events for one rollout
- **`test_deployment_guard.py`**, **`test_incident_triage.py`**, **`test_pipeline.py`** — policy, timeline, and pipeline checks
- **`captures/`** — controlled red-state reproduction (README, red fixture, session transcript)
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

## Setup and checks

Use CPython 3.11 or newer, from this directory:

```bash
python3 -m pytest -q
python3 pipeline.py
python3 deployment_guard.py plan deployment.json
python3 deployment_guard.py verify deployment.json observation.json
python3 incident_triage.py incident.jsonl deploy-104
```

`python3 -m pytest -q` reports **24 passed**. The pipeline compiles the
tools, runs the tests, and builds a read-only plan that stops at
`READY_FOR_APPROVAL`; an actual write is intentionally outside this example.

## Listing map

- **Listing 11.1** is the rollout-policy branch in `deployment_guard.py` that
  rejects a `max_unavailable` outside `(0, 1)`.
- **Listing 11.2** is `run_stage` and `run_pipeline` in `pipeline.py`, which
  stop at the first failing stage and otherwise print `READY_FOR_APPROVAL`.
- **Listing 11.3** is `select_timeline` in `incident_triage.py`, which filters
  one deployment's events and sorts them by time.
- **Listing 11.4** is the source-linked timeline that
  `python3 incident_triage.py incident.jsonl deploy-104` prints, keeping the
  `incident.jsonl:<line>` source identifier beside each fact.
- **Listing 11.5** is `listing_11_5.txt`, the post-change evidence packet.

## Real red-to-green capture

The capture began with `deployment.json` equal to the red fixture under
`captures/`, where `max_unavailable` was `2`. The agent read the config and
guard, changed the value to `1`, showed the exact diff, and reran the focused
and full suites. See [`captures/README.md`](captures/README.md).

## Limits

The policy values are teaching decisions, not universal production defaults.
A real service needs capacity measurements, provider-specific plans, protected
credentials, deployment approval, live observability, and a tested rollback.

See the [main README](../README.md) for setup instructions.
