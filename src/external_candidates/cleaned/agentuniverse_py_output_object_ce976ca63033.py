# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\output_object_ce976ca63033.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\output_object.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/3/13 15:39

# @Author  : heji

# @Email   : lc299034@antgroup.com

# @FileName: output_object.py

import json


class OutputObject(object):
    def __init__(self, params: dict):
        self.__params = params

        for k, v in params.items():
            self.__dict__[k] = v

    def to_dict(self):
        return self.__params

    def to_json_str(self):
        return json.dumps(self.__params, ensure_ascii=False)

    def get_data(self, key, default=None):
        return self.__params.get(key, default)
