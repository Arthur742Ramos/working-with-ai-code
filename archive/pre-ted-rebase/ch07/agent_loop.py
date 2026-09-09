def run_agent(goal, ask_model, run_tool,
              allowed_tools, max_steps):
    history = [{"role": "user", "content": goal}]

    for _ in range(max_steps):              # A
        reply = ask_model(history)
        call = reply.get("tool_call")
        if call is None:
            return reply["content"]         # B

        name = call["name"]
        if name not in allowed_tools:
            raise PermissionError(name)     # C

        history.append(reply)
        result = run_tool(name, call["args"])
        history.append({
            "role": "tool",
            "name": name,
            "content": result,
        })

    raise RuntimeError("step budget spent") # D
