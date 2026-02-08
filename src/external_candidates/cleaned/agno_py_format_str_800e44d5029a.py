# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\format_str_800e44d5029a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\format_str.py

from typing import Optional


def remove_indent(s: Optional[str]) -> Optional[str]:
    """

    Remove the indent from a string.

    Args:

        s (str): String to remove indent from

    Returns:

        str: String with indent removed

    """

    if s is not None and isinstance(s, str):
        return "\n".join([line.strip() for line in s.split("\n")])

    return None
