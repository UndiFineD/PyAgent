# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\units\singleton.py
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
