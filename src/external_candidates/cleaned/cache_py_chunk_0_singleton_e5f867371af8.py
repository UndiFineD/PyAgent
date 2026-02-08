# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_singleton_e5f867371af8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_singleton.py

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\units\singleton.py

# NOTE: extracted with static-only rules; review before use


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return get_instance
