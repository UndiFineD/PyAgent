# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-make-circuit-boards\tests\test_test.py
"""
This is a test tester to make sure the project's setup properly
"""

import pytest


def test_pass():
    pass


@pytest.mark.xfail
def test_fail():
    raise AssertionError
