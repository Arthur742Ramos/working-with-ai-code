# Chapter 7 — Bounded agents and orchestration

A minimal bounded tool-use loop (allow-list plus a step budget) alongside a
strict-`float` type added to the JSON config validator through an
independent inspect-red-fix cycle.

- **`agent_loop.py`** — Listing 7.1: A minimal bounded tool-use loop
- **`validator.py`** — Listing 7.2 target: the maintained green validator with strict `float` support
- **`test_agent_loop.py`** — Behavior checks for the loop's return, tool routing, allow-list, and step budget
- **`test_validator.py`** — The nine maintained validator checks, including the strict-float cases
- **`cli.py`** — A thin command-line runner for the validator
- **`fixtures/`** — `schema.json`, `config-valid.json`, and `config-invalid.json` for the CLI
- **`captures/before/validator.py`** — the red before-state validator with no `float` type
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

## Setup and checks

Run from this directory (needs only `pytest`):

```bash
python3 -m pytest -q
python3 cli.py --schema fixtures/schema.json --config fixtures/config-valid.json
python3 cli.py --schema fixtures/schema.json --config fixtures/config-invalid.json
```

`python3 -m pytest -q` reports **13 passed** (four loop checks plus nine
validator checks). The valid CLI command prints `ok` and exits `0`; the
invalid one reports `service.port: expected int` and
`service.ratio: expected float` and exits `1`.

## Listing map

- **Listing 7.1** is `agent_loop.py`: `run_agent` bounds the model with an
  allowed-tool set and a fixed step budget, returning final text, raising
  `PermissionError` on an out-of-policy tool, and `RuntimeError` when the
  budget is spent. The inline `# A`–`# D` markers match the printed callouts.
- **Listing 7.2** is the one-line registration of a strict `float` predicate
  (`type(value) is float`) in the validator's `CHECKS`. The maintained
  `validator.py` is the green after-state; `captures/before/validator.py` is
  the red before-state without the `float` entry.

## Red-to-green capture

See [`captures/README.md`](captures/README.md) to reproduce the strict-float
red result and the one-line repair.

## Limits

A step budget is a stop condition, not a sandbox: it bounds how long a loop
runs, not which files, commands, or network targets a tool may reach. The
loop's permission check stops at the tool name; a production harness should
prefer typed tools or validated argument vectors over model-authored text.

See the [main README](../README.md) for setup instructions.
