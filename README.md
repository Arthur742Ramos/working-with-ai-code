# Working with AI: companion code

This public companion contains twelve runnable chapter packages and an
Appendix A parser trial. Each chapter guide covers its dependencies, checks,
captured-session replay, and limits. [PRINTED_EXAMPLES.md](PRINTED_EXAMPLES.md)
maps the current teaching additions to their source.

This repository was maintained with help from AI tools: Claude Code, GitHub
Copilot, and Codex. The human author reviewed the published work and remains
responsible for its content and maintenance.

| Chapter | Package guide |
|---|---|
| Chapter 1: Working with AI: from magic to engineering | [README](ch01/README.md) |
| Chapter 2: Contracts that produce checkable work | [README](ch02/README.md) |
| Chapter 3: Conversations that converge | [README](ch03/README.md) |
| Chapter 4: Plans you can review and redirect | [README](ch04/README.md) |
| Chapter 5: Diagnosing failure under uncertainty | [README](ch05/README.md) |
| Chapter 6: Roles that produce independent artifacts | [README](ch06/README.md) |
| Chapter 7: Bounded agents and orchestration | [README](ch07/README.md) |
| Chapter 8: From checks to evaluations | [README](ch08/README.md) |
| Chapter 9: Context engineering: data, tools, and trust | [README](ch09/README.md) |
| Chapter 10: Software engineering: from idea to review-ready code | [README](ch10/README.md) |
| Chapter 11: Taking AI-assisted changes to production | [README](ch11/README.md) |
| Chapter 12: Measuring and governing AI-assisted work | [README](ch12/README.md) |
| Appendix A: Comparing agentic tools | [README](appA/README.md) |

## Run the checks

Use Python 3.11 or newer and install the chapter's listed requirements in an
isolated environment when needed. Run checks from the chapter directory; for
example, from the repository root:

```sh
(cd ch02 && python3 -m pytest -q test_pr_generator.py)
(cd ch10 && python3 -m pytest -q tests)
(cd ch10/batch_case && python3 -m pytest -q tests)
(cd ch12 && python3 -m unittest -v test_workflow_metrics)
python3 appA/verify_trial.py
```

Follow the chapter guides for the other green suites and the non-recording
capture replays. Chapters 1 and 5 use explicit test scripts; do not recursively
collect every chapter or a capture's intentionally red before-state with one
pytest command. Appendix A's starting fixture is also intentionally red: its
verifier checks the expected failure and a temporary reference repair without
modifying the printed fixture.

The deterministic examples need no live model or production service. Optional
provider adapters have separate setup instructions in their chapter guides.
The code is licensed under the [MIT License](LICENSE).
