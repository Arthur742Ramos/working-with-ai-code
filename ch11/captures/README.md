# Controlled deployment-policy capture

The maintained deployment configuration is safe. The file
`deployment_policy_value/before/deployment.json` preserves the one-line red
state used for the real agent session: `max_unavailable` is `2` instead of
the approved maximum `1`.

To reproduce the red result without changing the maintained configuration,
copy the fixture over `deployment.json` in a disposable worktree, run the
focused test, restore `deployment.json`, and rerun the same test. The real
capture followed that sequence directly: the working configuration started
red, the agent changed one value, and the focused and full suites went green.
The maintained `test_deployment_guard.py` also reads this fixture directly and
asserts it is exactly one policy violation.

The policy value is a human-owned operating decision. The test establishes two
facts: the configuration contains a value, and the deterministic policy either
accepts or rejects it. It does not decide how much production capacity the
service needs.

`session-transcript.md` preserves the sanitized runtime, read scope, exact red
output, approved diff, and green outputs from the real capture. The maintained
suite can gain unrelated hardening tests without rewriting the historical
count.
