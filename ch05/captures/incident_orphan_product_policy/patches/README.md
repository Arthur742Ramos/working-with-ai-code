# Patch status

`missing-product-policy.diff` is the machine-generated unified diff between immutable `before/server.py` and the disposable after-state that passed both green commands.

The patch contains only three required production responsibilities:

- Define the stable `MissingProductError` type.
- Raise it with order and product context before price calculation.
- Map it to the selected fail-closed `422` API response.

A provisional catch also duplicated timing and logging. The minimality review rejected those lines before the final patch was recorded. Removing any remaining hunk breaks either the focused domain behavior or the broader API-boundary behavior.

The handler deliberately keeps `self._send(...)` and `return` on separate lines. That form matches the surrounding early-exit idiom and separates the response side effect from control flow. Replacing it with `return self._send(...)` would remove one changed line, but it would make the code denser without narrowing behavior or scope. The approved patch is the smallest reviewable change, not the fewest-line spelling.

The runner applies this patch only inside `.work`, regenerates the unified diff, compares it byte-for-byte, and removes the disposable directory. It never applies the patch to the top-level final package.
