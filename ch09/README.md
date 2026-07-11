# Chapter 9 - Context engineering with executable house rules

This runnable sample shows why an agent needs repository context, not just a
better prompt. The feature is intentionally small: post an alert when a job
fails. A generic implementation might import `requests` and post directly.
That code is plausible, but wrong for this service because it bypasses the
approved client that owns authentication and retries.

The important surfaces are:

- **`AGENTS.md`** - the short, local contract a coding agent must follow.
- **`alerts.py`** - the final feature implementation. It uses only the
  approved `http_client.call` entry point.
- **`http_client.py`** - the narrow outbound-HTTP boundary. It adds
  authentication, retries transient failures without timing sleeps, accepts
  an injected transport for tests, and fails closed by default.
- **`test_house_rules.py`** - an AST-based repository guard. It rejects
  direct transport imports even when they use aliases or `from ... import`
  syntax, keeping policy enforcement outside the model.
- **`test_alerts.py`** and **`test_http_client.py`** - behavior, credential,
  retry, and no-network verification.
- **`fixtures/direct_requests/alerts.py`** - the checked-in failing state used
  by the chapter's red-to-green coding-agent session. It is scanned as source
  but never imported, so reproducing red needs neither `requests` nor a live
  endpoint.

## Setup and final green state

From the repository root:

```bash
python3 -m pip install -r ch09/requirements.txt
cd ch09
python3 -m pytest -q
```

Expected: `9 passed`. The suite makes no network calls and needs no real
credential.

## Deterministic red-to-green reproduction

The failing fixture is a real direct-`requests` implementation. Point the
house-rule test at it:

```bash
cd ch09
HOUSE_RULE_ROOT=fixtures/direct_requests \
  python3 -m pytest -q \
  test_house_rules.py::test_no_unapproved_http_clients
```

This deterministically fails with:

```text
alerts.py:3: unapproved outbound HTTP import: requests
```

No line number is fabricated: it refers to the checked-in fixture. The test
parses source without importing it, so `requests` is deliberately not a
dependency and no live request is attempted.

The minimal fix is the same change made in the final `alerts.py`:

```diff
-import requests
+from http_client import call
...
-    response = requests.post(ALERTS_URL, json={"text": message})
-    return response.status_code < 400
+    response = call("POST", ALERTS_URL, json={"text": message})
+    return response.status < 400
```

To verify the corrected source against the same guard without modifying the
repository:

```bash
tmpdir="$(mktemp -d)"
cp alerts.py "$tmpdir/alerts.py"
HOUSE_RULE_ROOT="$tmpdir" \
  python3 -m pytest -q \
  test_house_rules.py::test_no_unapproved_http_clients
rm -rf "$tmpdir"
```

Expected: `1 passed`. The final full suite remains green.

## What the example teaches

The instruction file gives the agent a local fact it could not learn from
public examples. The approved client grants only one narrow capability and
fails closed when no transport or credential is configured. The AST guard
then verifies the constraint independently of the agent. Together, those
surfaces demonstrate persistent context, explicit tools, least privilege,
and executable verification without relying on a model to remember policy.

See the [main README](../README.md) for the repository-wide index.
