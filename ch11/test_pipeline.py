import pipeline
from pipeline import Stage


def test_pipeline_stops_at_first_failure(
    monkeypatch,
    capsys,
) -> None:
    stages = (
        Stage("compile", ()),
        Stage("policy", ()),
        Stage("apply", ()),
    )
    results = {
        "compile": 0,
        "policy": 2,
        "apply": 0,
    }
    observed: list[str] = []

    def fake_run_stage(stage: Stage) -> int:
        observed.append(stage.name)
        return results[stage.name]

    with monkeypatch.context() as context:
        context.setattr(
            pipeline,
            "run_stage",
            fake_run_stage,
        )

        assert pipeline.run_pipeline(stages) == 2
        assert observed == ["compile", "policy"]
        assert capsys.readouterr().out == (
            "blocked_at=policy\n"
        )

    assert [stage.name for stage in pipeline.STAGES] == [
        "compile",
        "test",
        "plan-and-policy",
    ]
    assert not {
        "apply",
        "verify",
        "recovery",
    }.intersection(stage.name for stage in pipeline.STAGES)

    def completed_process(*args, **kwargs):
        return pipeline.subprocess.CompletedProcess(
            args[0],
            7,
        )

    monkeypatch.setattr(
        pipeline.subprocess,
        "run",
        completed_process,
    )
    assert pipeline.run_stage(
        Stage("test", ("test-command",))
    ) == 7
    captured = capsys.readouterr()
    assert captured.out == "== test ==\n"
    assert captured.err == ""

    def missing_process(*args, **kwargs):
        raise FileNotFoundError("test-command")

    monkeypatch.setattr(
        pipeline.subprocess,
        "run",
        missing_process,
    )
    assert pipeline.run_pipeline(
        (
            Stage("compile", ("missing-command",)),
            Stage("test", ("later-command",)),
        )
    ) == pipeline.LAUNCH_FAILURE
    captured = capsys.readouterr()
    assert captured.out == (
        "== compile ==\n"
        "blocked_at=compile\n"
    )
    assert captured.err == "tool_error=compile\n"
