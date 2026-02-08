# Refactored by Copilot placeholder
# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\utils\dict_utils.py
# NOTE: extracted with static-only rules; review before use


def exclude_items(dictionary: dict, keys_to_exclude: list) -> dict:
    return {k: v for k, v in dictionary.items() if k not in keys_to_exclude}
