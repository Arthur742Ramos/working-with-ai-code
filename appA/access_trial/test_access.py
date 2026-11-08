import unittest

from service import get_job


class AccessTests(unittest.TestCase):
    def test_owner_reads_job(self):
        job = get_job("u1", "job-1")
        self.assertEqual(job["status"], "ready")

    def test_another_owner_cannot_read_job(self):
        self.assertIsNone(get_job("u2", "job-1"))

    def test_second_owner_reads_own_job(self):
        job = get_job("u2", "job-2")
        self.assertEqual(job["status"], "queued")

    def test_unknown_job_is_absent(self):
        self.assertIsNone(get_job("u1", "missing"))
