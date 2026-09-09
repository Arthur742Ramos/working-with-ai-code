"""Model MCP capabilities and host-owned action policy."""

from dataclasses import dataclass
from enum import Enum


class Posture(str, Enum):
    READ = "read"
    PROPOSE = "propose"
    APPLY = "apply"


@dataclass(frozen=True)
class Resource:
    name: str
    load: object


@dataclass(frozen=True)
class Prompt:
    name: str
    render: object


@dataclass(frozen=True)
class Tool:
    name: str
    posture: Posture
    run: object
    allowed_targets: frozenset[str] = frozenset()
    reads_private_data: bool = False
    consumes_untrusted_content: bool = False
    communicates_externally: bool = False

    def __post_init__(self):
        lethal_trifecta = (
            self.reads_private_data
            and self.consumes_untrusted_content
            and self.communicates_externally
        )
        if lethal_trifecta:
            raise ValueError(
                "one tool cannot combine the lethal trifecta"
            )


class MCPHost:
    """Keep capability selection and approval outside the model."""

    def __init__(self, *, resources=(), prompts=(), tools=()):
        tools = tuple(tools)
        self._reject_lethal_toolset(tools)
        self.resources = self._index(resources)
        self.prompts = self._index(prompts)
        self.tools = self._index(tools)

    @staticmethod
    def _reject_lethal_toolset(tools):
        has_private_data = any(
            tool.reads_private_data for tool in tools
        )
        has_untrusted_content = any(
            tool.consumes_untrusted_content for tool in tools
        )
        has_external_communication = any(
            tool.communicates_externally for tool in tools
        )
        if (
            has_private_data
            and has_untrusted_content
            and has_external_communication
        ):
            raise ValueError(
                "one host cannot combine the lethal trifecta"
            )

    @staticmethod
    def _index(items):
        items = tuple(items)
        indexed = {item.name: item for item in items}
        if len(indexed) != len(items):
            raise ValueError("capability names must be unique")
        return indexed

    def read_resource(self, name):
        return self.resources[name].load()

    def render_prompt(self, name, arguments):
        return self.prompts[name].render(dict(arguments))

    def call_tool(self, name, arguments, *, approved=False):
        tool = self.tools[name]
        arguments = dict(arguments)
        target = arguments.get("target")
        if tool.allowed_targets and target not in tool.allowed_targets:
            raise PermissionError("tool target is not allowlisted")
        if tool.posture is Posture.APPLY and not approved:
            raise PermissionError("apply tools require explicit approval")
        return tool.run(arguments)
