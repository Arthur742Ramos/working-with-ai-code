"""Checks for MCP capability selection and action containment."""

import pytest

from mcp_policy import MCPHost, Posture, Prompt, Resource, Tool


def test_host_selects_resources_and_prompts():
    host = MCPHost(
        resources=[Resource("issue", lambda: {"id": 7})],
        prompts=[
            Prompt(
                "summarize",
                lambda args: f"Summarize {args['topic']}",
            )
        ],
    )

    assert host.read_resource("issue") == {"id": 7}
    assert host.render_prompt(
        "summarize", {"topic": "incident"}
    ) == "Summarize incident"


def test_read_tool_runs_without_apply_approval():
    host = MCPHost(tools=[
        Tool(
            "lookup",
            Posture.READ,
            lambda args: {"issue": args["issue"]},
        )
    ])

    assert host.call_tool("lookup", {"issue": 7}) == {"issue": 7}


def test_propose_tool_returns_reviewable_action():
    host = MCPHost(tools=[
        Tool(
            "draft_alert",
            Posture.PROPOSE,
            lambda args: {
                "target": args["target"],
                "text": args["text"],
            },
            allowed_targets=frozenset({"team-alerts"}),
        )
    ])

    assert host.call_tool(
        "draft_alert",
        {"target": "team-alerts", "text": "failed"},
    ) == {"target": "team-alerts", "text": "failed"}


def test_apply_tool_requires_explicit_approval():
    calls = []
    host = MCPHost(tools=[
        Tool(
            "send",
            Posture.APPLY,
            lambda args: calls.append(args),
            allowed_targets=frozenset({"team-alerts"}),
            communicates_externally=True,
        )
    ])

    with pytest.raises(PermissionError, match="explicit approval"):
        host.call_tool(
            "send",
            {"target": "team-alerts", "text": "failed"},
        )
    assert calls == []

    host.call_tool(
        "send",
        {"target": "team-alerts", "text": "failed"},
        approved=True,
    )
    assert calls == [
        {"target": "team-alerts", "text": "failed"}
    ]


def test_tool_target_must_be_allowlisted():
    host = MCPHost(tools=[
        Tool(
            "send",
            Posture.APPLY,
            lambda args: args,
            allowed_targets=frozenset({"team-alerts"}),
        )
    ])

    with pytest.raises(PermissionError, match="not allowlisted"):
        host.call_tool(
            "send",
            {"target": "external-recipient"},
            approved=True,
        )


def test_one_tool_cannot_complete_the_lethal_trifecta():
    with pytest.raises(ValueError, match="lethal trifecta"):
        Tool(
            "unsafe",
            Posture.APPLY,
            lambda args: args,
            reads_private_data=True,
            consumes_untrusted_content=True,
            communicates_externally=True,
        )


def test_one_host_cannot_compose_the_lethal_trifecta():
    tools = [
        Tool(
            "private_lookup",
            Posture.READ,
            lambda args: args,
            reads_private_data=True,
        ),
        Tool(
            "fetch_page",
            Posture.READ,
            lambda args: args,
            consumes_untrusted_content=True,
        ),
        Tool(
            "send_alert",
            Posture.APPLY,
            lambda args: args,
            communicates_externally=True,
        ),
    ]

    with pytest.raises(ValueError, match="one host cannot combine"):
        MCPHost(tools=tools)


def test_capability_names_are_unique():
    with pytest.raises(ValueError, match="names must be unique"):
        MCPHost(resources=[
            Resource("issue", lambda: 1),
            Resource("issue", lambda: 2),
        ])
