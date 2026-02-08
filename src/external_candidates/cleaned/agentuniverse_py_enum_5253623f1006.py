# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\memory.py\conversation_memory.py\enum_5253623f1006.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\memory\conversation_memory\enum.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/3/15 11:42

# @Author  : wangchongshi

# @Email   : wangchongshi.wcs@antgroup.com

# @FileName: enum.py

import enum

from enum import Enum


@enum.unique
class ConversationMessageEnum(Enum):
    INPUT = "input"

    OUTPUT = "output"


@enum.unique
class ConversationMessageSourceType(Enum):
    AGENT = "agent"

    TOOL = "tool"

    KNOWLEDGE = "knowledge"

    LLM = "llm"

    USER = "user"
