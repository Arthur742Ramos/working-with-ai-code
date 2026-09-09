# Chapter 9 final support package

This internal package keeps the green shared-client alert seam, the complete retrieval example, a bounded Model Context Protocol (MCP) policy model, deterministic tests, and the verified house-rule capture together. The directory is self-contained and can be copied to an isolated location without the repository root or another chapter.

## Files

- `AGENTS.md` is the short outbound-HTTP rule shown in the staged chapter.
- `alerts.py` is the green feature implementation. It routes the existing method, endpoint, and JSON payload through `http_client.call`.
- `http_client.py` is the complete injectable boundary behind the staged interface excerpt.
- `test_alerts.py`, `test_http_client.py`, and `test_house_rules.py` check exact routing, credentials, status handling, retries, fail-closed behavior, and the import guard.
- `retrieval.py` preserves the staged retrieve-then-inject flow and adds a deterministic local store plus `recall_at_k` measurement.
- `test_retrieval.py` checks provenance, selection, the four-chunk limit, prompt injection, and partial versus complete recall.
- `mcp_policy.py` models host-selected resources and prompts plus read, propose, and apply tool postures. It rejects the lethal trifecta within one tool or across the host's composed toolset.
- `test_mcp_policy.py` checks host selection, all three postures, explicit approval, target allowlists, and lethal-trifecta containment.
- `parity.md` maps every staged code and session surface to its package-local maintained source and records intentional differences.
- `test_package_parity.py` checks the staged rule, alert repair, parity map, replay locality, and pytest discovery boundary.
- `pytest.ini` limits top-level discovery to maintained green tests and excludes capture internals.
- `captures/house_rule_seam/` preserves the immutable direct-transport red state, exact three-line repair, raw evidence, and package-local replay runner.

## Verify the final package

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  -p no:cacheprovider
```

The expected result is twenty-eight passing tests. `pytest.ini` prevents recursive collection of the capture's test-shaped internals, so the top-level suite stays green while capture replay retains and exercises the intentional red before-state. No test makes a live network call or invokes a model.

## Replay the captured repair

Run from this directory:

```bash
python3 captures/house_rule_seam/run_capture.py
```

Replay reconstructs the red and repaired alert states in disposable package-local space, verifies the stored patch and original evidence, runs focused and broader capture checks, runs the final top-level suite, checks package-local parity records, and removes temporary work. Default replay does not rewrite evidence.

The capture metadata retains the repository commit, canonical checksums, and canonical-support green output from the original session as historical provenance. Replay verifies those records as stored evidence only. It does not locate or execute canonical chapter files, repository support code, other chapters, graphics, or Box.

## Dependencies

- Python 3
- pytest
- the system `patch` command

No command requires a model SDK, network access, repository-root configuration, or a third-party HTTP client.

## Remaining limitations

- The alert tests use an injected transport. They do not prove live endpoint availability, credential validity, production backoff timing, or observability.
- The local retriever ranks lexical token overlap rather than production embeddings, metadata filters, hybrid search, or reranking.
- `recall_at_k` assumes evaluators already labeled the required source identifiers. It does not score whether a model used the evidence correctly.
- The MCP policy model demonstrates host-owned boundaries. It is not a networked MCP client or server and does not implement protocol transport, discovery, authentication, or schema negotiation.
- Tool approval and target checks run in one process. Production systems still need durable audit records, credential isolation, redaction, recovery, and post-action verification.
- Host-level rejection prevents the three capabilities from coexisting in this modeled host. It does not prove that a larger system cannot reconnect the circuit across several hosts or sessions.
- The capture proves one bounded shared-client repair. It does not make that trust policy portable to another system.
