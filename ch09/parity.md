# Chapter 9 companion parity

This map keeps the reader-facing Chapter 9 examples executable without
depending on the book repository or any private capture location.

| Chapter surface | Companion source | Check |
|---|---|---|
| Listing 9.1 outbound rule | `AGENTS.md` | `test_house_rules.py` rejects direct transport imports |
| Listing 9.2 shared HTTP seam | `http_client.py` | `test_http_client.py` covers auth, retry, and fail-closed behavior |
| Alert repair | `alerts.py`, `test_alerts.py` | Exact method, URL, payload, and status behavior are observed |
| Listing 9.3 retrieval flow | `retrieval.py`, `test_retrieval.py` | Provenance, capped selection, and required-source recall stay visible |
| MCP resources, prompts, and tools | `mcp_policy.py`, `test_mcp_policy.py` | Host selection, postures, approvals, and target allowlists are checked |
| Lethal-trifecta containment | `mcp_policy.py`, `test_mcp_policy.py` | One tool and one composed host cannot complete all three legs |
| Real alert seam session | `captures/house_rule_seam/` | Red state, exact patch, transcript, and replay remain package-local |

The MCP model is intentionally a policy example, not an MCP protocol
implementation. The capture transcript uses only public companion paths and
generic endpoint data.
