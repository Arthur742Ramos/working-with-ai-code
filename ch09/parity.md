# Chapter 9 package parity

This map binds the current staged Chapter 9 teaching surfaces to files in this isolated package. It is package-local by design: no command or test needs the repository root, canonical support code, another chapter, graphics, or Box.

## Staged teaching map

| Staged Chapter 9 surface | Package-local source | Parity boundary |
|---|---|---|
| Listing 9.1 outbound HTTP rule | `AGENTS.md` | The four rule lines match the staged listing: use `http_client.call`, forbid direct transports, inject tests, and enforce the guard. |
| Listing 9.2 `Response` and `call` interface | `http_client.py` | The complete implementation preserves the staged fields and signature, then supplies deterministic auth, retry, injection, and fail-closed behavior behind the excerpt. |
| Green alert repair in the captured session | `alerts.py`, `test_alerts.py`, `test_house_rules.py`, `test_http_client.py` | The final package routes the same `POST` method, endpoint, and JSON payload through the shared seam. The top-level suite is green. |
| Listing 9.3 illustrative skill shape | No executable package source | The listing teaches progressive disclosure as a compact illustrative file shape; it is not presented as maintained package code. |
| Listing 9.4 retrieve, preserve provenance, then inject | `retrieval.py`, `test_retrieval.py` | `format_evidence` and `answer` preserve the staged listing shape. The local store and recall checks are maintained extensions, not printed production architecture. |
| Retrieval evidence ceiling | `recall_at_k`, `all_required_at_k`, and their tests | The checks distinguish partial recall from all-required-evidence success. They do not score answer use. |
| MCP resources, prompts, and tools | `mcp_policy.py`, `test_mcp_policy.py` | The host selects capabilities, separates read, propose, and apply postures, requires approval for apply, and enforces target allowlists. |
| Lethal-trifecta containment | `Tool.__post_init__`, `MCPHost._reject_lethal_toolset`, and their tests | A single tool and a composed host toolset are both rejected when private-data access, untrusted content, and external communication complete the circuit. |
| Real shared-client session | `captures/house_rule_seam/` | The capture retains its original before state, exact patch, red evidence, focused green, broader green, publication transcript, and origin metadata. Replay operates only on copied package-local fixtures. |

## Intentional differences

- The staged `http_client.py` excerpt ends in an ellipsis. This package includes the complete deterministic implementation needed by the tests.
- The staged retrieval listing assumes an external store and model. This package adds a lexical in-memory store and a recording model in tests so the flow runs offline.
- The staged MCP section teaches architecture rather than a protocol listing. This package models the host-owned policy boundary only. It does not claim to implement MCP transport, discovery, authentication, or schema negotiation.
- The top-level `alerts.py` docstring describes the accepted green state. The capture's `after/alerts.py` retains the historical session wording, while its executable statements match the same repair.
- Capture metadata retains repository commit, canonical checksums, and the original canonical-support green output as historical provenance. Package replay verifies those records as stored data but does not locate or execute their former repository paths.

## Verification surfaces

Run the complete green suite from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  -p no:cacheprovider
```

`pytest.ini` limits discovery to the six top-level test modules and excludes `captures/`. The intentionally red before-state is exercised only by:

```bash
python3 captures/house_rule_seam/run_capture.py
```

Replay creates disposable working files inside the capture directory, proves focused red, applies the stored patch, proves focused and broader green, runs the package-local green suite, compares stored evidence, and cleans up.
