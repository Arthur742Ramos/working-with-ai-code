import inspect
from pathlib import Path
import subprocess
import sys
import textwrap

import incident_triage
import pipeline


ROOT = Path(__file__).parent

LISTING_11_1 = """\
if (
    type(plan.max_unavailable) is not int
    or plan.max_unavailable not in (0, 1)
):
    failures.append(
        "max_unavailable must be 0 or 1"
    )
"""

LISTING_11_2 = """\
def run_stage(stage: Stage) -> int:
    print(f"== {stage.name} ==", flush=True)
    try:
        completed = subprocess.run(
            stage.command,
            cwd=ROOT,
            check=False,
        )
    except OSError:
        print(
            f"tool_error={stage.name}",
            file=sys.stderr,
        )
        return LAUNCH_FAILURE
    return completed.returncode


def run_pipeline(
    stages: Sequence[Stage] = STAGES,
) -> int:
    for stage in stages:
        result = run_stage(stage)
        if result:
            print(f"blocked_at={stage.name}")
            return result
    print("pipeline=READY_FOR_APPROVAL")
    return 0
"""

LISTING_11_3 = """\
def select_timeline(
    events: Iterable[Event],
    deployment_id: str,
) -> list[Event]:
    selected = (
        event
        for event in events
        if event.deployment_id == deployment_id
    )
    return sorted(selected, key=_event_time)
"""

LISTING_11_4 = """\
[incident.jsonl:1] 2030-04-18T14:00:00Z INFO
[incident.jsonl:1] event=rollout_started
[incident.jsonl:1] revision=sample-api:1.8.0
[incident.jsonl:3] 2030-04-18T14:04:00Z WARN
[incident.jsonl:3] event=ready_replicas_below_target
[incident.jsonl:3] revision=sample-api:1.8.0
[incident.jsonl:4] 2030-04-18T14:05:00Z ERROR
[incident.jsonl:4] event=error_rate_above_limit
[incident.jsonl:4] revision=sample-api:1.8.0
[incident.jsonl:4] error_rate=0.071
[incident.jsonl:4] trace=4bf92f3577b34da6a3ce929d0e0e4736
[incident.jsonl:5] 2030-04-18T14:07:00Z INFO
[incident.jsonl:5] event=rollback_started
[incident.jsonl:5] revision=sample-api:1.7.2
[incident.jsonl:6] 2030-04-18T14:13:00Z INFO
[incident.jsonl:6] event=service_recovered
[incident.jsonl:6] revision=sample-api:1.7.2
"""

LISTING_11_5 = """\
source_revision=<reviewed-commit>
target=production/sample-api
plan_id=plan-104
plan_digest=<sha256>
policy_version=rollout-policy-7
approval_scope=apply plan-104 once
applied_revision=sample-api:1.8.0
verification=FAIL error_rate=0.071
recovery_revision=sample-api:1.7.2
recovery_status=observed at 14:13Z
timeline=incident.jsonl:1,3,4,5,6
open_question=failed request path
owner=release-team
"""


def _without_function_docstring(function: object) -> str:
    lines = inspect.getsource(function).splitlines()
    lines = [
        line for line in lines
        if not line.strip().startswith('"""')
    ]
    return "\n".join(lines) + "\n"


def test_listing_11_1_matches_policy_branch() -> None:
    source = (ROOT / "deployment_guard.py").read_text()
    expected = textwrap.indent(LISTING_11_1, "    ")

    assert expected in source


def test_listing_11_2_matches_pipeline_functions() -> None:
    rendered = (
        _without_function_docstring(pipeline.run_stage)
        + "\n\n"
        + _without_function_docstring(pipeline.run_pipeline)
    )

    assert rendered == LISTING_11_2


def test_listing_11_3_matches_timeline_selector() -> None:
    rendered = _without_function_docstring(
        incident_triage.select_timeline
    )

    assert rendered == LISTING_11_3


def test_listing_11_4_matches_timeline_output() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "incident_triage.py",
            "incident.jsonl",
            "deploy-104",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout == LISTING_11_4


def test_listing_11_5_matches_maintained_artifact() -> None:
    artifact = (ROOT / "listing_11_5.txt").read_text()

    assert artifact == LISTING_11_5
