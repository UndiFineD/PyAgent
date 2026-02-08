# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\util.py\init_24bc3488186d.py
# NOTE: extracted with static-only rules; review before use

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
