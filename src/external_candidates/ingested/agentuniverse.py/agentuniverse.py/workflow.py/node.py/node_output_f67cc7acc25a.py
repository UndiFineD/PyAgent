# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\workflow\node\node_output.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/8/20 20:03
# @Author  : wangchongshi
# @Email   : wangchongshi.wcs@antgroup.com
# @FileName: node_output.py
from typing import Any, Dict, Optional

from agentuniverse.workflow.node.enum import NodeStatusEnum
from pydantic import BaseModel


class NodeOutput(BaseModel):
    """The basic class of the node output."""

    node_id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    status: NodeStatusEnum = NodeStatusEnum.RUNNING
    metadata: Optional[Dict[str, Any]] = None
    edge_source_handler: Optional[str] = None
