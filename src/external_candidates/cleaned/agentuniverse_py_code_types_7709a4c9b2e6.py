# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\knowledge.py\doc_processor.py\types.py\code_types_7709a4c9b2e6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\knowledge\doc_processor\types\code_types.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2025/3/4 15:06

# @Author  : hiro

# @Email   : hiromesh@qq.com

# @FileName: code_types.py

from typing import Dict, Optional, TypedDict

from agentuniverse.agent.action.knowledge.doc_processor.types.ast_types import AstNode

from agentuniverse.agent.action.knowledge.doc_processor.types.metrics_types import (
    CodeMetrics,
)


class CodeFeatures(TypedDict):
    node_counts: Dict[str, int]

    code_metrics: CodeMetrics

    identifier_count: int

    function_count: int

    class_count: int

    statement_count: int


class CodeRepresentation(TypedDict):
    ast: AstNode

    features: CodeFeatures

    language: str

    code_length: int


class ChunkRepresentation(TypedDict):
    ast: AstNode

    code: str

    language: str

    name: Optional[str]

    type: str
