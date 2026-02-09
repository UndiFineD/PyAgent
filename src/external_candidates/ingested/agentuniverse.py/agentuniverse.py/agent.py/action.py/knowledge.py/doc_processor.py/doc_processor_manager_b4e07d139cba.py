# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\knowledge\doc_processor\doc_processor_manager.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/7/23 14:12
# @Author  : fanen.lhy
# @Email   : fanen.lhy@antgroup.com
# @FileName: doc_processor_manager.py

from agentuniverse.agent.action.knowledge.doc_processor.doc_processor import (
    DocProcessor,
)
from agentuniverse.base.annotation.singleton import singleton
from agentuniverse.base.component.component_enum import ComponentEnum
from agentuniverse.base.component.component_manager_base import ComponentManagerBase


@singleton
class DocProcessorManager(ComponentManagerBase[DocProcessor]):
    """A singleton manager class of the DocProcessor."""

    def __init__(self):
        super().__init__(ComponentEnum.DOC_PROCESSOR)
