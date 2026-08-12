# Working with AI as a Real Teammate — Companion Code

Code listings from the Manning book by Arthur Ramos.

Each chapter directory mirrors that chapter's printed listings. Chapters 1–5
present the printed listings as standalone, reader-facing files
(`listing_N_M_*`) alongside a `README.md` index and a `PROMPTS.md` of the
chapter's prompt blocks. Chapters 6–12 are self-contained, runnable teaching
projects with passing test suites; their `README.md` files map each printed
listing to the maintained source file it comes from. A `requirements.txt`
appears wherever a chapter uses third-party packages.

## Chapters

### Chapter 1 — Working with AI: from magic to engineering

- [`listing_1_1_rate_limiter_before.py`](ch01/listing_1_1_rate_limiter_before.py) — Listing 1.1: The rate limiter before the observability repair
- [`listing_1_2_focused_red.txt`](ch01/listing_1_2_focused_red.txt) — Listing 1.2: Genuine focused red for the missing signal
- [`listing_1_3_accepted_repair.diff`](ch01/listing_1_3_accepted_repair.diff) — Listing 1.3: The accepted one-line repair
- [`listing_1_4_green_evidence.txt`](ch01/listing_1_4_green_evidence.txt) — Listing 1.4: Focused and broader green evidence
- [`PROMPTS.md`](ch01/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 2 — Contracts that produce checkable work

- [`listing_2_1_contract_template.txt`](ch02/listing_2_1_contract_template.txt) — Listing 2.1: A compact contract for checkable work
- [`listing_2_2_local_fixture.py`](ch02/listing_2_2_local_fixture.py) — Listing 2.2: A fixed diff and deterministic local response
- [`listing_2_3_schema.py`](ch02/listing_2_3_schema.py) — Listing 2.3: JSON Schema for a PR description
- [`listing_2_4_generate_and_validate.py`](ch02/listing_2_4_generate_and_validate.py) — Listing 2.4: Generate, parse, and validate the result
- [`listing_2_5_github_formatting.py`](ch02/listing_2_5_github_formatting.py) — Listing 2.5: GitHub formatting and CLI entry point
- [`listing_2_6_retry.py`](ch02/listing_2_6_retry.py) — Listing 2.6: Conversational retry after validation failure
- [`PROMPTS.md`](ch02/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 3 — Conversations that converge

- [`listing_3_1_event_processor_start.py`](ch03/listing_3_1_event_processor_start.py) — Listing 3.1: Starting event processor
- [`listing_3_2_missing_events_guard.diff`](ch03/listing_3_2_missing_events_guard.diff) — Listing 3.2: Missing-events validation guard
- [`PROMPTS.md`](ch03/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 4 — Plans you can review and redirect

- [`listing_4_1_staged_execution_plan.txt`](ch04/listing_4_1_staged_execution_plan.txt) — Listing 4.1: Staged execution plan for the customer importer
- [`listing_4_2_walking_skeleton.py`](ch04/listing_4_2_walking_skeleton.py) — Listing 4.2: Walking skeleton for a dry-run-capable importer
- [`listing_4_3_idempotent_replay_test.py`](ch04/listing_4_3_idempotent_replay_test.py) — Listing 4.3: Focused test for an idempotent replay
- [`listing_4_4_bounded_replay_policy.diff`](ch04/listing_4_4_bounded_replay_policy.diff) — Listing 4.4: Exact diff for the bounded replay policy
- [`listing_4_5_migration_execution_contract.txt`](ch04/listing_4_5_migration_execution_contract.txt) — Listing 4.5: Staged execution contract for a user migration
- [`PROMPTS.md`](ch04/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 5 — Diagnosing failure under uncertainty

- [`listing_5_1_falsifiable_hypothesis.txt`](ch05/listing_5_1_falsifiable_hypothesis.txt) — Listing 5.1: A falsifiable hypothesis for a repeatable order failure
- [`listing_5_2_timestamp_parser.py`](ch05/listing_5_2_timestamp_parser.py) — Listing 5.2: A timestamp parser that passes common examples
- [`listing_5_3_structural_vs_behavior.py`](ch05/listing_5_3_structural_vs_behavior.py) — Listing 5.3: Structural assertions versus behavior assertions
- [`listing_5_4_per_item_lookup.py`](ch05/listing_5_4_per_item_lookup.py) — Listing 5.4: The per-item lookup in the shipped summary path
- [`listing_5_5_missing_product_repair.diff`](ch05/listing_5_5_missing_product_repair.diff) — Listing 5.5: The exact missing-product policy repair
- [`listing_5_6_query_plan_evidence.txt`](ch05/listing_5_6_query_plan_evidence.txt) — Listing 5.6: Order and query-plan evidence for the repeated scan
- [`PROMPTS.md`](ch05/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 6 — Roles that produce independent artifacts

- [`validator.py`](ch06/validator.py) — Listing 6.1: The coder's validator implementation (maintained green version)
- [`test_bool_is_not_accepted_as_int.py`](ch06/test_bool_is_not_accepted_as_int.py) — Listing 6.2: Independent focused test derived from the contract
- [`cli.py`](ch06/cli.py) — Listing 6.3: A thin command-line runner for the verified validator
- [`test_validator.py`](ch06/test_validator.py) — The eight maintained broader checks
- [`PROMPTS.md`](ch06/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 7 — Bounded agents and orchestration

- [`agent_loop.py`](ch07/agent_loop.py) — Listing 7.1: A minimal bounded tool-use loop
- [`validator.py`](ch07/validator.py) — Listing 7.2 target: the validator with strict `float` support
- [`test_agent_loop.py`](ch07/test_agent_loop.py) and [`test_validator.py`](ch07/test_validator.py) — the loop and validator suites
- [`PROMPTS.md`](ch07/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 8 — From checks to evaluations

- [`test_allocation.py`](ch08/test_allocation.py) — Listing 8.1: Two checks with different jobs, plus the behavior suite
- [`allocation.py`](ch08/allocation.py) — Listing 8.2 target: proportional allocation with exact `Fraction` residues
- [`test_golden.py`](ch08/test_golden.py) — Listing 8.3: Excerpt from the maintained allocation golden set
- [`PROMPTS.md`](ch08/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 9 — Context engineering: data, tools, and trust

- [`AGENTS.md`](ch09/AGENTS.md) — Listing 9.1: A short project rule with an enforcement point
- [`http_client.py`](ch09/http_client.py) — Listing 9.2: The response interface and alert call
- [`retrieval.py`](ch09/retrieval.py) — Listing 9.3: Retrieve, preserve provenance, then inject
- [`alerts.py`](ch09/alerts.py) — the house-correct alert feature that uses `http_client.call`
- [`mcp_policy.py`](ch09/mcp_policy.py) — host-owned MCP capability policy
- [`test_mcp_policy.py`](ch09/test_mcp_policy.py) — posture and lethal-trifecta checks
- [`parity.md`](ch09/parity.md) — the Chapter 9 listing-to-source map
- [`PROMPTS.md`](ch09/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 10 — Software engineering: from idea to review-ready code

- [`reminders/service.py`](ch10/reminders/service.py) — Listing 10.1: Keeping snooze policy inside the service
- [`tests/test_service.py`](ch10/tests/test_service.py) — Listing 10.2: Proving policy with a fake and frozen clock
- [`tests/test_sqlite_repository.py`](ch10/tests/test_sqlite_repository.py) — Listing 10.3: Crossing the real SQLite row boundary
- [`tests/test_capture_controls.py`](ch10/tests/test_capture_controls.py) — capture cleanup and review-state controls
- [`manual_check.py`](ch10/manual_check.py) — Listing 10.4: Comparing local responses with storage
- [`captures/sqlite_row_conversion_seam/`](ch10/captures/sqlite_row_conversion_seam/) — the current SQLite row-conversion session fixture
- [`PROMPTS.md`](ch10/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 11 — Automation and operations: from proposal to production evidence

- [`deployment_guard.py`](ch11/deployment_guard.py) — Listing 11.1: Rollout-policy branch for unavailable capacity
- [`pipeline.py`](ch11/pipeline.py) — Listing 11.2: Stopping the pipeline at the approval boundary
- [`incident_triage.py`](ch11/incident_triage.py) — Listing 11.3: Selecting one deployment's events in time order (and printing Listing 11.4)
- [`listing_11_5.txt`](ch11/listing_11_5.txt) — Listing 11.5: A post-change evidence packet
- [`PROMPTS.md`](ch11/PROMPTS.md) — Prompt blocks from the current manuscript draft

### Chapter 12 — Measuring and governing AI-assisted work

- [`workflow_metrics.py`](ch12/workflow_metrics.py) — Listing 12.3 target: the green metric that counts every terminal attempt
- [`test_workflow_metrics.py`](ch12/test_workflow_metrics.py) — Listing 12.2: Failed attempts remain in the denominator
- [`listing_12_3_terminal_denominator.diff`](ch12/listing_12_3_terminal_denominator.diff) — Listing 12.3: Counting terminal attempts in the denominator
- [`listing_12_4_decision_record.py`](ch12/listing_12_4_decision_record.py) — Listing 12.4: A reviewable workflow decision record
- [`captures/before/workflow_metrics.py`](ch12/captures/before/workflow_metrics.py) — Listing 12.1: the defective before-state metric
- [`PROMPTS.md`](ch12/PROMPTS.md) — Prompt blocks from the current manuscript draft

Chapters 6 through 12 are runnable projects with passing test suites. From the
chapter directory, run `python3 -m pytest -q`:

- `ch06` prints `8 passed`,
- `ch07` prints `13 passed`,
- `ch08` prints `10 passed`,
- `ch09` prints `28 passed`,
- `ch10` prints `53 passed` (49 behavior checks plus four capture controls),
- `ch11` prints `24 passed`, and
- `ch12` prints `4 passed` (equivalently, `python3 -m unittest -v test_workflow_metrics`).

Chapters 6, 7, 8, 9, 11, and 12 document their deterministic red-to-green
exercises under each chapter's `captures/README.md`; Chapter 10 documents its
controlled reproductions in [`ch10/captures/README.md`](ch10/captures/README.md).

## Running the Code

Chapters 6 through 12 (and Chapter 2, for `jsonschema`) declare their
dependencies:

```bash
pip install -r ch02/requirements.txt \
    -r ch06/requirements.txt \
    -r ch07/requirements.txt \
    -r ch08/requirements.txt \
    -r ch09/requirements.txt \
    -r ch10/requirements.txt \
    -r ch11/requirements.txt \
    -r ch12/requirements.txt
```

Chapter 1 listings are excerpts and captured evidence. Chapters 3, 4, and 5
listings are standalone Python, text, and diff files that mirror the printed
listings; they need no third-party packages. Chapter 2's printed listings run
offline through a deterministic local fixture (Listing 2.2), so no model
provider or API key is required; only `jsonschema` is needed.

Chapters 6 through 12 are self-contained, runnable projects. Each needs only
`pytest`; from the chapter directory, run `python3 -m pytest -q`. Chapters 10,
11, and 12 use CPython 3.11 or newer.

The provider-neutral [`llm_client.py`](llm_client.py) helper remains available
for readers who want to wire a listing to a live model, but the printed
listings in this edition run without one.

## License

MIT
