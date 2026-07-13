from dataclasses import replace
from pathlib import Path
import pytest

from deployment_guard import (
    Observation,
    load_plan,
    policy_violations,
    verification_failures,
)


ROOT = Path(__file__).parent
CONFIG = ROOT / "deployment.json"
BEFORE = ROOT / "captures" / "deployment-before.json"


def test_production_config_is_safe() -> None:
    plan = load_plan(CONFIG)

    assert policy_violations(plan) == []
    invalid_values = (
        ("batch_size", True, "batch_size"),
        ("max_unavailable", True, "max_unavailable"),
        ("max_unavailable", False, "max_unavailable"),
        ("replicas", True, "at least 3 replicas"),
        ("readiness_path", 7, "readiness_path"),
    )
    for field, value, message in invalid_values:
        invalid = replace(
            plan,
            **{field: value},
        )
        assert any(
            message in failure
            for failure in policy_violations(invalid)
        )


def test_red_fixture_is_one_policy_violation() -> None:
    plan = load_plan(BEFORE)

    assert policy_violations(plan) == [
        "max_unavailable must be 0 or 1",
    ]


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "revision",
            "sample-api:1.7.2",
            "observed revision does not match plan",
        ),
        (
            "ready_replicas",
            5,
            "not all planned replicas are ready",
        ),
        (
            "total_replicas",
            5,
            "observed replica total does not match",
        ),
        (
            "error_rate",
            0.021,
            "observed error rate exceeds limit",
        ),
        (
            "request_succeeded",
            False,
            "representative request failed",
        ),
    ],
)
def test_verification_rejects_failed_postcondition(
    field: str,
    value: str | int | float | bool,
    message: str,
) -> None:
    plan = load_plan(CONFIG)
    values: dict[str, str | int | float | bool] = {
        "revision": plan.proposed_revision,
        "ready_replicas": plan.replicas,
        "total_replicas": plan.replicas,
        "error_rate": 0.008,
        "request_succeeded": True,
    }
    values[field] = value
    observed = Observation(**values)

    assert message in verification_failures(plan, observed)


def test_verification_accepts_target_and_rejects_bad_rates(
) -> None:
    plan = load_plan(CONFIG)
    observed = Observation(
        revision=plan.proposed_revision,
        ready_replicas=plan.replicas,
        total_replicas=plan.replicas,
        error_rate=0.008,
        request_succeeded=True,
    )

    assert verification_failures(plan, observed) == []
    for invalid in (
        float("nan"),
        -0.001,
        1.1,
        None,
        True,
    ):
        bad = replace(
            observed,
            error_rate=invalid,
        )
        assert verification_failures(plan, bad) == [
            "observed error rate is invalid",
        ]
