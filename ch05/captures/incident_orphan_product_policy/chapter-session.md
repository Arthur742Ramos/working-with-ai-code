# Real session: Turning an orphaned row into a named failure

Order `7` fails every time you rebuild the incident database. The deterministic seed has removed the mystery, but the application still reports a container error instead of the broken relationship. A repeatable crash is evidence. It is not yet a diagnosis.

*The exchange below comes from a real session with a coding agent (Claude Code 2.1.210) acting on `server.py` and its tests. The transcript is condensed from tool logs. Commands, output, exit statuses, and the diff come directly from the verified session evidence.*

The inspection contract was reconstructed from the retained author direction and staged incident evidence. It is not presented as a verbatim prompt.

> [!prompt Name the orphaned-product failure]
> Inspect `seed.py`, `server.py`, and the focused check. Run the focused check before editing, and do not edit until you have observed the failure and stated a one-sentence plan. When an order contains a product code absent from the catalog, require a named `MissingProductError` that identifies the order and missing code. Fail the summary closed at the API boundary while upstream data is repaired. Do not change valid summaries or invent a price for the missing product.

> [!ai-response Red evidence and bounded plan]
> I inspected the deterministic seed and the summary path. Order `7` contains one orphaned line: product code `90233`, quantity `2`. `lookup_product()` returns `None`, and `build_summary()` immediately reads `product["price"]`.
>
> I ran the focused check before editing:
>
> ```text
> python3 tests/test_orphan_policy.py .work
> DETERMINISTIC SEED: order=7 code=90233 qty=2
> FAIL: test_seeded_orphan_uses_explicit_missing_product_policy
> expected: MissingProductError: order 7 references missing product 90233
> observed: TypeError: 'NoneType' object is not subscriptable
> ```
>
> Exit status: `1`.
>
> The seed reaches the suspected missing row, but the implementation exposes an accidental Python error rather than a stable domain failure with order and product context.
>
> Plan: add `MissingProductError`, guard the missing lookup before price calculation, and map that exception to one fail-closed API response without changing valid summaries or upstream data.

The standing author direction allowed the agent to choose the bounded implementation without another approval checkpoint. The fail-closed policy was already settled. The agent selected `422` because the request is well formed but the referenced resource state cannot produce a trustworthy summary. The author did not name that status.

> [!ai-response Exact repair and green checks]
> I applied the following machine-generated diff:
>
> ```diff
> --- a/server.py
> +++ b/server.py
> @@ -36,6 +36,10 @@
>  _log_file = open(LOG_PATH, "a", buffering=1)
>  
>  
> +class MissingProductError(Exception):
> +    pass
> +
> +
>  def log(line):
>      ts = time.strftime("%Y-%m-%dT%H:%M:%S")
>      msg = "%s %s" % (ts, line)
> @@ -106,6 +110,11 @@
>      # each an unindexed full scan.
>      for item in items:
>          product = lookup_product(con, item["code"])
> +        if product is None:
> +            raise MissingProductError(
> +                "order %d references missing product %d"
> +                % (order_id, item["code"])
> +            )
>          price = product["price"]
>          line_total = price * item["qty"]
>          total += line_total
> @@ -184,6 +193,9 @@
>  
>          try:
>              summary, hit = get_summary(order_id)
> +        except MissingProductError as exc:
> +            self._send(422, {"error": str(exc)})
> +            return
>          except Exception as exc:
>              elapsed = (time.time() - start) * 1000
>              tb = traceback.format_exc()
> ```
>
> I reran the focused check:
>
> ```text
> python3 tests/test_orphan_policy.py .work
> DETERMINISTIC SEED: order=7 code=90233 qty=2
> PASS: test_seeded_orphan_uses_explicit_missing_product_policy
> observed: MissingProductError: order 7 references missing product 90233
> ```
>
> Exit status: `0`.
>
> I then ran the broader check:
>
> ```text
> python3 tests/test_orphan_policy_broader.py .work
> PASS: test_neighboring_valid_order_unchanged
> PASS: test_orphan_fails_closed_at_api_boundary
> ```
>
> Exit status: `0`.
>
> Focused green proves that this deterministic orphan raises the exported `MissingProductError` with the expected runtime type and message before total calculation. Broader green protects one valid summary and drives the real handler path to the selected `422` response. These checks do not establish the final public status, cover every corruption shape, prove cache or concurrency behavior, or repair upstream referential integrity.

Inspect the last hunk before accepting the green output. The handler calls `_send()`, then returns on the next line, matching the early-exit idiom around it. Collapsing those operations into `return self._send(...)` would remove one changed line, but it would make a side effect look like a returned value and buy no clearer behavior. This is the smallest reviewable diff: each hunk owns one required responsibility, and the control flow stays readable in context. The workflow turned an accidental `TypeError` into a falsifiable domain failure and checked one neighboring success path. It did not decide whether `422` is the right public contract or how orphaned references should be prevented. The owning team still sets those boundaries.
