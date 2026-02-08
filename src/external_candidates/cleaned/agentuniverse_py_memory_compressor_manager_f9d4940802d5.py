# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\memory.py\memory_compressor.py\memory_compressor_manager_f9d4940802d5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\memory\memory_compressor\memory_compressor_manager.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/10/9 19:33

# @Author  : wangchongshi

# @Email   : wangchongshi.wcs@antgroup.com

# @FileName: memory_compressor_manager.py

from agentuniverse.agent.memory.memory_compressor.memory_compressor import (
    MemoryCompressor,
)

from agentuniverse.base.annotation.singleton import singleton

from agentuniverse.base.component.component_enum import ComponentEnum

from agentuniverse.base.component.component_manager_base import ComponentManagerBase


@singleton
class MemoryCompressorManager(ComponentManagerBase[MemoryCompressor]):
    """A singleton manager class of the MemoryCompressor."""

    def __init__(self):
        super().__init__(ComponentEnum.MEMORY_COMPRESSOR)
