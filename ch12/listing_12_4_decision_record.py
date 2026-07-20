"""Listing 12.4: A reviewable workflow decision record

From "Working with AI as a Real Teammate" (Manning)
Chapter 12

A compact decision record for the mixed scorecard. It records the action and
the evidence boundary without pretending that code made the judgment.
"""

decision = {
    "workflow": "bounded_python_test_repair",
    "current_scope": "pilot_group",
    "action": "pause",
    "evidence": {
        "elapsed_time": {
            "baseline_minutes": 71,
            "trial_minutes": 55,
            "proposed_gain_percent": 15,
            "threshold_status": "unapproved",
            "observation": "proposed_gain_cleared",
        },
        "accepted_without_major_rework": {
            "baseline": "24/30",
            "trial": "25/30",
            "band_status": "unresolved",
        },
        "escaped_defects": {
            "baseline": "1/24 accepted",
            "trial": "2/25 accepted",
            "band_status": "unresolved",
        },
        "authority_exceptions": 2,
    },
    "reason": "authority_stop_condition_triggered",
    "owner": "workflow_owner",
    "next_review": "after_exception_repair",
    "rollout_authorized": False,
}
