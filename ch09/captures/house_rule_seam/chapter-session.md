# Publication-ready Chapter 9 session

The exchange below comes from a real session with a coding agent (Claude Code) acting on `alerts.py` and `test_alerts.py`. The transcript is condensed from tool logs. The commands, failing output, changed lines, and green output are reproduced from the verified session evidence.

The inspection contract was reconstructed from the retained author direction and the bounded session record. It is not presented as a verbatim prompt.

> [!prompt Inspect the seam before editing]
> Inspect `alerts.py`, the focused alert-routing test, the executable house-rule guard, and the shared client interface. Before editing, run the focused test against the staged before state. Require `send_alert` to route the existing method, URL, and JSON payload through `http_client.call`, while the broader guard still rejects `requests` and any other direct transport. Report genuine red and the smallest-reviewable-change plan. Preserve readable idiom; do not weaken tests, add dependencies, or edit canonical files.

> [!ai-response Captured response 1 of 5: genuine focused red]
> I read the staged source, the focused routing test, the guard, and the shared client interface. I then ran the focused behavior test against the before state:
>
> ```text
> $ PYTHONPATH=before HOUSE_RULE_ROOT=before \
>   PYTHONDONTWRITEBYTECODE=1 \
>   python3 -m pytest -q -p no:cacheprovider \
>   tests/test_alerts.py::test_send_alert_routes_through_house_client
> F                                                                        [100%]
> =================================== FAILURES ===================================
> _________________ test_send_alert_routes_through_house_client __________________
>
>     def test_send_alert_routes_through_house_client():
>         try:
>             accepted, calls = observe_shared_call()
> >           assert_exact_shared_call(accepted, calls)
>
> tests/test_alerts.py:72: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> accepted = True, calls = []
>
>     def assert_exact_shared_call(accepted, calls):
>         assert accepted is True
> >       assert calls == [
>             (
>                 "POST",
>                 ALERTS_URL,
>                 {"text": "disk 90% full"},
>             )
>         ], (
>             "send_alert must route method, URL, and JSON "
>             "through http_client.call"
>         )
> E       AssertionError: send_alert must route method, URL, and JSON through http_client.call
> E       assert [] == [('POST', 'ht...k 90% full'})]
> E         
> E         Right contains one more item: ('POST', 'https://alerts.example.com/api/v1/send', {'text': 'disk 90% full'})
> E         Use -v to get more diff
>
> tests/test_alerts.py:57: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_alerts.py::test_send_alert_routes_through_house_client - As...
> 1 failed in 0.02s
> ```

> [!ai-response Captured response 2 of 5: diagnosis and plan]
> The before implementation returned success through its direct transport, but the shared `http_client.call` observer recorded no method, URL, or JSON. This red result targets executable routing, not merely the absence of `requests`. The same observer accepts direct or module-qualified shared-client use.
>
> Plan: Replace only the direct `requests` import, `requests.post` call, and `status_code` access in `alerts.py` with `http_client.call`, the required `POST` method argument, and its `status` field, leaving the endpoint, payload, success threshold, shared client, guard, and unrelated behavior unchanged.

The standing author direction allowed the agent to choose the exact implementation without another approval checkpoint. The policy for this slice was already settled: outbound HTTP had to use the shared client seam with no exception. The agent selected the three-line substitution as the smallest reviewable diff because the existing interface accepted the same request data and the maintained tests covered the response adaptation. Collapsing the function into one return expression would change its readable shape and hide that adaptation without reducing behavioral scope.

> [!ai-response Captured response 3 of 5: exact diff]
> I changed only the import, call expression, and response field:
>
> ```diff
> --- a/alerts.py
> +++ b/alerts.py
> @@ -1,10 +1,10 @@
>  """Naive failing state for the deterministic house-rule reproduction."""
>  
> -import requests
> +from http_client import call
>  
>  ALERTS_URL = "https://alerts.example.com/api/v1/send"
>  
>  
>  def send_alert(message: str) -> bool:
> -    response = requests.post(ALERTS_URL, json={"text": message})
> -    return response.status_code < 400
> +    response = call("POST", ALERTS_URL, json={"text": message})
> +    return response.status < 400
> ```

> [!ai-response Captured response 4 of 5: focused green]
> I reran the focused command after applying the patch:
>
> ```text
> $ PYTHONPATH=before HOUSE_RULE_ROOT=before \
>   PYTHONDONTWRITEBYTECODE=1 \
>   python3 -m pytest -q -p no:cacheprovider \
>   tests/test_alerts.py::test_send_alert_routes_through_house_client
> .                                                                        [100%]
> 1 passed in 0.01s
> ```

> [!ai-response Captured response 5 of 5: broader green]
> I then ran the broader maintained checks against the repaired state:
>
> ```text
> $ PYTHONPATH=before HOUSE_RULE_ROOT=before \
>   PYTHONDONTWRITEBYTECODE=1 \
>   python3 -m pytest -q -p no:cacheprovider tests
> ..........                                                               [100%]
> 10 passed in 0.03s
> ```
>
> Focused green proves that `send_alert` routes the exact `POST` method, alert URL, and JSON payload through the approved seam. Broader green proves that the repaired feature also receives injected authentication, handles success and failure status, preserves the client's retry and fail-closed behavior, rejects direct transport imports, keeps the guard self-test live, and accepts module-qualified shared-client use.
>
> These checks do not prove a live alert service, credential validity, production transport behavior, backoff timing, or that the seam policy should apply in another system.

Inspect the three changed lines rather than rewarding a lower line count. The import names the approved boundary, the call preserves the endpoint and payload while supplying the required method, and the final line makes the response-field adaptation visible. The focused check now observes those exact request arguments at the seam; broader green protects authentication, status handling, retries, fail-closed behavior, and the import guard. These checks do not decide whether a failed alert should return `False`, raise, or page a human. Service maintainers still set that policy. The agent's job was narrower: make the code obey the boundary already chosen.
