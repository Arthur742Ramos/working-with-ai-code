# Capture and publication parity ledger

The staged Chapter 8 prose is the publication authority. `chapter-session.md` retains the integrated session excerpt as a package record, while this ledger distinguishes original capture evidence from the later final-package promotion check.

Stage: `complete_independently_reviewed`; independent review: `completed`; status: `Pass`. The attributable review reproduced canonical and mirror packages from clean disposable copies, matched all 20 metadata checksum claims and all 28 non-cache files, and returned `Pass, narrowly` on minimality. During that read-only review, the shared publication ledger was `Pending`; aggregate reconciliation later moved Chapter 8 to `Pass`. The historical receipt and review-scoped metadata preserve the earlier state. The ledger's current status and the package verdict now agree, but replay still treats them as separate controls.

| Printed or recorded item | Maintained source | Parity status |
|---|---|---|
| Binary-float before-state | `before/allocation.py` | Byte-checked copy of the reviewed float largest-remainder implementation |
| Exact-rational after-state | `after/allocation.py` | Matches `patches/allocation.patch`; adds `Fraction(str(weight))` while retaining the named largest-remainder stages |
| Focused test | `tests/test_lost_cent.py::test_equal_exact_remainders_keep_input_order` | Pins `allocate(10, [1, 1, 4]) == [2, 2, 6]` and fails as `[2, 1, 7]` before the patch |
| Original conservation case | `tests/test_lost_cent.py::test_pennies_are_conserved` | Retains `[3334, 3333, 3333]` and exact-total coverage |
| Prior neighboring cases | `tests/test_neighboring_behavior.py` | Retains even, weighted, unequal largest-remainder, and round-first shortcut coverage |
| Prior discriminating assertion | `tests/test_neighboring_behavior.py::test_round_then_force_first_is_rejected` | Retains `allocate(1, [1, 1, 2]) == [0, 0, 1]` and rejects round-then-force-index-zero |
| Red command and output | `metadata.json`, `evidence/focused_red.txt`, and `session.md` | Exact command, raw output, and exit `1` recorded |
| One-sentence plan | `session.md` | Condensed from the direct agent sequence after the genuine red and before the reviewed repair |
| Exact production diff | `patches/allocation.patch` | Machine-generated with `diff -u`; one arithmetic-representation change in the existing workflow |
| Focused green | `evidence/focused_green.txt` and `.exit_status` | Raw output, exit `0` |
| Broader green | `evidence/broader_green.txt` and `.exit_status` | Raw six-test output, exit `0` |
| Original maintained baseline | `evidence/canonical_support_green.txt` and `.exit_status` | Genuine nine-test output from the original session; `preserved_not_executed` by isolated replay |
| Final publication implementation | top-level `allocation.py` | Promotes the exact-rational representation into the maintained allocator with validation and `split_charge` intact |
| Nine canonical-equivalent checks | top-level `test_allocation.py` and `test_golden.py` | Eight maintained behavior checks plus one golden-set test run against the promoted implementation |
| Promoted exact-tie test | `test_allocation.py::test_equal_exact_remainders_keep_input_order` | Adds the tenth top-level check against the same promoted implementation |
| Final-package green | `evidence/final_package_green.txt` and `.exit_status` | Genuine package-local ten-test output, exit `0` |
| Test collection boundary | top-level `pytest.ini` | Excludes `captures/` so top-level discovery does not collect capture internals twice |
| Package checksum lock | `metadata.json` and `run_capture.py` | Locks the top-level source, both test files, and `pytest.ini` before and after replay |
| Cleanup invariant | `run_capture.py` | Rejects stale `.work-*` directories, exercises exception-path cleanup, and requires zero work directories after replay |
| Independent review | `evidence/independent-review.md` and `metadata.json` | Records the read-only reviewer, Claude Code 2.1.210.bee, model `gpt-5.6-sol[1m]`, runtime, clean canonical and mirror replay, 20 checksum claims, 28-file parity, narrow minimality verdict, and package `Pass`; checksum-locks the fixed active receipt |
| Certification mutation boundary | receipt, `metadata.json`, `run_capture.py`, both README files, and `parity.md` | Replay snapshots all six certification files and rejects any change during execution |
| Coding-agent provenance | `metadata.json`, `session.md`, and `chapter-session.md` | Identifies Claude Code 2.1.210; no vendor quotation is reconstructed |
| Actual action record | `session.md` | Preserves direct float-residue inspection, the harmless shell-wrapper variable failure, intentional record, and immutable original replay |
| Publication evidence boundary | staged prose, `chapter-session.md`, and this ledger | The historical nine-test run proved only that the unchanged baseline was green; the final-package ten-test run closes the unified release gap |
| Human policy boundary | `metadata.json`, both README files, and both session records | Domain owners decide accepted numeric types, conversion semantics, and tie fairness |

## Intentional excerpting and formatting

The package preserves raw pytest output in `evidence/`. `session.md` reproduces the four original outputs verbatim. `chapter-session.md` reproduces the focused red, focused green, capture broader green, and original nine-test maintained-baseline green. Replay ignores only elapsed-time text during comparison; it does not rewrite stored output.

The exact diff in `session.md` and `chapter-session.md` is copied from `patches/allocation.patch` without paraphrase. The human contract and action narration are condensed from retained direction and the direct tool sequence. They are not vendor quotations.

The staged publication excerpt omits private authoring paths, fixture copying, checksum mechanics, and the shell-wrapper variable mistake. It retains the bounded contract, exact test name, genuine red output and exit, one-sentence plan, approval basis, exact diff, green summaries, evidence boundary, and human-owned policy boundary.

The post-capture `evidence/final_package_green.txt` is not presented as part of the original agent session. It records the later final-package promotion check required by the staged chapter's release boundary.

## Teaching parity

The session remains one Chapter 8 review loop. It begins with the already-taught largest-remainder repair, shows a green conservation invariant masking a stable-tie defect, strengthens the arithmetic representation, and reruns focused and broader checks. It does not add a second allocation algorithm or a separate workflow.

The focused case demonstrates the representation bug with ordinary integer weights: all exact remainders are two-thirds, yet the float implementation ranks the third residue higher. `Fraction(str(weight))` restores exact comparison before Python's stable sort applies input order.

The staged chapter correctly says the original nine-test baseline did not prove compatibility with the staged repair. The final package now supplies that missing engineering evidence by running those nine canonical-equivalent checks plus the promoted exact-tie test against one top-level implementation.

## Minimality parity

The patch adds one standard-library import and one named `exact_weights` stage. The existing `ideal`, `shares`, `leftover`, `order`, and mutation loop remain. A denser conversion inside the ideal expression would change fewer lines but hide the representation boundary that reviewers need to inspect.

The prior discriminating cases remain beside the new one. The exact-tie case rejects binary-float misordering. The one-cent `[1, 1, 2]` case still rejects round-then-force-index-zero. The unequal case still proves that the largest remainder receives the leftover.

## Policy parity

The focused result pins stable input order only after exact rational comparison. The tests enforce that selected capture policy for the covered values. They do not make decimal-string interpretation or stable input order universally correct. Domain owners retain those decisions.

The final package is self-contained. Replay resolves only package-local source, tests, configuration, capture fixtures, patch, evidence, and records. Historical repository checksums remain metadata provenance and are never resolved as executable dependencies.

## September 9 final explanation check

The condensed publication narration now says that index 2 receives the first leftover cent. Recomputing the printed floating-point case gives remainder order `[2, 0, 1]`, so index 2 is visited before index 0. This corrects the allocation order in the explanation only; the resulting `[2, 1, 7]`, expected `[2, 2, 6]`, raw session outputs, fixtures, patch, and implementation are unchanged.
