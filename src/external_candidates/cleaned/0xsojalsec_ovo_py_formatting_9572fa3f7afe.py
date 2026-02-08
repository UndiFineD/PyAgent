# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\core.py\utils.py\formatting_9572fa3f7afe.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\utils\formatting.py

import hashlib

import os

import random

import re

import string

import uuid

from typing import Any, Collection

import numpy as np


def format_duration(td):
    """Returns: 1 day 2 hours and 5 minutes"""

    days = td.days

    hours, remainder = divmod(td.seconds, 3600)

    minutes, _ = divmod(remainder, 60)

    parts = []

    if days:
        parts.append(f"{days} day{'s' if days > 1 else ''}")

    if hours:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")

    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    return " and ".join(parts) if parts else "0 minutes"


def generate_id(previous_ids: Collection[str]) -> str:
    """Generate a unique ID using 3 or more random letters.

    Args:

        previous_ids: List of existing IDs to avoid.

    Returns:

        str: A unique identifier.

    """

    # Choose length based on order of magnitude of previous IDs count, at least 3 characters

    # 0 -> 3, 9-9999 -> 3, 10000-99999 -> 4, 100000-999999 -> 5, etc.

    length = max(3, int(np.log10(len(previous_ids)) if previous_ids else 0))

    new_id = None

    while new_id is None or new_id in previous_ids:
        new_id = "".join(random.choices(string.ascii_letters.lower(), k=length))

    return new_id


def get_hash_of_bytes(value: bytes) -> str:
    """Get SHA1 hash string of the given bytes, for example '2aae6c35c94fcfb415dbe95f408b9ce91ee846ed'"""

    return hashlib.sha1(value).hexdigest()


def get_hashed_path_for_bytes(value: bytes) -> str:
    """Get directory and subdirectory based on SHA1 hash, for example '2a/ae6c35c94fcfb415dbe95f408b9ce91ee846ed'

                                                                         ^ Note the slash here

    This is done similarly to nextflow workdir to avoid exceeding the directory limit of some filesystems.

    """

    hash_str = get_hash_of_bytes(value)

    return os.path.join(hash_str[:2], hash_str[2:])


def safe_filename(filename):

    # Allow only the specified characters

    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", filename).strip(".")


def parse_args(argv: list[str]) -> dict:
    """Parse list of args into a dict

    For example: ['--foo', 'bar', '--bar', 'baz', '--flag']

    into dict {'foo': 'bar', 'bar': 'baz', 'flag': True}

    """

    result = {}

    i = 0

    while i < len(argv):
        arg = argv[i]

        if arg.startswith("--"):
            key = arg.removeprefix("--")

            # If next is missing or is another flag → treat as boolean

            # Make sure to parse --run_params "--foo bar" as {"run_params": "--foo bar"} instead of {"run_params": True, "--foo bar": True}

            if i + 1 >= len(argv) or (argv[i + 1].startswith("--") and " " not in argv[i + 1]):
                result[key] = True

            else:
                result[key] = argv[i + 1]

                i += 1

        elif arg.startswith("-"):
            raise ValueError(f"Use double dashes --my_param value, got: {arg}")

        else:
            raise ValueError(f"Unexpected positional argument: {arg}")

        i += 1

    return result


def get_alphanumeric_sort_key(value: str) -> tuple:
    """Get a sort key that sorts strings with numbers in an alphanumeric way.

    For example, "item2" will come before "item10".

    :param value: The string to generate a sort key for.

    :return: A tuple that can be used as a sort key.

    """

    parts = re.split(r"(\d+)", value)

    return tuple([int(part) if part.isdigit() else (part or "").lower() for part in parts])


def sorted_alphanumeric(values: Collection[str]) -> list[str]:
    """Sort a list of strings in an alphanumeric  way.

    For example, "item2" will come before "item10".

    :param values: The list of strings to sort.

    :return: The sorted list of strings.

    """

    return sorted(values, key=get_alphanumeric_sort_key)


def truncated_list(items: Collection[Any], max_items: int, sep: str = ", ") -> str:
    """Join a list truncated to a maximum number of items, adding ellipsis if necessary."""

    if len(items) <= max_items:
        return sep.join(str(item) for item in items)

    else:
        return sep.join(str(item) for item in list(items)[:max_items]) + sep + "..."
