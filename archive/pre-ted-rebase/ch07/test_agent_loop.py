import pytest

from agent_loop import run_agent


def test_returns_final_text_without_a_tool_call():
    def ask_model(history):
        assert history == [
            {"role": "user", "content": "inspect"},
        ]
        return {"content": "complete"}

    result = run_agent(
        "inspect",
        ask_model,
        lambda name, args: None,
        {"read"},
        1,
    )

    assert result == "complete"


def test_runs_an_allowed_tool_and_records_observation():
    replies = iter([
        {
            "content": "",
            "tool_call": {
                "name": "read",
                "args": {"path": "validator.py"},
            },
        },
        {"content": "checked"},
    ])
    histories = []
    tool_calls = []

    def ask_model(history):
        histories.append(list(history))
        return next(replies)

    def run_tool(name, args):
        tool_calls.append((name, args))
        return "file contents"

    result = run_agent(
        "inspect",
        ask_model,
        run_tool,
        {"read"},
        2,
    )

    assert result == "checked"
    assert tool_calls == [
        ("read", {"path": "validator.py"}),
    ]
    assert histories[-1][-1] == {
        "role": "tool",
        "name": "read",
        "content": "file contents",
    }


def test_rejects_a_tool_outside_the_allowlist():
    def ask_model(history):
        return {
            "content": "",
            "tool_call": {
                "name": "write",
                "args": {},
            },
        }

    with pytest.raises(PermissionError, match="write"):
        run_agent(
            "inspect",
            ask_model,
            lambda name, args: None,
            {"read"},
            1,
        )


def test_raises_when_the_step_budget_is_spent():
    def ask_model(history):
        return {
            "content": "",
            "tool_call": {
                "name": "read",
                "args": {},
            },
        }

    with pytest.raises(RuntimeError, match="step budget spent"):
        run_agent(
            "inspect",
            ask_model,
            lambda name, args: "observation",
            {"read"},
            1,
        )
