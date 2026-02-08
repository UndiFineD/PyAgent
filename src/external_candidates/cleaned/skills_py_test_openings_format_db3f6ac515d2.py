# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\officialpm.py\my_tesla.py\tests.py\test_openings_format_db3f6ac515d2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\officialpm\my-tesla\tests\test_openings_format.py

import unittest

from scripts.tesla import _fmt_open


class TestOpeningsFormat(unittest.TestCase):
    def test_fmt_open_none(self):
        self.assertIsNone(_fmt_open(None))

    def test_fmt_open_bool(self):
        self.assertEqual(_fmt_open(True), "Open")

        self.assertEqual(_fmt_open(False), "Closed")

    def test_fmt_open_intish(self):
        self.assertEqual(_fmt_open(1), "Open")

        self.assertEqual(_fmt_open(0), "Closed")

        self.assertEqual(_fmt_open("1"), "Open")

        self.assertEqual(_fmt_open("0"), "Closed")

    def test_fmt_open_invalid(self):
        self.assertIsNone(_fmt_open("maybe"))


if __name__ == "__main__":
    unittest.main()
