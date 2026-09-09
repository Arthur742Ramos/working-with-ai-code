# Strict-float capture parity

Stage: `complete_independently_reviewed`; independent review: `completed`; package status: `Pass`. The prior failed review and its blocking findings remain preserved as historical evidence. The attributable read-only re-review passed canonical and mirrored package replay, checksums, isolation, cleanup, policy discrimination, publication parity, and all 13 top-level tests. The shared publication ledger was `Pending` during that read-only review and later moved to `Pass` during aggregate reconciliation. That external transition did not change the package verdict.

| Printed or captured item | Maintained source | Capture status |
|---|---|---|
| Listing 7.1, bounded tool-use loop | Package root `agent_loop.py` | Complete implementation matches the staged listing; outside this strict-float capture |
| Validator filename and before excerpt | `before/validator.py` | Reconstructed provenance labeled and checksum-verified |
| Focused behavior check | `tests/focused_test.py` | Checksum-verified; distinguishes one accepted built-in float from four invalid values, including a float subclass |
| Red command | `metadata.json` and `session.md` | Recorded |
| Red output | `evidence/focused-red.txt` | Genuine raw command output retained unchanged |
| Red exit status | `evidence/focused-red.exit` | Genuine exit `1` retained unchanged |
| Agent observation and one-sentence plan | `session.md` | Grounded in staged source, test, and red result |
| Approval basis and selected policy | `session.md` and `metadata.json` | Agent selected exact built-in semantics under standing direction; no false option attribution |
| Actual action sequence | `evidence/agent-actions.jsonl` | Origin session actions preserved in order |
| Listing 7.2, strict smallest float registration | `patches/strict_float_validator.diff` | Exact machine-generated one-line production diff printed byte-for-byte, including two trailing blank context lines |
| Focused green output | `evidence/focused-green.txt` | Genuine output, exit `0` |
| Broader green command | Package-local `tests/test_validator.py` copied beside the disposable after-state | Eight origin test bodies plus one post-review subclass-policy test exercised without repository-root access |
| Broader green output | `evidence/broader-green.txt` | Genuine nine-test pytest output with elapsed time normalized, exit `0` |
| Origin canonical support green | `evidence/canonical-support-green.txt` | Historical origin artifact retained by checksum; isolated replay does not execute its old path |
| Package immutability during replay | Before and after package-local checksums in `metadata.json` | Final `validator.py` and strengthened `test_validator.py` remain unchanged |
| Float-subclass policy | `tests/focused_test.py`, `tests/test_validator.py`, and package root `test_validator.py` | Focused, broader, and final-package layers explicitly reject a `float` subclass |
| `isinstance` adversarial check | `run_capture.py` | Replay widens only the disposable predicate and requires both capture layers to fail on the subclass case |
| Cleanup invariant | `run_capture.py` | Temporary `.work-*` state is removed on success or failure; replay fails if residue remains |
| Active review state | `metadata.json`, `README.md`, and `evidence/independent-review.md` | First review `Fail` retained as history; active state is `complete_independently_reviewed`, `completed`, and `Pass` with a checksum-bound receipt |
| Human policy boundary | `README.md`, `session.md`, and `metadata.json` | Future widening or coercion remains a human-owned contract change |
| Table 7.1, stop conditions | Staged chapter prose | Conceptual decision table; no executable package artifact |
| Table 7.2, workflow choice | Staged chapter prose | Conceptual decision table; no executable package artifact |
| Table 7.3, worker contracts | Staged chapter prose | Conceptual decision table; no executable package artifact |
| Table 7.4, failure routing | Staged chapter prose | Conceptual decision table; no executable package artifact |
| Table 7.5, autonomy postures | Staged chapter prose | Conceptual decision table; no executable package artifact |

## Intentional excerpting and normalization

The before fixture is intentionally reconstructed rather than claimed as a historical byte copy. The session narrative condenses tool activity, while `evidence/agent-actions.jsonl` preserves the actual action order. Focused outputs are stored verbatim. Pytest color, external plugin loading, bytecode, and cache output are disabled; only elapsed time is normalized to `<TIME>`. The printed focused-green command uses `<WORK>/validator.py` for the runner's randomized package-local `.work-*` directory; the executable command passes that concrete temporary path.

The localized broader suite preserves the eight origin test bodies and adds one post-review subclass-policy test. Its stale section reference was corrected to Listing 7.2. Because the test harness changed intentionally, the five-case focused and nine-test broader evidence was genuinely rerun and the chapter counts were updated. The eight-test canonical-support artifact remains labeled origin history and is not regenerated.

## Replay isolation and origin provenance

`metadata.json` keeps the repository commit, original canonical checksums, canonical support output, and original action record as archival provenance. `run_capture.py` does not derive a repository root, resolve another chapter or canonical code directory, or run those historical paths. It verifies and executes only files inside the copied Chapter 7 package.

## Chapter integration boundary

The staged Chapter 7 session maps the five-case red command and output, exact Listing 7.2 diff, five-case focused green, nine-test broader green, evidence boundary, and human-owned policy decision to this package. Reader-facing prose does not expose this private capture path or direct readers to external code. The independent parity re-review passed and the package is `Pass`. The shared ledger was `Pending` during package review; aggregate reconciliation later moved its publication gate to `Pass` without changing this certification.
