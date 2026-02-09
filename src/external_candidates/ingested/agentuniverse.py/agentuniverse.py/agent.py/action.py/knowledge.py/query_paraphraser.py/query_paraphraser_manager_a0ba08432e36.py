# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\knowledge\query_paraphraser\query_paraphraser_manager.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/7/24 11:37
# @Author  : fanen.lhy
# @Email   : fanen.lhy@antgroup.com
# @FileName: query_paraphraser_manager.py

from agentuniverse.agent.action.knowledge.query_paraphraser.query_paraphraser import (
    QueryParaphraser,
)
from agentuniverse.base.annotation.singleton import singleton
from agentuniverse.base.component.component_enum import ComponentEnum
from agentuniverse.base.component.component_manager_base import ComponentManagerBase


@singleton
class QueryParaphraserManager(ComponentManagerBase[QueryParaphraser]):
    """A singleton manager class of the QueryParaphraser."""

    def __init__(self):
        super().__init__(ComponentEnum.QUERY_PARAPHRASER)
