# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\tests.py\pdfalyzer.py\helpers.py\test_rich_text_helper_2d3b9ceea782.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\tests\pdfalyzer\helpers\test_rich_text_helper.py

from pdfalyzer.helpers.rich_text_helper import quoted_text


def test_quoted_text():

    assert quoted_text("xyz").plain == "'xyz'"

    assert quoted_text("-1", quote_char='"').plain == '"-1"'
