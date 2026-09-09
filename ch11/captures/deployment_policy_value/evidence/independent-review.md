# Independent canonical capture review

## Certification

Verdict: **PASS**

No blocking capture, replay, parity, isolation, minimality, provenance, or policy-boundary defect was found. This record certifies the canonical Chapter 11 `deployment_policy_value` capture package.

## Attribution

- Reviewer role: Independent canonical capture reviewer, read-only
- Reviewer tool: Claude Code 2.1.210.814
- Review date: 2026-07-15
- Review mode: Clean disposable copy
- Repository modified by reviewer: No
- Attribution limit: This package preserves the supplied independent review report. Raw vendor session logs are not retained here.

## Reviewed authorities

The reviewer checked the canonical capture package against the real-session capture standard and the active Chapter 11 mapping. The review also compared the canonical and staged chapter sources, verified all printed listings and transcript evidence, and confirmed that reader-facing prose exposes no private support or restructuring path.

The commands below preserve the reviewed operations while replacing machine-specific roots with variables.

```bash
REPOSITORY_ROOT=<repository-root>
REVIEW_ROOT=/tmp/ch11-canonical-review.<id>
PACKAGE="$REVIEW_ROOT/ch11"
CAPTURE="$PACKAGE/captures/deployment_policy_value"
```

## Commands and results

### Non-recording replay

```bash
python3 "$CAPTURE/run_capture.py"
```

Observed:

```text
RED VERIFIED: exit 1
PATCH VERIFIED: strict one-line production diff
FOCUSED GREEN VERIFIED: exit 0
BROADER GREEN VERIFIED: exit 0
FINAL PACKAGE GREEN VERIFIED: exit 0
ORIGIN PROVENANCE VERIFIED: preserved, not executed
PARITY VERIFIED: package and capture ledgers complete
```

### Independent package suite

```bash
cd "$PACKAGE"
PY_COLORS=0 PYTHONDONTWRITEBYTECODE=1 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python3 -m pytest -q -p no:cacheprovider
```

Result: **29 passed**, comprising 24 operational tests and 5 listing-parity tests.

### Manual red reproduction

The immutable before source, configuration, and focused test were copied into a disposable manual state.

```bash
cd "$REVIEW_ROOT/manual-state"
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_policy.py::\
test_schema_valid_deployment_satisfies_policy
```

Result: exit 1 with exactly one policy violation:

```text
max_unavailable must be 0 or 1
```

### Patch application and focused green

```bash
patch -p1 < "$CAPTURE/patches/deployment_policy_value.diff"
shasum -a 256 deployment.json
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_policy.py::\
test_schema_valid_deployment_satisfies_policy
```

The after-state SHA-256 was:

```text
53aa995496d8602e6a2ee95b1c7ebf49de4a252c79ba3c4469eb9b8a5346a5d2
```

Result: **1 passed**.

### Broader green

```bash
python3 -m pytest -q -p no:cacheprovider \
  test_deployment_guard.py \
  test_incident_triage.py \
  test_pipeline.py
```

Result: **24 passed**.

### Operational boundary

```bash
python3 deployment_guard.py plan deployment.json
python3 deployment_guard.py verify \
  deployment.json observation.json
PYTEST_ADDOPTS='-p no:cacheprovider' python3 pipeline.py
```

Observed:

- `policy=PASS`
- `verification=PASS`
- Pipeline internal suite: 24 passed
- Final state: `pipeline=READY_FOR_APPROVAL`
- No apply stage, credential use, cloud call, or target-system write occurred.

### Isolation

The package suite and replay were run in a sandbox that denied reads from `$REPOSITORY_ROOT`.

```bash
/usr/bin/sandbox-exec \
  -p '(version 1) (allow default)
      (deny file-read* (subpath "<repository-root>"))' \
  /bin/zsh -c '
    cd "<disposable-package>" &&
    PY_COLORS=0 PYTHONDONTWRITEBYTECODE=1 \
    PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
    python3 -m pytest -q -p no:cacheprovider &&
    python3 captures/deployment_policy_value/run_capture.py
  '
```

Result: 29 tests passed and the full replay passed. Historical repository paths were unavailable to the process, and no executable file contained a historical repository path reference.

### Checksums and cleanup

- Declared package-local checksums: 34 of 34 passed.
- Before fixtures: 2 passed.
- Capture inputs: 5 passed.
- Evidence artifacts: 11 passed.
- Final support files: 15 passed.
- Agent action log: 1 passed.
- Complete non-cache manifest: 36 files unchanged.
- Before and after manifest comparison: `cmp` exit 0.
- Remaining `.work-*` directories: 0.
- Canonical and disposable relative manifests: equal, 36 of 36 files.

## Minimality

The production patch changes one JSON value:

```diff
-    "max_unavailable": 2
+    "max_unavailable": 1
```

The reviewer exercised adversarial alternatives:

- A zero-line change left the focused test red.
- Changing the value to `0` made the focused test pass, but the broader suite produced 23 passed and 1 failed because the selected approval surface changed.
- Widening the guard to accept `2` made the focused test pass, but the broader suite produced 22 passed and 2 failed because it erased the preserved unsafe-fixture rejection and changed the approval surface.
- Changing the test would hide the violation without repairing production behavior.

No smaller behaviorally complete patch satisfies the selected contract. The `2` to `1` substitution is minimal without weakening policy.

## Transcript and listing parity

All 12 direct parity checks passed. Listings 11.1 through 11.5 match maintained source, deterministic command output, or the byte-exact packet artifact. Printed red, patch, focused green, and broader green match package evidence. The red excerpt removes trailing spaces from two pytest lines during Markdown formatting, while all non-whitespace content remains exact.

The reconstructed initial contract is explicitly labeled. The retained completion direction remains distinct from that reconstruction. Canonical and staged chapter sources were byte-identical at review time. Reader-facing prose contained no internal Chapter 11 support path, capture-package path, or restructuring path.

## Provenance

- Coding-agent provenance records Claude Code 2.1.210.642.
- Before fixtures are local historical byte copies with verified checksums.
- The initial contract is honestly labeled reconstructed.
- The completion direction and action order are retained.
- All 13 action-log records are sequential and agree with the patch and commands.
- Original canonical-support output is classified as `preserved_not_executed`.
- The original session recorded a non-clean working tree, so provenance proves the checksummed captured files and actions, not unrelated repository state.

## Policy boundary

`max_unavailable: 1` is a captured fixture policy, not a universal deployment recommendation. A service owner or release team must verify peak capacity, service objectives, and rollback headroom before authorizing a production write.

The package does not exercise an apply stage, credentials, a cloud API, target drift, live traffic, or rollback against a real target. Those decisions and checks remain human-owned.

## Final certification

**PASS**
