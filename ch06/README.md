# Chapter 6 role-relay validator support

This internal package keeps the complete green validator, the independent tester artifact, the broader suite, the thin command-line runner, and the verified Boolean-as-integer capture together. It is self-contained: copy this directory anywhere with Python and pytest available, then run the commands below from the copied directory.

## Files

- `validator.py` is the final green implementation.
- `test_validator.py` contains the eight maintained broader checks.
- `test_bool_is_not_accepted_as_int.py` is the reader-facing focused tester listing and standalone green check.
- `cli.py` is the thin command-line runner.
- `schema.json` and `config.json` are generic maintained fixtures for the exact valid command printed in the chapter.
- `invalid_config.json` changes the integer field to a Boolean so the same runner proves validation exit status `1`.
- `pytest.ini` limits top-level pytest discovery to `test_validator.py` and excludes `captures/`.
- `captures/boolean_as_integer_role_handoff/` preserves the red fixture, exact patch, role artifacts, evidence, and replay runner.

## Role artifacts

| Role | Maintained artifacts | What they establish |
|---|---|---|
| Tester | Capture test, focused red evidence, and the contract, observation, and plan in `session.md` | The permissive before state accepts `True`, and the case detects it before editing in the captured Claude Code session |
| Implementer | `patches/strict-int.patch`, focused green, broader green, and the action record in `session.md` | The same Claude Code session changes one predicate under the selected policy and records the focused plus neighboring checks |
| Verifier | `metadata.json` under `integration_review_receipt.verdict` and the review gate in `parity.md` | A later maintained integration-review receipt accepts the evidence, scope, minimality, and policy boundary; it is not a separate verifier transcript |

## Verify the green package

Run from this directory:

```bash
python3 cli.py --schema schema.json --config config.json
python3 cli.py --schema schema.json --config invalid_config.json
python3 -m pytest -q
python3 test_bool_is_not_accepted_as_int.py validator.py
```

The valid command should print `ok` and exit `0`. The invalid command should print `service.port: expected int` and exit `1`. The pytest run should report eight passing tests. The focused handoff should report `PASS`. Pytest does not collect capture internals; those files are exercised only by the replay command.

## Replay the captured repair

```bash
python3 captures/boolean_as_integer_role_handoff/run_capture.py
```

Replay removes stale work before preflight, creates disposable red and repaired states inside the capture, compares them with the stored evidence, verifies every top-level executable artifact and the independent-review receipt by checksum, and removes its working directory on success or failure. It does not import repository-root code, inspect another chapter, rewrite evidence, or replace the top-level green implementation.

## Chapter listing map

- Listing 6.1 is a presentation composite. Its formatting follows top-level `validator.py`, while its permissive `int` predicate comes from the captured before state. The top-level file keeps the accepted strict predicate.
- Listing 6.2 excerpts four contract-derived cases from top-level `test_validator.py`.
- Listings 6.3 and 6.4 together match top-level `test_bool_is_not_accepted_as_int.py`. The capture copy is behaviorally identical but retains the original capture docstring and usage-line wrapping.
- Listing 6.5 matches top-level `cli.py` with no intentional code difference.

See `captures/boolean_as_integer_role_handoff/parity.md` for the complete printed-artifact, command-normalization, evidence, and certification mapping. The package-level independent review is retained at `captures/boolean_as_integer_role_handoff/evidence/independent-review.md`; it is separate from the verifier-role receipt printed in the chapter.

## Remaining limitations

- The validator supports only strings, exact built-in integers, Booleans, dictionaries, and exact built-in floating-point values.
- Arrays, coercion, custom messages, and validation of unknown configuration keys remain out of scope.
- The public function expects the schema and nested `fields` values to be mappings; malformed container shapes can still raise runtime exceptions.
- The command-line runner lets file, permission, and malformed JSON errors propagate.
- The tests do not exhaust numeric subclasses, deeply malformed schemas, or every nested configuration shape.
- The capture proves only the Boolean-as-integer repair and does not choose the product's schema policy.
