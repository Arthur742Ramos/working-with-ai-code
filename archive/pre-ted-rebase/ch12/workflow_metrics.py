from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowAttempt:
    status: str
    quality_score: float


def quality_success_rate(
    attempts: list[WorkflowAttempt],
    minimum_quality: float,
) -> float:
    successful_attempts = [
        attempt
        for attempt in attempts
        if attempt.status == "succeeded"
    ]
    if not successful_attempts:
        return 0.0

    passing_count = sum(
        attempt.quality_score >= minimum_quality
        for attempt in successful_attempts
    )
    return passing_count / sum(
        attempt.status in {"succeeded", "failed"}
        for attempt in attempts
    )
