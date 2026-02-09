# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-OpenBot\python\tests\test_download_data.py
import os

import pytest
from download_data import get_data

CUR_DIR = os.path.join(os.path.dirname(__file__))


def test_download_data():
    get_data(CUR_DIR)


if __name__ == "__main__":
    test_download_data()
