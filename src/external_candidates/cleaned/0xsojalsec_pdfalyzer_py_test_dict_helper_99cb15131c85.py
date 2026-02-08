# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\tests.py\pdfalyzer.py\helpers.py\test_dict_helper_99cb15131c85.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\tests\pdfalyzer\helpers\test_dict_helper.py

from pdfalyzer.helpers.dict_helper import get_dict_key_by_value


def test_get_dict_key_by_value():
    arr = [1, 2, 3]

    hsh = {"a": 1, "b": b"BYTES", 1: arr}

    assert get_dict_key_by_value(hsh, 1) == "a"

    assert get_dict_key_by_value(hsh, b"BYTES") == "b"

    assert get_dict_key_by_value(hsh, arr) == 1
