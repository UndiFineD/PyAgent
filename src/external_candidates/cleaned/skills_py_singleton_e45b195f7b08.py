# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\chocomintx.py\xiaohongshutools.py\scripts.py\units.py\singleton_e45b195f7b08.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\units\singleton.py


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return get_instance
