# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\pdfalyzer.py\helpers.py\dict_helper_bf50355b1ca4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\pdfalyzer\helpers\dict_helper.py

"""

Fun with dicts.

"""


def get_dict_key_by_value(_dict: dict, value):
    """Inverse of the usual dict operation"""

    return list(_dict.keys())[list(_dict.values()).index(value)]


def merge(dict1: dict, dict2: dict) -> dict:
    """Merge two dicts into a new dict"""

    return {**dict1, **dict2}
