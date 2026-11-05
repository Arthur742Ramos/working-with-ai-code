from idempotency_probe import run_probe


def test_service_with_distinct_conflict_status_rejects_changed_payload():
    assert run_probe(422) == {
        "statuses": [201, 409, 422],
        "conflicting_payload_accepted": False,
        "stored_customers": 1,
    }


def test_service_that_reuses_409_exposes_the_importers_assumption():
    assert run_probe(409) == {
        "statuses": [201, 409, 409],
        "conflicting_payload_accepted": True,
        "stored_customers": 1,
    }
