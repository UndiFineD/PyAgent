# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_bitwise_operations.py
# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\units\fuck_reverse_crypto\bitwise_operations.py
# NOTE: extracted with static-only rules; review before use


def unsigned_left_shift(value, shift):
    """无符号左移"""

    return (value << shift) & 0xFFFFFFFF


def unsigned_right_shift(value, shift):
    """无符号右移"""

    return (value & 0xFFFFFFFF) >> shift
