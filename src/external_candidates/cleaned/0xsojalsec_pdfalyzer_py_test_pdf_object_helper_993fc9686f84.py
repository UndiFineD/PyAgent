# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\tests.py\pdfalyzer.py\helpers.py\test_pdf_object_helper_993fc9686f84.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\tests\pdfalyzer\helpers\test_pdf_object_helper.py

from pdfalyzer.util.adobe_strings import has_indeterminate_prefix


def test_has_indeterminate_prefix():

    assert not has_indeterminate_prefix("/Dobbs")

    assert has_indeterminate_prefix("/Destroy")
