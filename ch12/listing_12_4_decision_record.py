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
            "current_practice_minutes": 71,
            "bounded_workflow_minutes": 55,
            "proposed_gain_percent": 15,
            "threshold_status": "unapproved",
            "observation": "proposed_gain_cleared",
        },
        "nonaccepted_terminal_minutes": {
            "current_practice": 46,
            "bounded_workflow": 73,
        },
        "accepted_without_major_rework": {
            "current_practice": "24/30",
            "bounded_workflow": "25/30",
            "band_status": "unresolved",
        },
        "escaped_defects": {
            "current_practice": "1/24 accepted",
            "bounded_workflow": "2/25 accepted",
            "band_status": "unresolved",
        },
        "authority_exceptions": 2,
    },
    "reason": "authority_stop_condition_triggered",
    "owner": "workflow_owner",
    "next_review": "after_exception_repair",
    "rollout_authorized": False,
}
