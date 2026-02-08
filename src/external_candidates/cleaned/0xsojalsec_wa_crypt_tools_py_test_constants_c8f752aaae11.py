# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_wa_crypt_tools.py\tests.py\lib.py\test_constants_c8f752aaae11.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wa-crypt-tools\tests\lib\test_constants.py

from wa_crypt_tools.lib.constants import C


class TestConstants:
    def test_zip_header(self):
        assert C.ZIP_HEADER == b"PK\x03\x04"
