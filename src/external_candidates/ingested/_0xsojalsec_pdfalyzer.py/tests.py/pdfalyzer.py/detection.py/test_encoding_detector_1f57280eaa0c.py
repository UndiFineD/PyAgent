# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\tests\pdfalyzer\detection\test_encoding_detector.py
import pytest


@pytest.fixture
def hebrew_win_1255():
    return {
        "encoding": "Windows-1255",
        "language": "Hebrew",
        "confidence": 0.62538832,
    }
