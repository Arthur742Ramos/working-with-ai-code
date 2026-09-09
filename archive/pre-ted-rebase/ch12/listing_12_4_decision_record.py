"""Listing 12.4: A reviewable workflow decision record

From "Working with AI as a Real Teammate" (Manning)
Chapter 12

A compact decision record for the mixed scorecard. It records the action and
the evidence boundary without pretending that code made the judgment.
"""

decision = {
    "workflow": "bounded_python_test_repair",
    "current_scope": "current_practice",
    "action": "pause",
    "evidence": {
        "time_to_acceptance": {
            "current_minutes": 71,
            "bounded_minutes": 55,
            "proposed_gain_percent": 15,
            "threshold": "unapproved",
        },
        "nonaccepted_minutes": {
            "current": 46, "bounded": 73,
        },
        "accepted_without_rework": {
            "current": "24/30", "bounded": "25/30",
            "band": "unresolved",
        },
        "escaped_defects": {
            "current": "1/24", "bounded": "2/25",
            "band": "unresolved",
        },
        "authority_exceptions": 2,
    },
    "reason": "authority_stop_condition_triggered",
    "owner": "workflow_owner",
    "next_review": "after_exception_repair",
    "rollout_authorized": False,
}
