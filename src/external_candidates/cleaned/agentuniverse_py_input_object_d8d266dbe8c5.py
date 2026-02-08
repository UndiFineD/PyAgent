# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\input_object_d8d266dbe8c5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\input_object.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/3/13 15:39

# @Author  : heji

# @Email   : lc299034@antgroup.com

# @FileName: input_object.py

import json


class InputObject(object):
    def __init__(self, params: dict):
        self.__params = params

        for k, v in params.items():
            self.__dict__[k] = v

    def to_dict(self):
        return self.__params

    def to_json_str(self):
        return json.dumps(self.__params)

    def add_data(self, key, value):
        self.__params[key] = value

        self.__dict__[key] = value

    def get_data(self, key, default=None):
        return self.__params.get(key, default)
