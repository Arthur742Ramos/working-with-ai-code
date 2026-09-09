# Independent canonical capture certification

## Certification

Verdict: **PASS**

No certification blocker was found. This record certifies the canonical Chapter 5 `incident_orphan_product_policy` capture package reviewed on 2026-07-15.

## Attribution

- Reviewer role: Independent canonical-capture certifier
- Reviewer tool: Claude Code 2.1.210.bee, gpt-5.6-sol[1m]
- Review date: 2026-07-15
- Canonical target: `<repository-root>/code/ch05/captures/incident_orphan_product_policy`
- Review mode: Clean disposable workspace
- Disposable workspace retained: No
- Repository modified by reviewer: No
- Attribution limit: This receipt preserves the supplied independent certification report. Raw vendor session logs are not retained in the package.

## Commands and results

### Default replay

```bash
python3 <disposable-workspace>/package/captures/incident_orphan_product_policy/run_capture.py
```

Result: exit `0`. Replay reproduced the genuine focused red, exact patch, focused green, broader green, final-package greens, inventory verification, and checksum parity.

### Independent manual chain

The reviewer independently ran the focused red, applied the patch with POSIX `patch -p1`, regenerated the diff with `diff -u`, and ran the focused and broader greens.

Observed:

- Focused red exited `1` with the expected accidental `TypeError`.
- Patch application exited `0`.
- The regenerated diff matched `patches/missing-product-policy.diff` byte for byte.
- Focused and broader greens exited `0`.
- Both maintained top-level test scripts exited `0`.

### Record replay

```bash
python3 <disposable-workspace>/package/captures/incident_orphan_product_policy/run_capture.py --record
```

Result: exit `0`. All six evidence hashes remained unchanged.

### Negative controls

The reviewer confirmed that replay rejects each of these conditions with a nonzero exit:

- Before-fixture checksum drift.
- Runtime failure.
- Maintained-file inventory drift.
- Contradictory completed-review state.
- Missing review receipt.
- Forced patch failure.

Every failure path removed `.work`, `shop.db`, `server.log`, bytecode, and test caches.

## Minimality

The reviewer removed each patch responsibility in turn:

- Removing the exception class broke the focused behavior.
- Removing the pre-price guard restored the accidental `TypeError`.
- Removing the API mapping preserved focused green but broke the broader API-boundary green.

All three production responsibilities are required. The patch is the smallest reviewable behaviorally complete change under the selected contract.

## Integrity and parity

At review time, the canonical and mirrored packages matched across exactly 25 maintained files, with identical relative paths and SHA-256 hashes. Both packages had zero runtime residue.

The canonical and staged Chapter 5 sources were byte-identical at review time:

```text
7c81e7c4c2cb372b8bb753f7f3e5fff9ff78ee6c0749e7d6dcd7461dd4ee1764
```

The reviewer also confirmed:

- Listing 5.6 contains the stored patch exactly.
- Raw red and green evidence, commands, and exit statuses match the printed transcript after Markdown blockquote normalization.
- Listing 5.4 is Abstract Syntax Tree equivalent to the retained red loop.
- The documented 13-line to 11-line formatting normalization and omitted captured guard are accurate.
- Provenance correctly names Claude Code and labels the reconstructed human contract.
- The chapter states that the coding agent selected `422`.
- The owning team retains responsibility for the public API contract and upstream referential-integrity policy.
- The shared ledger maps Chapter 5 to this capture. Its external `Pending` state was not used as the package verdict.

## Quality checks

JSON validation, Python syntax validation, `codespell`, and prohibited-dash checks passed. Temporary bytecode created during syntax validation was removed.

## Policy boundary

The package proves the deterministic orphan failure, exact bounded repair, named domain exception, selected fail-closed `422` mapping, and protected neighboring success path. It does not establish `422` as the final public contract or repair upstream referential integrity. Those decisions remain with the owning team.

## Final certification

**PASS**
