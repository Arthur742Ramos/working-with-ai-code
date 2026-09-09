# Idempotent 409 replay session

Status: implementation and evidence capture complete. Independent review remains pending.

## Actual human contract

The following is an original, verbatim excerpt from the human's completion request:

> Standing author direction: choose the best implementation without another approval checkpoint. Approval policy for this slice: Treat 409 as already created only for this exact idempotent endpoint and identity contract; do not generalize other conflicts.
>
> Complete the actual coding-agent session inside the staged package only. Verify the genuine red first. Record the approval basis without claiming the author named a specific option. Apply the strict smallest production diff to a disposable or after-state copy, record the machine-generated exact diff, run genuine focused green and broader green, store raw output and exit statuses, complete session.md, metadata.json, README.md, parity.md, and a non-recording replay mode. Preserve the actual agent action record. Keep canonical chapter and canonical code files unchanged.

The staged package also retained its earlier inspection-stage contract and red evidence. That record required inspection and a genuine focused red before any implementation edit.

## Reconstructed bounded contract for chapter integration

RECONSTRUCTED CONTRACT: The wording below condenses the retained staged contract and the current author direction. It is not a retained historical vendor quotation.

> The importer is in `importer.py` with tests in `test_importer.py`. Verified policy evidence says this exact endpoint returns `409 Conflict` for the same stable `source_id` and idempotency key to mean "already created." Inspect the files and run only `test_conflict_is_idempotent_replay` before editing. Report the red result and a one-sentence strict-smallest-change plan. After approval, apply only the bounded edit, then run the focused test and the full test file. Do not generalize other conflicts.

Current provenance clarification: the paragraph above is preserved historical wording. For current chapter use, treat its `409` rule as a supplied human contract, not observed upstream policy evidence. The retained runs verify local implementation behavior only; they cannot establish that the service keeps the promise.

## Agent inspection

The agent read `before/importer.py`, `tests/test_importer.py`, the red-only runner, and every staged record before executing the package. The test was a byte-for-byte copy of the then-maintained source test. No historical pre-repair blob exists in git, so the before importer is explicitly reconstructed by removing only the documented `409` acceptance behavior from the checksum-recorded source used by the original session. The final package retains local support copies and no longer resolves that historical origin during replay.

The staged source returns only for status codes below `400`. Because `409` is not in `TRANSIENT`, the next branch raises `RuntimeError`. The focused test supplies one `409` result and requires `send_with_retry` to return that result.

## Genuine focused red

The agent first ran the existing non-recording replay from the staged support package. In this final copy, the equivalent package-local command is:

```bash
python3 captures/idempotent_409_replay/run_capture.py
```

The focused subprocess ran in disposable `.work/` space:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.work \
python3 -m pytest -q --color=no -p no:cacheprovider \
tests/test_importer.py::test_conflict_is_idempotent_replay
```

Exit status: `1`

Normalized display below; raw combined output is retained in `evidence/focused-red.txt`:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
______________________ test_conflict_is_idempotent_replay ______________________

    def test_conflict_is_idempotent_replay():
        # The API returns 409 for a duplicate source_id and treats it as
        # "already created." A 409 must count as a successful send, not a
        # failure, or a retried batch inflates the failure count.
        row = parse_customer({"source_id": "C-1", "email": "x@y.co", "name": "X"})
>       result = send_with_retry(row, fake_sender(409), attempts=3)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_importer.py:82: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

row = CustomerRow(source_id='C-1', email='x@y.co', name='X', key='07e9a9696557f5c8f882be06e799bc09')
sender = <function fake_sender.<locals>.sender at 0x<address>>, attempts = 3

    def send_with_retry(
        row: CustomerRow,
        sender: Sender,
        attempts: int = 3,
    ) -> ApiResult:
        request = build_request(row)
    
        for attempt in range(1, attempts + 1):
            result = sender(request)
            if result.status < 400:
                return result
            if result.status not in TRANSIENT:
>               raise RuntimeError(result.body)
E               RuntimeError

.work/importer.py:83: RuntimeError
=========================== short test summary info ============================
FAILED tests/test_importer.py::test_conflict_is_idempotent_replay - RuntimeError
1 failed in <time>s
```

## Agent observation

The focused test is genuinely red because `409` bypasses the existing success condition and enters the generic non-transient failure branch at `.work/importer.py:83`, which raises `RuntimeError` instead of returning the replay result.

## One-sentence strict-smallest-change plan

Change only the existing success condition in `send_with_retry` so it also returns for `result.status == 409`, leaving all retry and other non-transient failure behavior unchanged.

## Approval basis and selected policy

The author did not name a code option or select a syntax. The standing direction authorized the coding agent to choose the best implementation without another checkpoint, while the explicit policy limited success handling to `409` from this exact idempotent endpoint and identity contract.

The agent selected an exact `result.status == 409` disjunct in the existing success condition. This is one changed production line, does not create a reusable conflict policy, and cannot accept `400` through `408` or any status above `409`.

## Actual agent action record

1. Read the governing capture standard and every staged source, test, evidence, and documentation file.
2. Ran the existing non-recording red replay. It reproduced exit status `1` and the expected `RuntimeError` branch.
3. Recomputed SHA-256 hashes for the before fixture, focused test, and then-maintained support files. All matched the staged metadata.
4. Recorded the one-sentence plan and selected the endpoint-specific exact-status condition under the standing approval direction.
5. Copied `before/importer.py` into disposable `.work/importer.py`. The first guarded replacement command used twelve spaces instead of eight; its assertion failed before writing, so it made no source change. The empty diff artifact from that failed attempt was overwritten.
6. Repeated the guarded replacement with the exact eight-space source text. The source edit and `diff -u` generation succeeded. A trailing zsh bookkeeping assignment used the reserved variable name `status` and failed after the patch had already been written. The agent read and inspected the generated patch before continuing.
7. Ran the focused green command against the disposable patched copy and stored raw output plus exit status `0`.
8. Ran the full staged test file against the same disposable patched copy and stored raw output plus exit status `0`.
9. Ran the unchanged support test file and stored raw output plus exit status `0`; source and test hashes remained unchanged.
10. Ran the completed default replay without `--record`. It reproduced red exit `1`, verified the exact patch, reproduced focused and broader green exit `0`, reproduced support exit `0`, verified parity, and removed `.work/`.

The original session did not edit the chapter or the then-maintained importer and test. This final copy validates only package-local support.

## Exact machine-generated diff

The agent generated `patches/idempotent_409_replay.patch` with `diff -u` between the immutable before fixture and the disposable patched copy:

```diff
--- a/importer.py
+++ b/importer.py
@@ -77,7 +77,7 @@
 
     for attempt in range(1, attempts + 1):
         result = sender(request)
-        if result.status < 400:
+        if result.status < 400 or result.status == 409:
             return result
         if result.status not in TRANSIENT:
             raise RuntimeError(result.body)
```

The patch removes one line and adds one line. A smaller line-count patch is impossible because the existing comparison must change to accept exactly one additional status. Replacing `< 400` with `<= 409` or `< 410` would be the same line count but would broaden success to `400` through `408`, violating the approved policy. Adding a separate branch, constant, or generic conflict set would require more production lines.

## Genuine focused green

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.work \
python3 -m pytest -q --color=no -p no:cacheprovider \
tests/test_importer.py::test_conflict_is_idempotent_replay
```

Exit status: `0`

Normalized display below; raw combined output is retained in `evidence/focused-green.txt`:

```text
.                                                                        [100%]
1 passed in <time>s
```

## Genuine broader green

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.work \
python3 -m pytest -q --color=no -p no:cacheprovider \
tests/test_importer.py
```

Exit status: `0`

Normalized display below; raw combined output is retained in `evidence/broader-green.txt`:

```text
.......                                                                  [100%]
7 passed in <time>s
```

The package-local support suite also exits `0` with seven passing tests. Its output is retained in `evidence/package-support-green.txt`.

## Agent evidence-boundary statement

The red and green checks prove that the one-line staged patch changes the selected `409` path from `RuntimeError` to a returned `ApiResult` while the seven neighboring tests remain green. They do not prove the upstream endpoint contract, the identity of an existing customer, payload equivalence, or safety for any other conflict response. The package-support run proves only that the final package's green importer suite still passes without editing it.

## Author inspection and human-owned policy decision

The author supplied the policy boundary before implementation: for this exact idempotent endpoint and stable identity contract, `409` means "already created." That direction supports the bounded return path. It explicitly does not support a shared `409` success rule, a conflict range, or another endpoint. Independent review must still replay the package, try to refute patch minimality, and compare any later Chapter 4 transcript integration with this evidence before the ledger moves to `Pass`.
