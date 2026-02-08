# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\pepe276.py\moltbookagent.py\core.py\utils_bbce5e10a4bd.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\pepe276\moltbookagent\core\utils.py

import re

import string


def normalize_text_for_comparison(text: str) -> str:
    """

    Normalizes text for consistent comparison:

    1. Converts to lowercase.

    2. Removes punctuation (except maybe crucial ones, but usually strip all for keyword matching).

    3. Collapses multiple spaces.

    """

    if not text:
        return ""

    # Lowercase

    text = text.lower()

    # Remove punctuation

    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove extra whitespace

    text = re.sub(r"\s+", " ", text).strip()

    return text
