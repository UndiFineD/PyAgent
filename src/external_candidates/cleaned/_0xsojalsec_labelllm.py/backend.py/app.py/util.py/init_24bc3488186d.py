# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\util\__init__.py

import random


def sample(ratio, n):
    """
    ratio in [0, 100]
    n >= 0
    """
    if 0 >= n:
        return []

    return [i for i in range(n) if ratio >= random.randint(1, 100)]
