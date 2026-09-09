# Session record: PR generator retry wiring

## Provenance

This record comes from a real Claude Code session begun on 2026-07-14 and completed on 2026-07-15. The harness reported Claude Code version `2.1.210.642` and model `gpt-5.6-sol[1m]`. The transcript is condensed from tool logs. Source inspection, commands, raw output, exit statuses, the exact diff, and observable agent actions are retained.

## Human contract

Original retained inspection contract:

> Candidate slice: The CLI bypasses the existing conversational retry path after malformed structured output.
>
> Inspect the staged source and test, run a genuine discriminating red command, record raw red output and exit status, write a one-sentence strict-smallest-change plan, identify the exact human-owned policy decision and a recommendation, and stop before any production repair or passing after implementation. Keep canonical chapters and canonical code unchanged. Keep every write inside the staged support directory.

Original retained completion direction, condensed without changing the policy:

> Complete the actual coding-agent session inside the staged package only. Verify the genuine red first. Reuse the existing retry helper unchanged: JSON and schema failures, two retries, three attempts total. Apply the strict smallest production diff, preserve machine-generated evidence, complete the package records, and add a non-recording replay mode. Keep canonical chapter and code files unchanged.

## Agent inspection

The staged `before/pr_generator.py` is byte-identical to canonical Chapter 2 support at repository commit `38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6`.

The module already defines `generate_with_retry()`. It catches both `json.JSONDecodeError` and `ValidationError`, appends the invalid reply as an assistant message, adds a user correction containing the validation detail, and loops over `range(max_retries + 1)`. Its default `max_retries=2` gives three attempts total.

The command-line entry point bypasses that helper. It calls `generate_pr_description(diff)`, which makes one adapter call and converts the first JSON or schema failure to `ValueError`.

## Genuine focused red

Before any staged production edit, the agent ran the package's non-recording replay. The runner copied `before/` into disposable `.work/` and executed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
tests/focused_test.py .work/pr_generator.py
```

Exit status: `1`

Raw combined output:

```text
FAIL: test_cli_retries_after_malformed_json
expected: CLI recovers after malformed JSON on the second chat call
observed: SystemExit: 1 after 1 chat call
stderr: Error: Invalid JSON: Expecting value: line 1 column 1 (char 0)
```

## Agent observation

The red result isolates the command-line wiring boundary. The process stops after one malformed reply even though the existing retry helper and a valid second reply are both available. JSON parsing works as written; the command-line path never reaches the conversation loop.

## Strict-smallest-change plan

Change only the command-line entry point in `pr_generator.py` to call `generate_with_retry(diff)` instead of `generate_pr_description(diff)`, leaving retry semantics and output formatting unchanged.

## Approval basis

The standing author direction allowed the agent to choose the best implementation without another approval checkpoint. The agent selected reuse of the existing helper unchanged because the defect is wiring and the helper already matches the bounded policy: retry JSON syntax and schema-validation failures, allow two retries, and stop after three attempts. This record does not claim that the author named or selected a menu option.

## Agent action record

The observable action sequence is preserved in `evidence/agent-actions.md`. In summary, the agent read the governing standard and staged files, replayed genuine red before editing, created a package-local after state, changed one production line, generated the patch with `diff`, ran focused and broader green checks, and validated recording plus non-recording replay. No canonical file was edited.

## Exact applied diff

The system `diff` command generated `patches/pr_generator_retry_wiring.patch`:

```diff
--- a/pr_generator.py
+++ b/pr_generator.py
@@ -160,7 +160,7 @@
         print("No staged changes found.", file=sys.stderr)
     else:
         try:
-            pr = generate_pr_description(diff)
+            pr = generate_with_retry(diff)
             print(format_for_github(pr))
 
             with open("pr_description.json", "w") as f:   #C
```

The patch changes one call site. `generate_with_retry()`, its exception classes, its retry count, and every other production line remain unchanged. A smaller behavioral patch is not available because replacing the called function name is the single required wiring operation.

## Genuine focused green

After applying the stored patch to disposable `.work/`, the runner repeated the focused command.

Exit status: `0`

Raw combined output:

```text
PASS: test_cli_retries_after_malformed_json
observed: CLI succeeded after 2 chat calls
```

## Genuine broader green

The runner then executed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
tests/broader_test.py .work/pr_generator.py
```

Exit status: `0`

Raw combined output:

```text
PASS: test_valid_first_response_stays_single_attempt
observed: CLI succeeded after 1 chat call
PASS: test_schema_failure_retries_with_feedback
observed: CLI succeeded after 2 chat calls
PASS: test_retry_exhaustion_stays_bounded
observed: CLI failed after 3 chat calls
3 passed
```

## Agent evidence boundary

The focused check proves that malformed JSON now reaches the existing correction loop and succeeds on the second reply. The broader check proves that valid output stays single-attempt, schema-invalid JSON receives feedback, and repeated malformed JSON stops after three calls. These deterministic stand-ins do not prove that a live model will comply, that the generated claims are true, or that retries should include transport failures.

## Author inspection and human-owned policy decision

The human-owned boundary is the retry policy itself: which failures merit another paid model call and how much retry budget the application may spend. For this slice, the agent applied the bounded policy stated in the completion direction and already encoded by the helper. The resulting evidence supports that implementation; it does not transfer the same policy to rate limits, authentication, network failures, or another workflow.

Canonical `chapters/ch02.md` and canonical files under `code/ch02/` remained checksum-identical throughout the session.

## Post-capture first-review repair

A later independent read-only review replayed the canonical package successfully but returned `Fail` at the publication gate. The first-review receipt is preserved in `evidence/first-independent-review.md`. The reviewer found that the shared mapping still selected a stale historical package, the chapter omitted the exact focused command, and the printed patch lost one space on a blank context line.

The shared mapping now selects this canonical package and remains intentionally `Pending`. The canonical and staged chapter sources print the exact focused command and preserve the patch whitespace byte-for-byte. Package replay now locks the failed-review receipt, rejects a false completed-review state, and checks cleanup residue. These repairs do not rewrite the original red, patch, or green evidence and do not convert the failed review into a Pass certification. A new independent review is still required.
