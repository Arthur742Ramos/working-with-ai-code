"""Plan and verify a bounded production deployment."""

from __future__ import annotations

import argparse
import json
import math
import reprlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MAX_ERROR_RATE = 0.02


@dataclass(frozen=True)
class DeploymentPlan:
    """A reviewable deployment proposal."""

    service: str
    environment: str
    current_revision: str
    proposed_revision: str
    replicas: int
    batch_size: int
    max_unavailable: int
    readiness_path: str
    error_rate_limit: float
    rollback_revision: str


@dataclass(frozen=True)
class Observation:
    """Post-change facts collected from the target."""

    revision: str
    ready_replicas: int
    total_replicas: int
    error_rate: float
    request_succeeded: bool


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    return data


def load_plan(path: Path) -> DeploymentPlan:
    """Load a deployment proposal from JSON."""
    data = _read_json(path)
    rollout = data["rollout"]
    health = data["health"]
    rollback = data["rollback"]
    return DeploymentPlan(
        service=data["service"],
        environment=data["environment"],
        current_revision=data["current_revision"],
        proposed_revision=data["proposed_revision"],
        replicas=data["replicas"],
        batch_size=rollout["batch_size"],
        max_unavailable=rollout["max_unavailable"],
        readiness_path=health["readiness_path"],
        error_rate_limit=health["error_rate_limit"],
        rollback_revision=rollback["revision"],
    )


def load_observation(path: Path) -> Observation:
    """Load observed post-change state from JSON."""
    data = _read_json(path)
    return Observation(
        revision=data["revision"],
        ready_replicas=data["ready_replicas"],
        total_replicas=data["total_replicas"],
        error_rate=data["error_rate"],
        request_succeeded=data["request_succeeded"],
    )


def _is_finite_number(value: object) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    return (
        isinstance(value, float)
        and math.isfinite(value)
    )


def _is_valid_rate_limit(value: object) -> bool:
    return (
        _is_finite_number(value)
        and 0 < value <= MAX_ERROR_RATE
    )


def rollout_violations(
    plan: DeploymentPlan,
) -> list[str]:
    """Return deterministic rollout-policy failures."""
    failures: list[str] = []
    if (
        type(plan.batch_size) is not int
        or plan.batch_size not in (1, 2)
    ):
        failures.append("batch_size must be 1 or 2")
    if (
        type(plan.max_unavailable) is not int
        or plan.max_unavailable not in (0, 1)
    ):
        failures.append(
            "max_unavailable must be 0 or 1"
        )
    if (
        not isinstance(plan.readiness_path, str)
        or not plan.readiness_path.startswith("/")
    ):
        failures.append("readiness_path must start with /")
    rate = plan.error_rate_limit
    if not _is_valid_rate_limit(rate):
        failures.append(
            "error_rate_limit must be > 0 and <= 0.02"
        )
    if plan.rollback_revision != (
        plan.current_revision
    ):
        failures.append(
            "rollback must match current revision"
        )
    return failures


def policy_violations(
    plan: DeploymentPlan,
) -> list[str]:
    """Return deterministic production policy failures."""
    failures: list[str] = []
    if plan.environment != "production":
        failures.append("environment must be production")
    if plan.current_revision == plan.proposed_revision:
        failures.append("proposed revision must change")
    if (
        type(plan.replicas) is not int
        or plan.replicas < 3
    ):
        failures.append(
            "production needs at least 3 replicas"
        )
    failures.extend(rollout_violations(plan))
    return failures


def verification_failures(
    plan: DeploymentPlan,
    observed: Observation,
) -> list[str]:
    """Compare observations with approved postconditions."""
    failures: list[str] = []
    if observed.revision != plan.proposed_revision:
        failures.append(
            "observed revision does not match plan"
        )
    if type(observed.total_replicas) is not int:
        failures.append("observed replica total is invalid")
    elif observed.total_replicas != plan.replicas:
        failures.append(
            "observed replica total does not match"
        )
    if type(observed.ready_replicas) is not int:
        failures.append(
            "observed ready replicas are invalid"
        )
    elif observed.ready_replicas != plan.replicas:
        failures.append(
            "not all planned replicas are ready"
        )
    rate = observed.error_rate
    limit = plan.error_rate_limit
    if (
        not _is_finite_number(rate)
        or not 0 <= rate <= 1
    ):
        failures.append("observed error rate is invalid")
    elif not _is_valid_rate_limit(limit):
        failures.append("plan error rate limit is invalid")
    elif rate > limit:
        failures.append("observed error rate exceeds limit")
    if observed.request_succeeded is not True:
        failures.append("representative request failed")
    return failures


def _short_repr(
    value: object,
    limit: int = 40,
) -> str:
    rendered = reprlib.repr(value)
    if len(rendered) <= limit:
        return rendered
    return rendered[: limit - 3] + "..."


def _safe_field(
    value: object,
    limit: int = 80,
) -> str:
    if not isinstance(value, str):
        return _short_repr(value, limit)
    sample = value[:limit]
    rendered = "".join(
        character
        if character.isprintable()
        else f"\\x{ord(character):02x}"
        for character in sample
    )
    if len(value) > limit:
        rendered += "..."
    if len(rendered) > limit:
        rendered = rendered[: limit - 3] + "..."
    return rendered


def _format_rate(value: object) -> str:
    if not _is_valid_rate_limit(value):
        return _short_repr(value)
    rendered = repr(value)
    if "e" in rendered.lower():
        return rendered
    whole, separator, fraction = rendered.partition(".")
    if not separator:
        return f"{whole}.000"
    return f"{whole}.{fraction.ljust(3, '0')}"


def describe_plan(
    plan: DeploymentPlan,
    failures: list[str] | None = None,
) -> str:
    """Render the pipeline's small approval surface."""
    lines = [
        f"service={_safe_field(plan.service)}",
        f"environment={_safe_field(plan.environment)}",
        (
            "revision="
            f"{_safe_field(plan.current_revision)} -> "
            f"{_safe_field(plan.proposed_revision)}"
        ),
        (
            "rollout=batch "
            f"{_safe_field(plan.batch_size)}, "
            "max unavailable "
            f"{_safe_field(plan.max_unavailable)}"
        ),
        (
            f"health={_safe_field(plan.readiness_path)}, "
            "error rate <= "
            f"{_format_rate(plan.error_rate_limit)}"
        ),
        f"rollback={_safe_field(plan.rollback_revision)}",
    ]
    if failures is None:
        failures = policy_violations(plan)
    status = "PASS" if not failures else "BLOCK"
    lines.append(f"policy={status}")
    lines.extend(f"violation={item}" for item in failures)
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )
    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("config", type=Path)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("config", type=Path)
    verify_parser.add_argument("observation", type=Path)
    return parser.parse_args()


def main() -> int:
    """Run a read-only plan or post-change verification."""
    args = _parse_args()
    plan = load_plan(args.config)
    if args.command == "plan":
        failures = policy_violations(plan)
        print(describe_plan(plan, failures))
        return 0 if not failures else 2
    plan_failures = policy_violations(plan)
    if plan_failures:
        print("verification=FAIL")
        for item in plan_failures:
            print(f"failure=plan policy: {item}")
        return 3
    observed = load_observation(args.observation)
    failures = verification_failures(plan, observed)
    status = "PASS" if not failures else "FAIL"
    print(f"verification={status}")
    for item in failures:
        print(f"failure={item}")
    return 0 if not failures else 3


if __name__ == "__main__":
    raise SystemExit(main())
