"""Listing 4.3: Focused test for an idempotent replay

From "Working with AI as a Real Teammate" (Manning)
Chapter 4

Excerpt: `parse_customer`, `send_with_retry`, and `fake_sender` are defined
in the importer and its test harness.
"""

def test_conflict_is_idempotent_replay():
    raw = {
        "source_id": "C-1",
        "email": "x@y.co",
        "name": "X",
    }
    row = parse_customer(raw)
    result = send_with_retry(
        row,
        fake_sender(409),
        attempts=3,
    )
    assert result.status == 409
