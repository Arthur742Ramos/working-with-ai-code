# House-rule seam session

This public transcript preserves the bounded alert-routing repair without
depending on private repository paths or credentials.

## Contract

Inspect the alert feature, its focused routing test, the import guard, and the
shared client. Run the focused check against the direct-transport before state.
Require the existing method, endpoint, and JSON payload to cross
`http_client.call`. Keep the change in the feature file.

## Focused red

```text
$ python3 -m pytest -q -p no:cacheprovider \
  tests/test_alerts.py::test_send_alert_routes_through_house_client
F                                                                        [100%]
FAILED tests/test_alerts.py::test_send_alert_routes_through_house_client
1 failed
```

The direct transport returned success, but the shared observer recorded no
method, endpoint, or JSON payload. The smallest plan was to replace the
transport import, call expression, and response field.

## Exact repair

```diff
-import requests
+from http_client import call

-    response = requests.post(ALERTS_URL, json={"text": message})
-    return response.status_code < 400
+    response = call("POST", ALERTS_URL, json={"text": message})
+    return response.status < 400
```

## Green evidence

```text
$ python3 -m pytest -q -p no:cacheprovider \
  tests/test_alerts.py::test_send_alert_routes_through_house_client
.                                                                        [100%]
1 passed

$ python3 -m pytest -q -p no:cacheprovider
.........                                                               [100%]
9 passed
```

Focused green proves exact routing at the seam. The broader run protects the
injected credentials, retry and fail-closed behavior, status handling, and
import guard. It does not prove live endpoint availability or production
transport behavior.
