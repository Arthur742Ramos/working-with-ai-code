import unittest

from parser import parse_count


class CountTests(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(parse_count("3"), 3)

    def test_zero(self):
        self.assertEqual(parse_count("0"), 0)

    def test_non_integer(self):
        with self.assertRaises(ValueError):
            parse_count("three")

    def test_negative(self):
        with self.assertRaises(ValueError):
            parse_count("-1")
