# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\utils.py\dict_utils_65b4ce464799.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\utils\dict_utils.py


def exclude_items(dictionary: dict, keys_to_exclude: list) -> dict:

    return {k: v for k, v in dictionary.items() if k not in keys_to_exclude}
