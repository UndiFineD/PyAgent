# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\tests.py\pdfalyzer.py\detection.py\test_encoding_detector_1f57280eaa0c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\tests\pdfalyzer\detection\test_encoding_detector.py

import pytest


@pytest.fixture
def hebrew_win_1255():

    return {
        "encoding": "Windows-1255",
        "language": "Hebrew",
        "confidence": 0.62538832,
    }
