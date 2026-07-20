import unittest

from workflow_metrics import WorkflowAttempt
from workflow_metrics import quality_success_rate


class QualitySuccessRateTests(unittest.TestCase):
    minimum_quality = 0.80

    def test_failed_attempts_remain_in_denominator(self):
        attempts = [
            WorkflowAttempt("succeeded", 0.94),
            WorkflowAttempt("failed", 0.00),
        ]

        rate = quality_success_rate(
            attempts,
            self.minimum_quality,
        )

        self.assertEqual(rate, 0.50)

    def test_successes_are_checked_for_quality(self):
        attempts = [
            WorkflowAttempt("succeeded", 0.91),
            WorkflowAttempt("succeeded", 0.72),
        ]

        rate = quality_success_rate(
            attempts,
            self.minimum_quality,
        )

        self.assertEqual(rate, 0.50)

    def test_pending_attempts_are_excluded(self):
        attempts = [
            WorkflowAttempt("succeeded", 0.91),
            WorkflowAttempt("pending", 0.99),
        ]

        rate = quality_success_rate(
            attempts,
            self.minimum_quality,
        )

        self.assertEqual(rate, 1.00)

    def test_no_terminal_attempts_returns_zero(self):
        attempts = [
            WorkflowAttempt("pending", 0.99),
        ]

        rate = quality_success_rate(
            attempts,
            self.minimum_quality,
        )

        self.assertEqual(rate, 0.00)


if __name__ == "__main__":
    unittest.main()
