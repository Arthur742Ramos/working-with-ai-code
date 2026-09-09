"""Focused test for a schema-valid rollout policy value."""

import json
from pathlib import Path

from deployment_guard import load_plan, policy_violations


CONFIG = Path(__file__).with_name("deployment.json")


def _schema_accepts_max_unavailable(data: dict) -> bool:
    value = data["rollout"]["max_unavailable"]
    replicas = data["replicas"]
    return (
        type(value) is int
        and type(replicas) is int
        and 0 <= value <= replicas
    )


def test_schema_valid_deployment_satisfies_policy() -> None:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))

    assert _schema_accepts_max_unavailable(data)
    plan = load_plan(CONFIG)
    assert plan.max_unavailable == data["rollout"]["max_unavailable"]
    assert policy_violations(plan) == []
