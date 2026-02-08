# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\knowledge.py\doc_processor.py\types.py\ast_types_a0897b06de86.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\knowledge\doc_processor\types\ast_types.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2025/3/4 15:05

# @Author  : hiro

# @Email   : hiromesh@qq.com

# @FileName: ast_types.py

from typing import Any, List, Optional, TypedDict


class AstNodePoint(TypedDict):
    row: int

    column: int


class AstNode(TypedDict):
    type: str

    start_point: AstNodePoint

    end_point: AstNodePoint

    start_byte: int

    end_byte: int

    text: Optional[str]

    children: Optional[List["AstNode"]]


class CodeBoundary(TypedDict):
    start: int

    end: int

    type: str

    name: Optional[str]

    node: Any
