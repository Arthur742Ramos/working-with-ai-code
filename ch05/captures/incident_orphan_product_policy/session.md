# Session record: incident orphan-product policy

Status: complete through genuine red, exact patch, focused green, broader green, and non-recording replay.

## 1. Human contract

The original user direction required the agent to work only inside the staged capture package, verify genuine red before editing, preserve the actual action record, apply the smallest reviewable production diff to disposable state, record raw evidence and statuses, and leave the original capture source unchanged.

The approved behavior was:

> Raise a stable contextual `MissingProductError` and fail closed at the API boundary while upstream data is repaired.

The standing author direction also required the agent to choose the best implementation without another approval checkpoint. The author did not name an HTTP status or claim a specific response payload.

## 2. Bounded focused contract

The following focused clause was reconstructed from the approved behavior and staged incident evidence. It is not a verbatim vendor prompt:

> Given the deterministic incident seed, inspect the implementation and run the focused check before editing. When an order contains a product code absent from the catalog, require a named `MissingProductError` that identifies the order and missing code instead of an accidental generic exception. Do not edit before observing red.

## 3. Agent inspection

The agent read the staged `seed.py`, `server.py`, and focused test. The staged seed uses random seed `1729`, inserts product codes `1` through `40000`, and gives every seventh order one code at or above `90000`. The focused query found exactly one orphan for order `7`: product code `90233`, quantity `2`.

The staged `build_summary()` calls `lookup_product()`, receives `None`, and immediately evaluates `product["price"]`. The generic API exception handler then turns the accidental exception into `500`, so no named domain seam or selected fail-closed mapping exists.

## 4. Genuine red

The agent first ran the existing replay command from the package against a disposable `.work` copy. The focused command was:

```bash
python3 tests/test_orphan_policy.py .work
```

Raw output:

```text
DETERMINISTIC SEED: order=7 code=90233 qty=2
FAIL: test_seeded_orphan_uses_explicit_missing_product_policy
expected: MissingProductError: order 7 references missing product 90233
observed: TypeError: 'NoneType' object is not subscriptable
```

Exit status: `1`

No output normalization was applied.

## 5. Agent observation

The red result discriminates the selected behavior. The deterministic input reaches the missing catalog row, but the implementation exposes a Python container error rather than a stable domain failure that names the affected order and product code.

## 6. One-sentence plan

Add `MissingProductError`, guard the missing lookup before price calculation, and map that exception to one fail-closed API response without changing valid summaries or upstream data.

## 7. Approval basis and selected policy

The production edit proceeded under the author's standing direction to choose the best implementation and the explicit approval to raise a contextual domain error and fail closed. The agent selected `422` because the request shape is valid but the current referenced resource state cannot produce a trustworthy summary. This status was the agent's implementation choice, not an author-named option.

The upstream repair remains outside this bounded session. The patch neither changes product data nor invents a price for the orphaned line.

## 8. Actual agent action record

1. Read the capture standard, staged fixture, focused test, red evidence, and package records.
2. Replayed the stored red from an immutable copy and observed exit status `1`.
3. Copied `before/server.py` and `before/seed.py` into disposable `.work`.
4. Added the exception class, lookup guard, and a first `422` catch that duplicated timing and logging.
5. Generated a provisional diff. One shell wrapper attempt failed because `status` is read-only in `zsh`; the agent reran the same `diff` command with variable `rc`.
6. Ran the focused check green against the disposable after-state.
7. Refuted the provisional patch's minimality: the duplicate timing and logging were not required by the approved behavior. Removed those lines before recording the final patch.
8. Regenerated the machine diff and reran focused green.
9. Added one package-only broader check for the deterministic valid summary and real API boundary, then ran it green.
10. Replaced the red-only runner with full record and replay behavior and invoked `--record` to recreate red, apply and compare the exact patch, and store both greens.
11. Completed the session, metadata, README, patch note, and parity records, then invoked default replay without evidence writes.

This is a condensed action record derived from the actual tool sequence. It does not present reconstructed prose as a verbatim vendor quotation.

## 9. Exact applied diff

The final patch was generated by POSIX `diff -u` from the immutable before file and the disposable after-state:

```diff
--- a/server.py
+++ b/server.py
@@ -36,6 +36,10 @@
 _log_file = open(LOG_PATH, "a", buffering=1)
 
 
+class MissingProductError(Exception):
+    pass
+
+
 def log(line):
     ts = time.strftime("%Y-%m-%dT%H:%M:%S")
     msg = "%s %s" % (ts, line)
@@ -106,6 +110,11 @@
     # each an unindexed full scan.
     for item in items:
         product = lookup_product(con, item["code"])
+        if product is None:
+            raise MissingProductError(
+                "order %d references missing product %d"
+                % (order_id, item["code"])
+            )
         price = product["price"]
         line_total = price * item["qty"]
         total += line_total
@@ -184,6 +193,9 @@
 
         try:
             summary, hit = get_summary(order_id)
+        except MissingProductError as exc:
+            self._send(422, {"error": str(exc)})
+            return
         except Exception as exc:
             elapsed = (time.time() - start) * 1000
             tb = traceback.format_exc()
```

Each hunk is necessary for one approved responsibility: name the domain failure, detect it before calculating a plausible total, and fail closed at the API boundary. Removing any hunk fails either the focused or broader check. The rejected duplicate instrumentation is absent.

Within the handler hunk, `self._send(...)` and `return` remain separate because that form matches the surrounding early-exit idiom and distinguishes a response side effect from control flow. A one-line `return self._send(...)` spelling would remove one changed line, but it would make the code denser without narrowing behavior or scope. The final patch is the smallest reviewable diff, not a changed-line minimum.

## 10. Genuine focused green

Command:

```bash
python3 tests/test_orphan_policy.py .work
```

Raw output:

```text
DETERMINISTIC SEED: order=7 code=90233 qty=2
PASS: test_seeded_orphan_uses_explicit_missing_product_policy
observed: MissingProductError: order 7 references missing product 90233
```

Exit status: `0`

## 11. Genuine broader green

Command:

```bash
python3 tests/test_orphan_policy_broader.py .work
```

Raw output:

```text
PASS: test_neighboring_valid_order_unchanged
PASS: test_orphan_fails_closed_at_api_boundary
```

Exit status: `0`

## 12. Evidence boundary

The evidence proves the deterministic before failure, the exact production patch, the exported exception class name, the runtime exception type and message, one unchanged deterministic valid summary, and the selected `422` response through the real handler method. The observed runtime type is derived from `type(exc).__name__`. It does not prove that `422` is the final external contract, that all database corruption shapes are covered, that cached or concurrent requests behave correctly, or that upstream referential integrity is repaired.

## 13. Authorial inspection and human-owned decision boundary

Inspect the last hunk before accepting the green output. The handler calls `_send()`, then returns on the next line, matching the early-exit idiom around it. Collapsing those operations into `return self._send(...)` would remove one changed line, but it would make a side effect look like a returned value and buy no clearer behavior. This is the smallest reviewable diff: each hunk owns one required responsibility, and the control flow stays readable in context.

Look at what the workflow bought you: the accidental `TypeError` became a named, reproducible failure, and one neighboring success path constrained the repair. The checks do not decide whether `422` is the right public contract or how orphaned references should be prevented. The coding agent selected the concrete mapping under standing implementation authority; the owning team still sets the API and data-governance boundaries.
