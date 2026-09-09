# Deployment-policy value capture parity

Stage: `complete_pending_recertification`; independent review: `historical`; status:
`Pending recertification`. Staged chapter integration is mapped in the final
package's top-level `parity.md`.

| Printed or captured item | Maintained source | Capture status |
|---|---|---|
| Deployment guard filename and historical excerpt | `before/deployment_guard.py` | Historical byte copy from the original support; checksum-verified locally |
| Unsafe deployment proposal | `before/deployment.json` | Historical byte copy of the original red fixture; checksum-verified locally |
| Historical broad-test contract | `before/test_deployment_guard.py` | Pre-revision package-test snapshot frozen so later CLI changes cannot rewrite the captured 24-test run; not claimed as original-session source |
| Focused behavior check | `tests/test_deployment_policy.py` | Checksum-verified; distinguishes structural acceptance from rollout-policy acceptance |
| Red command | `metadata.json` and `session.md` | Recorded exactly |
| Red output | `evidence/focused-red.txt` | Genuine command output with elapsed time normalized |
| Red exit status | `evidence/focused-red.exit-status` | Genuine exit `1` |
| Agent observation and one-sentence plan | `session.md` | Grounded in the source, corrected focused test, and final red result |
| Approval basis and selected policy | `session.md` and `metadata.json` | Agent selected `max_unavailable: 1` under standing direction; no false option attribution |
| Actual action sequence | `evidence/agent-actions.jsonl` | Original session actions preserved in order, including the package-local harness correction |
| Exact production diff | `patches/deployment_policy_value.diff` | Machine-generated one-line value substitution |
| Focused green output | `evidence/focused-green.txt` | Genuine output, exit `0` |
| Broader green command | Package-local operational support copied beside the disposable after-state | Twenty-four operational cases exercised against the patched configuration |
| Broader green output | `evidence/broader-green.txt` | Genuine pytest output with elapsed time normalized, exit `0` |
| Original canonical-support green | `evidence/canonical-support-green.txt` | Historical origin evidence, checksum-preserved with replay status `preserved_not_executed` |
| Final-package green | `evidence/final-package-green.txt` | Current package-local 29-test output, reproduced during replay |
| Final-package immutability | `final_package_support.checksums_sha256` in `metadata.json` | All declared package files remain unchanged during replay |
| Independent review | `evidence/independent-review.md` and `metadata.json` | Attributable read-only review completed on 2026-07-15 with verdict `Pass`; artifact checksum verified during replay |
| Listings 11.1 through 11.5 | Top-level `parity.md` and `test_listing_parity.py` | Five package-local checks map code excerpts, command output, and the maintained packet artifact exactly |
| Human policy boundary | `README.md`, `session.md`, and `metadata.json` | Fixture uses one unavailable replica; live capacity evidence still controls a real deployment |

## Intentional excerpting and normalization

The before fixture is a historical byte copy, not a reconstruction. The session narrative condenses tool activity, while `evidence/agent-actions.jsonl` preserves the original action order. Stored command output preserves genuine pytest text and exit status, with only elapsed time replaced by `<TIME>`. Pytest color, external plugin loading, bytecode, and cache output are disabled; replay applies the same normalization while comparing fresh output with stored evidence.

The staged focused test initially pinned the unsafe value `2`, so the same test could not turn green after a production-only value repair. Before the production edit, the agent changed that package-local assertion to compare the loader result with the current configuration and reran genuine red. This correction changes no production behavior and is recorded in the action log and metadata.

The captured broader check is not a second workflow. Replay copies the explicit operational file manifest from the final package into disposable space, overlays the byte-checked before source, configuration, and historical broad-test contract, applies the one-line production diff, and runs the three original test modules there. It does not copy or inspect repository-root support.

## Chapter integration boundary

The final package's top-level `parity.md` maps every staged listing. Listing 11.1 removes only function indentation; Listings 11.2 and 11.3 omit one-line docstrings; Listing 11.4 is exact deterministic command output; Listing 11.5 is maintained byte-for-byte in `listing_11_5.txt`.

The package paths remain private authoring details. The reader-facing chapter preserves the filename, bounded contract, red result, exact diff, focused and broader green results, evidence boundary, and human policy decision without directing the reader to external code.

`session.md` preserves the historical pending-review language that was accurate when the coding-agent capture was assembled. The prior review receipt is historical after the support-contract changes; current recertification status is carried by this parity record, `metadata.json`, and `README.md`.
