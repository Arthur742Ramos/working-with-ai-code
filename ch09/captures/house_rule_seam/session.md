# Session record: house-rule HTTP seam

## Provenance

This record comes from a real Claude Code session begun on 2026-07-14 and completed on 2026-07-15. The harness reported Claude Code version `2.1.210.642` and model `gpt-5.6-sol[1m]`. The transcript is condensed from tool logs. Source inspection, commands, raw output, exit statuses, the machine-generated diff, and observable agent actions are retained.

## Human contract

The inspection contract below was reconstructed during the red-only stage from the approved restructuring architecture, the maintained Chapter 9 contract, and the bounded candidate slice. It is not presented as a retained quotation from the author or a vendor transcript.

> Inspect `alerts.py`, the focused alert-routing test, and the executable house-rule guard. Run the focused routing test against the staged before state before editing. The bounded behavior is that `send_alert` must route through `http_client.call` with the existing method, URL, and JSON payload; the broader guard must still reject `requests` or another direct transport. Report genuine red and the smallest-reviewable-change plan. Preserve readable surrounding idiom rather than optimizing for changed-line count. Do not weaken the tests, add dependencies, or edit canonical files.

Original retained completion direction, condensed without changing its policy:

> Complete the actual coding-agent session inside the staged package only. Verify genuine red first. Choose the best implementation without another approval checkpoint. Route outbound HTTP through the required shared client seam with no exception. Apply the smallest reviewable production diff in the surrounding style, preserve machine-generated evidence and actual actions, run focused and broader green, complete all package records, and add non-recording replay. Keep canonical chapter and code files unchanged.

## Agent inspection

The agent read the staged before source and guard before running the focused command.

- `before/alerts.py` imported `requests` on line 3, called `requests.post` directly, and read `response.status_code`.
- `tests/test_alerts.py` patched `http_client.call` before loading the feature and asserted the exact `POST` method, alert URL, and JSON body. Its in-memory `requests.post` stub let the dependency-free before fixture complete without making a network call. This observer accepts direct and module-qualified shared-client imports; an explicit module-qualified positive case protects that property.
- `tests/test_house_rules.py` parsed feature modules with Python's abstract syntax tree and rejected direct transport imports, while excluding the approved `http_client.py` boundary.
- Canonical `http_client.call` accepted the existing endpoint and JSON payload shape, required the HTTP method as its first argument, and returned `Response.status`.
- The remaining alert tests checked injected authentication, success status, and failure status through the maintained transport seam.

The staged direct-`requests` source checksum was `ad35f4f08f1b7d18b198d48a491dc0160a917233534bddabac05564cb0d5cd8e`. After the first independent review exposed import-shape overfitting, the behavior-level focused test checksum became `ec1dd662429f7d9ff7a42b1c9285729d75d659b7ade0b6237f432805ab120195`.

## Genuine focused red

Before creating `after/` or a patch, the agent ran the red-only replay. The runner copied the staged inputs into disposable space and executed the equivalent of:

```bash
PYTHONPATH=before HOUSE_RULE_ROOT=before \
  PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -q -p no:cacheprovider \
  tests/test_alerts.py::test_send_alert_routes_through_house_client
```

Exit status: `1`

Raw combined output:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
_________________ test_send_alert_routes_through_house_client __________________

    def test_send_alert_routes_through_house_client():
        try:
            accepted, calls = observe_shared_call()
>           assert_exact_shared_call(accepted, calls)

tests/test_alerts.py:72: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

accepted = True, calls = []

    def assert_exact_shared_call(accepted, calls):
        assert accepted is True
>       assert calls == [
            (
                "POST",
                ALERTS_URL,
                {"text": "disk 90% full"},
            )
        ], (
            "send_alert must route method, URL, and JSON "
            "through http_client.call"
        )
E       AssertionError: send_alert must route method, URL, and JSON through http_client.call
E       assert [] == [('POST', 'ht...k 90% full'})]
E         
E         Right contains one more item: ('POST', 'https://alerts.example.com/api/v1/send', {'text': 'disk 90% full'})
E         Use -v to get more diff

tests/test_alerts.py:57: AssertionError
=========================== short test summary info ============================
FAILED tests/test_alerts.py::test_send_alert_routes_through_house_client - As...
1 failed in 0.02s
```

Agent observation: the before implementation returned success through its direct transport, but the approved shared call recorded no method, URL, or JSON. The defect was executable routing, not merely the presence of a forbidden import. Because the observer patches `http_client.call` before loading the feature, either direct or module-qualified shared-client use reaches the same check.

## One-sentence smallest-reviewable-change plan

Replace only the direct `requests` import, `requests.post` call, and `status_code` access in `alerts.py` with `http_client.call`, the required `POST` method argument, and its `status` field, leaving the endpoint, payload, success threshold, shared client, guard, and unrelated behavior unchanged.

## Approval basis

The standing author direction allowed the agent to choose the exact implementation without another approval checkpoint. The slice's approval policy required outbound HTTP to use the shared client seam with no exception. The agent selected the three-line substitution because it is the narrowest behaviorally complete edit in the surrounding style: it keeps the response variable, makes the interface adaptation visible, and changes no unrelated control flow. A one-return-line rewrite may change fewer physical lines, but it expands review scope by changing the function's readable shape and hiding the `status_code` to `status` adaptation inside a call chain. This record does not claim that the author named or selected a menu option.

## Agent action record

The observable sequence is preserved in `evidence/agent-actions.md`. The original session read the governing standard and staged files, strengthened and manually reviewed the focused routing test, replayed genuine behavioral red, inspected the shared interface and maintained guard, retained the three-line production patch, ran focused green, ran genuine broader and canonical green, refreshed every dependent record, and completed recording and non-recording replay. After independent review, the certification repair replaced local-symbol interception with shared-call observation, added the module-qualified positive case, mapped the printed excerpt, and added cleanup and review-state invariants. Production code and the three-line patch remained unchanged.

## Exact applied diff

The system `diff` command generated `patches/house_rule_seam.patch`:

```diff
--- a/alerts.py
+++ b/alerts.py
@@ -1,10 +1,10 @@
 """Naive failing state for the deterministic house-rule reproduction."""
 
-import requests
+from http_client import call
 
 ALERTS_URL = "https://alerts.example.com/api/v1/send"
 
 
 def send_alert(message: str) -> bool:
-    response = requests.post(ALERTS_URL, json={"text": message})
-    return response.status_code < 400
+    response = call("POST", ALERTS_URL, json={"text": message})
+    return response.status < 400
```

The patch changes three production lines. A syntax-only import patch would leave alert delivery broken. A one-return-line rewrite would still need the approved import, method argument, and response-field adaptation while also replacing the function's existing two-step shape. The retained diff is therefore the smallest reviewable change: each changed line maps to one required interface substitution, and the response variable keeps the adaptation explicit. `http_client.py`, the endpoint, the payload, and the threshold remain byte-identical.

## Genuine focused green

After applying the stored patch in disposable space, the agent repeated the focused command.

Exit status: `0`

Raw combined output:

```text
.                                                                        [100%]
1 passed in 0.01s
```

## Genuine broader green

The first broader attempt exposed a capture setup omission rather than a production failure: the disposable test tree lacked the guard's own direct-transport fixture. That attempt exited `1` after eight passes and is preserved in `evidence/broader_green_setup_failure.txt`. The agent copied the byte-identical before fixture to `tests/fixtures/direct_requests/alerts.py` and reran the unchanged broader command:

```bash
PYTHONPATH=before HOUSE_RULE_ROOT=before \
  PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -q -p no:cacheprovider tests
```

Exit status: `0`

Raw combined output:

```text
..........                                                               [100%]
10 passed in 0.03s
```

## Genuine canonical support green

The agent also ran the maintained Chapter 9 support suite without changing it:

```bash
cd code/ch09 && PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -q -p no:cacheprovider
```

Exit status: `0`

Raw combined output:

```text
.........                                                                [100%]
9 passed in 0.01s
```

## Agent evidence boundary

Focused green proves that `send_alert` invokes the approved seam with the exact `POST` method, alert URL, and JSON payload. Broader green proves the package-local after state also receives injected authentication, handles success and failure status, preserves the client's retry and fail-closed behavior, rejects direct transport imports, keeps the guard self-test live, and accepts module-qualified shared-client use. Canonical green remains historical proof that the maintained support suite passed during the original session.

These checks do not prove a live alert service, credential validity, production transport behavior, backoff timing, or that the seam policy should apply in another system. They support this bounded implementation of an already-set trust policy.

## Author inspection and human-owned policy decision

Inspect the diff rather than its line count: the import names the approved boundary, the call preserves the existing endpoint and payload while adding the required method, and the final line adapts only the response field. Focused green proves those request arguments reach the approved seam; broader green protects authentication, status handling, retries, fail-closed behavior, and the direct-import guard. Neither check decides whether a failed alert should return `False`, raise, or trigger escalation. For this slice, the author direction settled only the bypass boundary: route outbound HTTP through the required seam with no exception. Service owners still own failure policy and any future redesign of the shared boundary.

Canonical `chapters/ch09.md` and the checksum-locked support files remained identical during the original session. The later certification repair updated the current chapter excerpt, package-local tests and records, and the final-code mirror only where review parity required; it did not change the captured production patch or historical support tree.
