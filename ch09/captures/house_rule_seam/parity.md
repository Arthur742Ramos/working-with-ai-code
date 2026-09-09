# Parity map

Stage: `complete_independently_reviewed`; active review: `completed`; verdict: `Pass`. The shared session ledger was `Pending` during read-only package review and later moved to aggregate `Pass` during whole-book reconciliation. Neither workflow state is the package verdict.

## Supersession decision

The earlier GitHub Copilot CLI transcript is formally superseded. Its publication status is `superseded`, not an alternate transcript. It uses a different command surface, fixture path, timing, and provenance from this independently replayed Claude Code package. Do not copy that transcript, its `fixtures/direct_requests` commands, its compact diff, or its recorded timings into the current chapter.

Use `chapter-session.md` as the publication-ready source together with the explicit excerpt and formatting allowances below. The current sources are `chapters/ch09.md` and `manuscripts/restructure/chapters/ch09.md`; both must retain the same session text.

## Exact evidence map for the current chapter

| Printed or captured item | Maintained source | Required current use |
|---|---|---|
| Coding-agent provenance | `metadata.json`, `coding_agent`; `session.md`, Provenance | Identify the real coding agent as Claude Code. The chapter may combine the two opening provenance paragraphs into one sentence, but must retain reconstructed-contract status. |
| Contract status | `metadata.json`, `human_contract`; `session.md`, Human contract | State that the inspection contract was reconstructed from retained direction. Do not present it as a verbatim quotation. |
| Bounded contract | `session.md`, Human contract; `chapter-session.md`, prompt | Preserve the complete prompt in `chapter-session.md`: inspect `alerts.py`, the routing test, guard, and shared interface; run focused red before editing; require the existing method, URL, and JSON through `http_client.call`; preserve readable idiom; and do not weaken tests, add dependencies, or edit canonical files. |
| Prompt and response titles | `chapter-session.md` | Preserve the prompt title `Inspect the seam before editing`. Label the five response boxes in order as `Captured response 1 of 5` through `Captured response 5 of 5`, followed by the response-specific description. |
| Filename | `alerts.py` | Name only `alerts.py` in reader-facing prose. |
| Shared boundary | `http_client.py` | Explain that the shared client owns the outbound boundary. Do not expose its internal support path. |
| Production excerpt | `send_alert()` in `before/alerts.py` and `after/alerts.py` | Use the exact three-line interface substitution shown in `chapter-session.md`. |
| Focused test | `test_send_alert_routes_through_house_client` in `tests/test_alerts.py` | Preserve the exact test name. The test patches `http_client.call` before loading the feature, then proves exact method, URL, and JSON routing. It accepts direct or module-qualified shared-client use. |
| Import-shape positive case | `test_module_qualified_shared_client_shape_is_accepted` in `tests/test_alerts.py` | Retain in broader green as private capture machinery. It prevents the focused observer from regressing to a local-symbol requirement. |
| Red command | `metadata.json`, `red.command` | Use the same command tokens shown in `chapter-session.md`. Backslash line wrapping is the only command formatting change. |
| Red exit | `metadata.json`, `red.exit_status`; `evidence/focused_red.exit_status` | Preserve exit status `1`. |
| Full red output | `evidence/focused_red.txt`; `chapter-session.md` | `chapter-session.md` reproduces every stored line exactly. |
| Printed red excerpt | `evidence/focused_red.txt`; both current chapter sources | The chapter intentionally prints six exact lines, in order: the `F [100%]` progress line; the `AssertionError` line naming method, URL, JSON, and `http_client.call`; `tests/test_alerts.py:57: AssertionError`; the short-summary header; the `FAILED` line; and the `1 failed` line. Omitted traceback lines remain in `chapter-session.md` and raw evidence. |
| Agent red observation | `session.md`, observation after Genuine focused red | Preserve that the direct transport returned success while the shared seam recorded no method, URL, or JSON. State that the observer accepts direct or module-qualified shared-client use. |
| One-sentence plan | `session.md`, One-sentence smallest-reviewable-change plan | Preserve the complete sentence reproduced after `Plan:` in `chapter-session.md`. It precedes the edit. |
| Approval basis | `session.md`, Approval basis; `metadata.json`, `approval_basis` | Attribute the implementation choice to standing delegation plus the already-set seam policy. Do not claim the author selected a named option. The chapter may condense this to one paragraph. |
| Agent action chronology | `evidence/agent-actions.md` | Preserve inspect, red, plan, approval basis, edit, focused green, and broader green order. The certification-repair section must remain separate from the original session chronology. |
| Exact diff | `patches/house_rule_seam.patch` | Reproduce the complete machine-generated unified diff. Keep the three-line import, call, and status substitution. Do not shrink it to an import-only patch or collapse `send_alert()` into one expression. |
| Focused green command and output | `metadata.json`, `focused_green`; `evidence/focused_green.txt` | Repeat the focused command after the diff and reproduce its two stored output lines exactly. |
| Broader green command and output | `metadata.json`, `broader_green`; `evidence/broader_green.txt` | Run after focused green and reproduce the two stored output lines exactly, including `10 passed`. |
| Evidence boundary | `session.md`, Agent evidence boundary | State that focused green proves exact method, URL, and JSON reach the seam; state what broader green protects; then state that neither proves live service, credential, transport, timing, or cross-system policy behavior. |
| Authorial inspection and policy boundary | `chapter-session.md`, closing paragraph; `session.md`, Author inspection and human-owned policy decision | Retain one closing inspection paragraph. Keep failure and seam policy human-owned. Do not add a second compliance paragraph. |
| Independent review | `evidence/independent-review.md`; `metadata.json`, `review_state.active_review` | Attributable canonical review completed on 2026-07-15 with verdict `Pass`; replay verifies its package-local path and SHA-256. |
| Review state | `metadata.json`, `review_state`; `README.md`, Independent review state | Active stage is `complete_independently_reviewed`, status is `completed`, and verdict is `Pass`. Historical first-review findings remain preserved. The ledger was `Pending` during review and now records aggregate `Pass`; neither state is the package verdict. |
| Review gate | `run_capture.py`, `verify_review_state`; top-level `test_package_parity.py` | A completed claim requires completed active status, verdict `Pass`, no blocking findings, and a present checksum-locked receipt under `evidence/`. |
| Cleanup invariant | `run_capture.py`, `disposable_work`; top-level `test_package_parity.py` | Replay must remove `.work-*` state after success and exceptions and reject stale disposable directories. |
| Guard self-test | `test_direct_requests_source_proves_guard_is_live` | Covered by broader green but omitted from the printed transcript as capture machinery. |
| Broader setup failure | `evidence/broader_green_setup_failure.txt` | Retain in the private record. Omit from publication because it is capture setup chronology, not feature behavior. |
| Canonical support green | `evidence/canonical_support_green.txt` | Retain as historical parity evidence. Do not print its internal command or support path. |

## Intentional excerpting and formatting

`chapter-session.md` omits capture-directory paths, fixture copying, checksum operations, the shell variable mistake around the first diff wrapper, the broader setup correction, and the historical canonical-support command. Those items remain in the private package record.

The current chapter makes four additional, explicit editorial changes. It combines the publication source's opening provenance paragraphs, condenses the approval and diagnosis prose without changing the policy or sequence, labels the five continued response boxes in order, and prints the six-line red excerpt mapped above instead of the full traceback. Commands, diff lines, focused green, and broader green match `chapter-session.md`. These changes are authorized condensation, not evidence substitution.

Command formatting uses shell line continuation for print width. Command tokens and order match `metadata.json`. Stored evidence retains raw pytest progress lines and timing; replay normalizes only elapsed time during comparison. No reader-facing text exposes this private package, an internal support path, or an external code prerequisite.
