# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\tool.py\enum_f82bbd46c75d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\tool\enum.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/3/13 14:34

# @Author  : wangchongshi

# @Email   : wangchongshi.wcs@antgroup.com

# @FileName: enum.py

import enum

from enum import Enum


@enum.unique
class ToolTypeEnum(Enum):
    API = "api"

    MCP = "mcp"

    FUNC = "func"
