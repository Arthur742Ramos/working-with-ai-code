from dataclasses import replace
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

from deployment_guard import (
    Observation,
    load_plan,
    policy_violations,
    verification_failures,
)


ROOT = Path(__file__).parent
CONFIG = ROOT / "deployment.json"
BEFORE = (
    ROOT
    / "captures"
    / "deployment_policy_value"
    / "before"
    / "deployment.json"
)


def _run_cli(
    *arguments: str | Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "deployment_guard.py"),
            *(str(argument) for argument in arguments),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_production_config_is_safe() -> None:
    plan = load_plan(CONFIG)

    assert policy_violations(plan) == []
    invalid_values = (
        ("batch_size", True, "batch_size"),
        ("max_unavailable", True, "max_unavailable"),
        ("max_unavailable", False, "max_unavailable"),
        ("replicas", True, "at least 3 replicas"),
        ("readiness_path", 7, "readiness_path"),
        ("error_rate_limit", True, "error_rate_limit"),
        ("error_rate_limit", "0.02", "error_rate_limit"),
        ("error_rate_limit", None, "error_rate_limit"),
        ("error_rate_limit", [], "error_rate_limit"),
        (
            "error_rate_limit",
            float("nan"),
            "error_rate_limit",
        ),
        (
            "error_rate_limit",
            float("inf"),
            "error_rate_limit",
        ),
        (
            "error_rate_limit",
            10**400,
            "error_rate_limit",
        ),
        ("error_rate_limit", 0.021, "error_rate_limit"),
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
            "ready_replicas",
            6.0,
            "observed ready replicas are invalid",
        ),
        (
            "total_replicas",
            5,
            "observed replica total does not match",
        ),
        (
            "total_replicas",
            6.0,
            "observed replica total is invalid",
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


def test_plan_cli_prints_approval_surface() -> None:
    completed = _run_cli("plan", CONFIG)

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout == (
        "service=sample-api\n"
        "environment=production\n"
        "revision=sample-api:1.7.2 -> "
        "sample-api:1.8.0\n"
        "rollout=batch 2, max unavailable 1\n"
        "health=/ready, error rate <= 0.020\n"
        "rollback=sample-api:1.7.2\n"
        "policy=PASS\n"
    )


def test_plan_cli_blocks_malformed_rate(
    tmp_path: Path,
) -> None:
    data = json.loads(CONFIG.read_text())
    data["health"]["error_rate_limit"] = "0.02"
    config = tmp_path / "deployment.json"
    config.write_text(json.dumps(data))

    completed = _run_cli("plan", config)

    assert completed.returncode == 2
    assert completed.stderr == ""
    assert "error rate <= '0.02'" in completed.stdout
    assert "policy=BLOCK" in completed.stdout
    assert (
        "violation=error_rate_limit must be > 0 and <= 0.02"
        in completed.stdout
    )


def test_plan_cli_bounds_large_rate_output(
    tmp_path: Path,
) -> None:
    data = json.loads(CONFIG.read_text())
    data["health"]["error_rate_limit"] = 10**400
    config = tmp_path / "deployment.json"
    config.write_text(json.dumps(data))

    completed = _run_cli("plan", config)

    assert completed.returncode == 2
    assert completed.stderr == ""
    assert len(completed.stdout) < 500
    assert "policy=BLOCK" in completed.stdout


def test_plan_cli_preserves_precise_rate(
    tmp_path: Path,
) -> None:
    data = json.loads(CONFIG.read_text())
    rate = math.nextafter(0.02, 0.0)
    data["health"]["error_rate_limit"] = rate
    config = tmp_path / "deployment.json"
    config.write_text(json.dumps(data))

    completed = _run_cli("plan", config)

    assert completed.returncode == 0
    assert f"error rate <= {rate!r}" in completed.stdout


def test_plan_cli_escapes_multiline_fields(
    tmp_path: Path,
) -> None:
    data = json.loads(CONFIG.read_text())
    data["service"] = "sample-api\npolicy=PASS"
    config = tmp_path / "deployment.json"
    config.write_text(json.dumps(data))

    completed = _run_cli("plan", config)

    assert completed.returncode == 0
    assert "service=sample-api\\x0apolicy=PASS" in (
        completed.stdout
    )
    assert completed.stdout.splitlines().count(
        "policy=PASS"
    ) == 1


def test_verify_cli_rejects_invalid_plan(
    tmp_path: Path,
) -> None:
    data = json.loads(CONFIG.read_text())
    data["health"]["error_rate_limit"] = "0.02"
    config = tmp_path / "deployment.json"
    config.write_text(json.dumps(data))

    completed = _run_cli(
        "verify",
        config,
        ROOT / "observation.json",
    )

    assert completed.returncode == 3
    assert completed.stderr == ""
    assert completed.stdout == (
        "verification=FAIL\n"
        "failure=plan policy: "
        "error_rate_limit must be > 0 and <= 0.02\n"
    )


def test_verify_cli_prints_passing_verdict() -> None:
    completed = _run_cli(
        "verify",
        CONFIG,
        ROOT / "observation.json",
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout == "verification=PASS\n"
