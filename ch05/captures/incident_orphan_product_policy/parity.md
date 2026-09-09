# Parity map

Stage: `complete_independently_reviewed`; independent review: `completed`; status: `Pass`.

This map binds the verified session to the isolated final Chapter 5 package and to the staged Chapter 5 publication surface. The retained before fixture records historical origin; no executable check reaches outside this package.

| Session or publication item | Package-local maintained source | Capture artifact | Status |
|---|---|---|---|
| Final production filename | Top-level `server.py` | `before/server.py` plus `patches/missing-product-policy.diff` | Patch reproduces the top-level green file byte for byte |
| Deterministic seed | Top-level `seed.py` | `before/seed.py` | Byte-for-byte verified |
| Focused maintained test | Top-level `tests/test_orphan_policy.py` | `tests/test_orphan_policy.py` | Byte-for-byte verified; genuine red and focused green |
| Broader maintained test | Top-level `tests/test_orphan_policy_broader.py` | `tests/test_orphan_policy_broader.py` | Byte-for-byte verified; valid summary and API boundary |
| Intended top-level suite | Two explicit test scripts from the final package root | Top-level `README.md` | Capture internals are not recursively collected as current tests |
| Focused test name | `test_seeded_orphan_uses_explicit_missing_product_policy` | `tests/test_orphan_policy.py` | Exact |
| Focused capture command | `python3 tests/test_orphan_policy.py .work` | `metadata.json` and `session.md` | Exact |
| Focused final command | `python3 tests/test_orphan_policy.py` | Top-level `README.md` and replay | Package-local green |
| Red output | Deterministic orphan plus expected and observed exception contrast | `evidence/focused-red.txt` | Raw, no normalization |
| Red exit status | `1` | `evidence/focused-red.exitstatus` | Raw |
| One-sentence plan | Named exception, pre-price guard, fail-closed mapping | `session.md` | Recorded before final patch |
| Approval basis | Standing author direction plus approved fail-closed behavior | `session.md` | Author did not name `422` |
| Agent action record | Actual inspect, red, provisional edit, minimality rejection, final edit, and checks | `session.md` | Condensed from tool sequence |
| Exact diff | Three required production hunks, including separate `_send` and `return` lines | `patches/missing-product-policy.diff` | Machine-generated, replay-compared, and accepted under the smallest-reviewable-diff standard |
| Focused green output | Exported class name, runtime type name, and stable message | `evidence/focused-green.txt` | Runtime type derived from `type(exc).__name__`; raw, no normalization |
| Focused green exit status | `0` | `evidence/focused-green.exitstatus` | Raw |
| Broader capture command | `python3 tests/test_orphan_policy_broader.py .work` | `metadata.json` and `session.md` | Exact |
| Broader final command | `python3 tests/test_orphan_policy_broader.py` | Top-level `README.md` and replay | Package-local green |
| Broader green output | Two named pass lines | `evidence/broader-green.txt` | Raw, no normalization |
| Broader green exit status | `0` | `evidence/broader-green.exitstatus` | Raw |
| Listing 5.4 shipped loop | Top-level `server.py` per-item lookup | Canonical and staged Chapter 5 sources | Semantic excerpt; the printed `lines.append({...})` form removes the source-only outer line break recorded below |
| Listing 5.6 exact repair | Difference from `before/server.py` to top-level `server.py` | `patches/missing-product-policy.diff` | Exact three-hunk diff |
| Printed red and green transcript | Package-local commands and stored evidence | `chapter-session.md` | Checksum-bound publication source |
| Human policy boundary | Fail the summary closed and repair upstream | `README.md` and `session.md` | Human-owned |
| Concrete HTTP mapping | `422` with contextual error text | Patch, broader test, and session | Agent-selected under standing direction |
| Replay immutability | Complete maintained-file inventory | `run_capture.py` and `metadata.json` | Every maintained path and checksum remains unchanged; final green runs in disposable space |
| Runtime cleanup | `shop.db`, `server.log`, `.work`, bytecode, and test caches | `run_capture.py` | Removed on success, runtime failure, and preflight failure |
| Independent review | `evidence/independent-review.md` and `metadata.json` | Attributable canonical certification completed on 2026-07-15 with verdict `Pass`; receipt checksum verified during replay |
| Review gate | `run_capture.py`, `metadata.json`, and the maintained inventory | `complete_independently_reviewed` requires active status `completed`, verdict `Pass`, the exact package-local receipt, matching attribution, and a valid receipt checksum |

## Intentional excerpting and formatting

`chapter-session.md` condenses fixture setup and the private action record while preserving the reconstructed-contract label, all four red result lines, both focused green result lines, both broader pass lines, command exit statuses, one-sentence plan, exact three-hunk diff, approval basis, evidence boundary, and human-owned policy boundary in substance.

Listing 5.4 intentionally changes only the grouping of the final append call. The maintained source uses a 13-line form with `lines.append(` on one line, the dictionary opening on the next line, and the closing parenthesis after the dictionary. The printed listing uses the 11-line `lines.append({` form and closes with `})`. The dictionary keys, values, order, and executable behavior are unchanged. The listing also omits the captured missing-product guard because it presents the shipped red loop immediately before the repair transcript.

The staged chapter integrates that transcript into its diagnosis flow. It omits checksums, disposable-copy mechanics, the rejected provisional instrumentation, and the shell wrapper mistake because they do not advance the teaching job. It must not claim the author selected `422`, claim that upstream repair occurred, or send readers to this private package. No stored command output was reformatted or normalized.

The authorial inspection keeps `self._send(...)` and `return` on separate lines and explains why the one-line return form is not a smaller reviewable change. This is a readability and surrounding-idiom decision, not a behavior change; the raw evidence and patch therefore remain unchanged.

`session.md` and `chapter-session.md` preserve the historical capture and publication language that was accurate when the coding-agent package was assembled. Current certification is carried by this parity map, `metadata.json`, `README.md`, and `evidence/independent-review.md`.

## Origin boundary

The before fixture originated as a byte-identical copy of the incident demo used in the original pre-restructure session. That fact remains provenance, not a runtime dependency. Current replay verifies only package-local files and can run after this directory is copied away from the repository.
