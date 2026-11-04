import pytest

from agent_loop import run_agent
from issue_injection import ISSUE, scripted_model


def run_with(issue, allowed):
    executed = []

    def tool(name, args):
        executed.append(name)
        return issue if name == "read_issue" else "simulated"

    return executed, lambda: run_agent(
        "Summarize the issue", scripted_model, tool, allowed, 2
    )


def test_injected_message_is_denied_before_the_tool_runs():
    executed, run = run_with(ISSUE, {"read_issue"})
    with pytest.raises(PermissionError, match="send_message"):
        run()
    assert executed == ["read_issue"]


def test_benign_issue_returns_without_requesting_a_message():
    executed, run = run_with("Export failed.", {"read_issue"})
    assert run() == "No action requested."
    assert executed == ["read_issue"]


def test_control_reaches_the_fake_tool_if_explicitly_allowed():
    executed, run = run_with(ISSUE, {"read_issue", "send_message"})
    with pytest.raises(RuntimeError, match="step budget spent"):
        run()
    assert executed == ["read_issue", "send_message"]
