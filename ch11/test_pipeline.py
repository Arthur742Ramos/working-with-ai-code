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

    monkeypatch.setattr(
        pipeline,
        "run_stage",
        fake_run_stage,
    )

    assert pipeline.run_pipeline(stages) == 2
    assert observed == ["compile", "policy"]
    assert capsys.readouterr().out == (
        "blocked_at=policy\n"
    )
