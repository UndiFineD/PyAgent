# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\knowledge.py\store.py\store_manager_9d2f3ff2b0b1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\knowledge\store\store_manager.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/7/24 11:45

# @Author  : fanen.lhy

# @Email   : fanen.lhy@antgroup.com

# @FileName: store_manager.py

from agentuniverse.agent.action.knowledge.store.store import Store

from agentuniverse.base.annotation.singleton import singleton

from agentuniverse.base.component.component_enum import ComponentEnum

from agentuniverse.base.component.component_manager_base import ComponentManagerBase


@singleton
class StoreManager(ComponentManagerBase[Store]):
    """A singleton manager class of the reader."""

    def __init__(self):
        super().__init__(ComponentEnum.STORE)
