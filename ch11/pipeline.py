"""A small provider-neutral continuous delivery pipeline."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).parent


@dataclass(frozen=True)
class Stage:
    """One deterministic pipeline stage."""

    name: str
    command: tuple[str, ...]


STAGES = (
    Stage(
        "compile",
        (
            sys.executable,
            "-m",
            "py_compile",
            "deployment_guard.py",
            "incident_triage.py",
        ),
    ),
    Stage(
        "test",
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "test_deployment_guard.py",
            "test_incident_triage.py",
            "test_pipeline.py",
        ),
    ),
    Stage(
        "plan-and-policy",
        (
            sys.executable,
            "deployment_guard.py",
            "plan",
            "deployment.json",
        ),
    ),
)


def run_stage(stage: Stage) -> int:
    """Run one stage and preserve its real exit code."""
    print(f"== {stage.name} ==", flush=True)
    completed = subprocess.run(
        stage.command,
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


def run_pipeline(
    stages: Sequence[Stage] = STAGES,
) -> int:
    """Stop at the first failing authority boundary."""
    for stage in stages:
        result = run_stage(stage)
        if result:
            print(f"blocked_at={stage.name}")
            return result
    print("pipeline=READY_FOR_APPROVAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_pipeline())
