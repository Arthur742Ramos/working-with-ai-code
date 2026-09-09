# Working with AI: current chapter packages

This checkout provides the book's twelve runnable chapter packages. Each chapter README names its maintained commands, captured-session replay, dependencies, and limits. [PRINTED_EXAMPLES.md](PRINTED_EXAMPLES.md) maps the revised teaching additions.

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

Run each chapter's checks from its own directory. The packages have different dependencies and independent test-module names; use their stated commands rather than collecting every chapter in one pytest invocation. Each captured session has a dedicated replay command that exercises its intentional red state before verifying the repair.

Chapter 10 retains its established public capture verifier while its application code and new printed example match the book. The private manuscript snapshot and its authoring-only verifier are not part of this public distribution.

The previous listing-oriented companion is preserved under [archive/pre-ted-rebase](archive/pre-ted-rebase/README.md). It is historical material; current verification uses the top-level ch01 through ch12 packages. No live model or production service is needed by the deterministic examples. Optional provider adapters require separate setup described in their chapter guides.
