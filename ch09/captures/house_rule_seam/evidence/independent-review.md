# Independent canonical capture review

## Certification

Verdict: **PASS**

No blocking capture, replay, behavioral import-shape, exact-patch, cleanup, isolation, checksum, minimality, provenance, printed-parity, or policy-boundary defect was found. This record certifies the canonical Chapter 9 `house_rule_seam` package.

## Attribution

- Reviewer role: Independent canonical capture reviewer
- Reviewer tool: Claude Code 2.1.210
- Reviewer model: `gpt-5.6-sol[1m]`
- Review date: 2026-07-15
- Review mode: Clean disposable copy with independent replay, red, patch, green, checksum, publication, and visual checks
- Reviewer repository edits: None
- Integration boundary: This receipt and the active certification metadata were added only after the read-only review returned `Pass`.
- Attribution limit: Raw vendor session logs are not retained. Tool and model attribution is package-level rather than cryptographically authenticated.

## Reviewed authorities

The reviewer checked the canonical capture package, its staged mirror, both current Chapter 9 sources, both committed Word deliverables, the session ledger mapping, and the printed transcript evidence. The shared ledger was inspected only to confirm the canonical path mapping and its external `Pending` workflow state. The reviewer did not edit it or treat that state as the package verdict.

Machine-specific roots below are represented with placeholders.

```bash
REPOSITORY_ROOT=<repository-root>
REVIEW_ROOT=/tmp/ch09-independent-review
PACKAGE="$REVIEW_ROOT/ch09"
CAPTURE="$PACKAGE/captures/house_rule_seam"
```

## Commands and observed results

### Fresh isolation

The canonical package was copied with `rsync` into the disposable review root. The source and copy contained 44 files and had the same aggregate SHA-256:

```text
1ddf67c31083d97972656486f71b89583c6564b7aaa177b2b141855d131533f8
```

### Canonical replay

```bash
python3 "$CAPTURE/run_capture.py"
```

The command exited `0`. It reproduced focused red with exit `1`, applied the exact stored patch, reproduced every green stage with exit `0`, and matched the package-local parity records.

### Independent focused red

The documented focused target ran against the immutable `before/` state and exited `1`. The direct transport returned success while the shared seam recorded no method, URL, or JSON. The failure therefore proved the selected routing defect rather than a dependency or network problem.

### Exact patch and scope

```bash
patch -s -p1 -i "$CAPTURE/patches/house_rule_seam.patch"
```

The command exited `0`. A fresh generated diff matched the stored patch exactly. Recursive before-and-after comparison found only `alerts.py` changed, with three removals and three additions. `http_client.py` remained byte-identical.

### Focused and broader green

The focused target passed after the patch:

```text
1 passed
```

The module-qualified positive case also passed:

```text
1 passed
```

The broader capture suite reported:

```text
10 passed
```

The top-level package suite reported:

```text
28 passed
```

### Compilation

`python3 -m py_compile` completed successfully over the package and capture Python files.

### Cleanup and stale-work rejection

A deliberately created `.work-stale-independent-review` directory caused replay to exit `1` with the expected stale-work error. A forced exception inside `disposable_work()` removed its work directory, and normal replay also left zero `.work-*` directories.

### Review-state invariant

Three targeted package parity tests passed. They confirmed that `Pending` was accepted only as a non-Pass workflow state and that a completed package claim required completed status, verdict `Pass`, no blocking findings, and a valid package-local review artifact checksum.

### Checksums

The reviewer independently recalculated metadata fixture, patch, package, and evidence checksums. All 34 assertions passed with zero failures.

### Canonical and mirror parity

The canonical package and the staged Chapter 9 package contained the same 44 files and the same aggregate SHA-256. No file was missing, extra, or changed.

### Ledger mapping

The shared session ledger mapped Chapter 9 to the canonical `house_rule_seam` package. Its `Pending` value remained a workflow state outside the package certification boundary.

### Source and Word parity

The canonical and staged Chapter 9 Markdown sources were byte-identical with SHA-256:

```text
3b4bc3dbdc53580e913f1d922b4e5649f46a52888d1804b01866d68ea91471dd
```

The two committed Word deliverables were byte-identical with SHA-256:

```text
58c50093dfe86d932c5bf19619ca058d1c0f7fafd11e97cf120a8452c9b0ab8b
```

Temporary conversion of both sources succeeded. Each generated document had 228 paragraphs and 6 tables, matching the committed output structure.

### Printed evidence and visual pass

Structural inspection found all six callout titles using `.AI Prompt Begin` or `.AI Response Begin`. The red excerpt, exact diff, green results, and policy paragraph were present. The six selected red lines matched raw evidence exactly and remained in order.

Raw document XML contained no prompt or response markers, code fences, TODO markers, or missing-image markers. LibreOffice rendered 23 pages. Canonical and staged page images had zero mismatches, and every page passed visual inspection without a layout defect.

### Prose and self-containment

`vale` reported zero errors and warnings for the canonical Chapter 9 source. `codespell` was clean. Internal-path, external-prerequisite, proprietary-name, and Unicode dash scans were clean.

### Final cleanup

The disposable review root was removed. The source tree remained unchanged and contained no capture-owned `.work-*` directories.

## Minimality and behavior

The production repair remains the exact three-line interface substitution:

```diff
-import requests
+from http_client import call
 
-    response = requests.post(ALERTS_URL, json={"text": message})
-    return response.status_code < 400
+    response = call("POST", ALERTS_URL, json={"text": message})
+    return response.status < 400
```

A zero-line state bypasses the approved seam. Removing only the direct transport import does not route the request. Changing the shared client or guard widens the slice. Collapsing the function into one expression removes the readable response-interface adaptation without narrowing behavior. The stored patch is the smallest reviewable, behaviorally complete repair in the surrounding style.

## Transcript and publication parity

The current chapter preserves the reconstructed contract label, genuine focused red, exact three-line diff, focused green, ten-test broader green, evidence boundary, and human-owned seam policy. The printed red excerpt selects six exact lines from the complete stored evidence. Commands may wrap for print width, but their tokens and order remain unchanged.

All six callout titles are mapped in `parity.md`. The earlier wording that said "five titles" while listing six was a non-blocking count error; package integration corrected the count without changing any title or transcript text.

## Provenance

- Coding-agent provenance remains Claude Code 2.1.210.642.
- The human inspection contract remains explicitly reconstructed from retained direction.
- The original action chronology remains separate from later certification repair.
- The historical nine-test canonical-support output remains checksum-verified origin evidence only and is not treated as the current package verdict.
- The shared ledger remains an external workflow record and was not edited during review or integration.

## Policy boundary

Focused green proves that the exact `POST` method, alert URL, and JSON payload reach `http_client.call`. Broader green protects the injected authentication, response contract, bounded retry behavior, fail-closed transport boundary, direct-import guard, live guard fixture, and module-qualified import shape.

The package does not prove live endpoint availability, real credentials, production transport behavior, backoff timing, observability, or whether every future outbound protocol belongs behind this seam. Service maintainers continue to own that policy.

## Final certification

**PASS**
