# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_klavis.py\open_strata.py\src.py\strata.py\utils.py\dict_utils_2aa82321ba51.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\open-strata\src\strata\utils\dict_utils.py

from typing import Any, Dict, Optional


def find_in_dict_case_insensitive(name: str, dictionary: Dict[str, Any]) -> Optional[str]:
    """Helper function to find name in dictionary using case-insensitive matching.

    Args:

        name: The name to search for

        dictionary: Dictionary to search in

    Returns:

        The actual key from the dictionary if found, None otherwise

    """

    if not isinstance(name, str) or not dictionary:
        return None

    # First try exact match

    if name in dictionary:
        return name

    # Then try case-insensitive match

    name_lower = name.lower()

    for key in dictionary.keys():
        if isinstance(key, str) and key.lower() == name_lower:
            return key

    return None
