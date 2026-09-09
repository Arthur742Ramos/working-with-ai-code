from pathlib import Path
from agent_loop import run_agent


def scripted_model(history):
    if len(history) == 1:
        return {"role": "assistant", "content": "",
                "tool_call": {"name": "read_contract",
                              "args": {}}}
    return {"role": "assistant",
            "content": history[-1]["content"]}


def run_tool(name, args):
    if name != "read_contract" or args:
        raise PermissionError("unsupported request")
    return Path("contract.txt").read_text().strip()


result = run_agent(
    "Read the accepted integer policy.",
    scripted_model, run_tool, {"read_contract"}, 2,
)
assert result == "int excludes bool"
print(result)
