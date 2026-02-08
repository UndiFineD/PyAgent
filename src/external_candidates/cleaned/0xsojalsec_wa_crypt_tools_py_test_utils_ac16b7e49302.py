# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_wa_crypt_tools.py\tests.py\lib.py\test_utils_ac16b7e49302.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wa-crypt-tools\tests\lib\test_utils.py

from wa_crypt_tools.lib.utils import hexstring2bytes


class TestUtils:
    # Sample test to test the test infrastructure (!)

    def test_hexstring2bytes(self):
        assert hexstring2bytes("0" * 64) == b"\x00" * 32
