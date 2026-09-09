"""Listing 2.2: A fixed diff and deterministic local response

From "Working with AI as a Real Teammate" (Manning)
Chapter 2
"""

import json


FIXED_DIFF = """diff --git a/app.py b/app.py
new file mode 100644
--- /dev/null
+++ b/app.py
@@ -0,0 +1,9 @@
+def validate_registration(payload):
+    errors = []
+    if "@" not in payload.get("email", ""):
+        errors.append("email is invalid")
+    if len(payload.get("password", "")) < 12:
+        errors.append("password is too short")
+    if len(payload.get("username", "")) < 3:
+        errors.append("username is too short")
+    return errors
"""

VALID_RESPONSE = {
    "title": "Validate registration fields",
    "summary": [
        "Validate email, password, and username",
        "Return all field errors together",
    ],
    "tests": [
        "Reject malformed email addresses",
        "Reject short passwords and usernames",
        "Reject missing or non-object request bodies",
    ],
    "risks": [
        "Non-object bodies need explicit handling",
        "Boundary lengths need product review",
    ],
}


def chat(messages,
         system=None,
         max_tokens=1024) -> str:
    if len(messages) == 1:
        return "not-json"
    correction = messages[-1]["content"]
    if "invalid" not in correction.lower():
        raise AssertionError(
            "retry omitted validation feedback")
    return json.dumps(VALID_RESPONSE)
