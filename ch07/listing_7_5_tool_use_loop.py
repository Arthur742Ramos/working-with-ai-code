"""Listing 7.5: A minimal tool-use loop.

This is an illustrative snippet, not a runnable program. It references
names that are intentionally undefined here (`chat`, `run`, `MAX_STEPS`,
and `as_tool_result`) because the point is the shape of the loop, not a
working harness. It is not imported by the test suite and will not run on
its own.
"""

TOOLS = {
    "read_file": lambda path: open(path).read(),
    "run_tests": lambda: run("pytest -q"),
}


def agent(goal, messages):
    messages.append({"role": "user", "content": goal})
    for _ in range(MAX_STEPS):              #A
        reply = chat(messages, tools=TOOLS)
        if reply.tool_call is None:
            return reply.text               #B
        name = reply.tool_call.name
        args = reply.tool_call.args
        result = TOOLS[name](**args)        #C
        messages.append(
            as_tool_result(name, result)
        )
    raise RuntimeError("step budget spent")  #D
