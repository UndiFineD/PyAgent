# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\base.py\annotation.py\singleton_43b5a8db7fa4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\base\annotation\singleton.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/4/2 15:21

# @Author  : jerry.zzw

# @Email   : jerry.zzw@antgroup.com

# @FileName: singleton.py

from functools import wraps


def singleton(cls):
    """Decorator to make a class a Singleton class (only one instance), using closure."""

    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return get_instance
