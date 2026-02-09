# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse_product\service\model\plugin_dto.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/8/27 15:53
# @Author  : wangchongshi
# @Email   : wangchongshi.wcs@antgroup.com
# @FileName: plugin_dto.py
from typing import List, Optional

from agentuniverse_product.service.model.tool_dto import ToolDTO
from pydantic import BaseModel, Field


class PluginDTO(BaseModel):
    id: str = Field(description="ID")
    nickname: Optional[str] = Field(description="plugin nickname", default="")
    avatar: Optional[str] = Field(description="plugin avatar path", default="")
    description: Optional[str] = Field(description="plugin description", default="")
    toolset: Optional[List[ToolDTO]] = Field(description="plugin toolset", default=[])
    openapi_desc: Optional[str] = Field(description="plugin openapi schema", default="")
