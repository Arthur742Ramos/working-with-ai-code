# Boolean-as-integer capture parity ledger

Status: one Claude Code session captured the tester and implementer artifacts; a later maintained integration review recorded the verifier-role receipt. A separate independent canonical review certifies the final Chapter 6 package.

## Role artifact map

| Role | Printed artifact | Maintained package source | Parity status |
|---|---|---|---|
| Tester | Tester contract, inspection, focused red, one-sentence plan, and policy boundary | `session.md` from Human contract through One-sentence strict-smallest-change plan, `tests/test_bool_is_not_accepted_as_int.py`, and `evidence/focused-red.*` | Contract is reconstructed and labeled; inspection, output, status, observation, and plan are contemporaneous within the captured Claude Code session |
| Implementer | Replay statement, exact one-line diff, focused green, and broader green | `session.md` from Approval basis through Agent evidence-boundary statement, `patches/strict-int.patch`, and focused plus broader green evidence | The same Claude Code session produced the machine-generated diff and stored outputs; pytest timing alone is normalized |
| Verifier | Maintained integration-review receipt with replay, red, minimality, green, record, immutability, blocker, and repair fields | `metadata.json` at `integration_review_receipt.verdict` | The later receipt matches the printed JSON fields and values; it is not a separate verifier transcript or the independent canonical certification |

## Chapter listing map

| Chapter item | Maintained package source | Intentional difference |
|---|---|---|
| Listing 6.1, coder implementation before independent testing | `before/validator.py` for before-state behavior; top-level `validator.py` for presentation formatting | The listing is a presentation composite: it uses the top-level annotated formatting with the captured permissive `int` predicate. The copied before fixture retains its capture-era module documentation and compact recursion formatting. The top-level implementation remains green with `type(value) is int`. |
| Listing 6.2, contract-derived maintained-suite excerpt | Four functions in top-level `test_validator.py` | The chapter prints the complete functions without modification. |
| Listings 6.3 and 6.4, independent focused test | Top-level `test_bool_is_not_accepted_as_int.py` | The capture copy under `tests/` is behaviorally identical and emits the same output, but it retains the original capture docstring and formats the usage message on one line. |
| Listing 6.5, thin command-line runner | Top-level `cli.py` | No intentional code difference. |

## Evidence and command map

| Printed or session item | Maintained source | Parity status |
|---|---|---|
| Printed focused red command: `python3 test_bool_is_not_accepted_as_int.py validator.py` | Executable capture command in `session.md` and `metadata.json`: `python3 captures/boolean_as_integer_role_handoff/tests/test_bool_is_not_accepted_as_int.py captures/boolean_as_integer_role_handoff/before/validator.py`; `evidence/focused-red.*` | The chapter removes internal staging prefixes and preserves the command role, output, and exit status `1` |
| One-sentence plan and selected policy | `session.md` and `metadata.json` | Recorded before the disposable edit; the agent selected exact semantics under standing delegation while policy ownership remains human |
| Exact applied diff | `patches/strict-int.patch` | Machine-generated unified diff with one changed production line |
| Printed focused green command: `python3 test_bool_is_not_accepted_as_int.py validator.py` | Executable capture command in `session.md` and `metadata.json`: `python3 captures/boolean_as_integer_role_handoff/tests/test_bool_is_not_accepted_as_int.py captures/boolean_as_integer_role_handoff/.work/validator.py`; `evidence/focused-green.*` | The same printed command shape now targets the disposable after state; output and exit status `0` are unchanged |
| Broader test behavior | Top-level `test_validator.py`, copied into `.work/` | Eight tests protect the focused behavior and neighboring validator behavior |
| Printed broader green command: `python3 -m pytest -q test_validator.py` | Historical capture command preserved in `session.md` and `metadata.json`: `cd captures/boolean_as_integer_role_handoff/.work && python3 -m pytest -q test_validator.py`; hardened replay command in `metadata.json`: the same command with `-p no:cacheprovider`; `evidence/broader-green.*` | The replay-only cache control does not change collected tests or output. The chapter omits internal controls and the working-directory prefix; ANSI color is removed and elapsed timing becomes `<TIME>s`, while the eight-pass count and exit status remain unchanged. |
| Final green implementation | Top-level `validator.py` | Uses exact built-in `int` semantics and remains unchanged during replay |
| Top-level focused green check | Top-level `test_bool_is_not_accepted_as_int.py` | Runs separately from pytest and matches Listings 6.3 and 6.4 together |
| Top-level test discovery boundary | Top-level `pytest.ini` | `python3 -m pytest -q` collects only `test_validator.py`; capture internals remain replay-only |
| Thin runner | Top-level `cli.py` | Matches Listing 6.5 |
| Non-recording replay | `run_capture.py` | Cleans stale work before preflight, verifies that the resolved evidence root remains under the capture package, recreates and compares red, patch, focused green, broader green, evidence checksums, all top-level executable checksums, and the independent-review receipt without rewriting evidence; disables pytest caching so replay leaves no package-root `.pytest_cache/` |

## Origin and isolation

The session originated from the earlier maintained role-relay validator at the repository commit recorded in `metadata.json`. The final package removes the retired chapter assignment and original support path from copied documentation and the fixture label. It preserves the origin commit, reconstructed-fixture disclosure, coding-agent version, policy selection history, and evidence checksums.

All commands in the final package are relative to the Chapter 6 package root. `run_capture.py` derives its paths from its own location, copies only local files into `.work/`, and checks only local artifacts. It does not import repository-root code, read another chapter, or require the original capture location.

## Review gates

The verifier role inside the printed three-role handoff is represented by the later integration-review receipt stored in `metadata.json` under `integration_review_receipt.verdict`. It records acceptance of the replayed handoff but is not a separate verifier transcript.

The package-level independent canonical certification is stored separately at `evidence/independent-review.md`. Active state is `complete_independently_reviewed`, review status is `completed`, and verdict is `Pass`. `run_capture.py` rejects that completed stage if the active review is pending, its verdict is not `Pass`, the resolved evidence root escapes the capture package, or the package-local receipt is missing, external, or checksum-invalid. It removes stale `.work/` state before preflight and after every success or failure, and the cache-disabled pytest replay leaves no package-root `.pytest_cache/`.

The shared session ledger mapped this canonical package as Pending during read-only package review, then moved to Pass during aggregate publication-control reconciliation. That external control history is separate from package certification.

Internal ledgers may name package-local paths. The reader-facing chapter remains self-contained and does not direct readers to this support package.
