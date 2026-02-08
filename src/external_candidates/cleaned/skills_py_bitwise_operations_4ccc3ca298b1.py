# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\chocomintx.py\xiaohongshutools.py\scripts.py\units.py\fuck_reverse_crypto.py\bitwise_operations_4ccc3ca298b1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\units\fuck_reverse_crypto\bitwise_operations.py


def unsigned_left_shift(value, shift):
    """无符号左移"""

    return (value << shift) & 0xFFFFFFFF


def unsigned_right_shift(value, shift):
    """无符号右移"""

    return (value & 0xFFFFFFFF) >> shift
