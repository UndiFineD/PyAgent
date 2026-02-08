# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse_product\service\model\session_dto.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/7/26 14:26
# @Author  : wangchongshi
# @Email   : wangchongshi.wcs@antgroup.com
# @FileName: session_dto.py
from typing import Optional

from agentuniverse_product.service.model.message_dto import MessageDTO
from pydantic import BaseModel, Field


class SessionDTO(BaseModel):
    id: str = Field(description="ID")
    agent_id: str = Field(description="session agent id")
    messages: Optional[list[MessageDTO]] = Field(description="session messages", default=[])
    gmt_created: Optional[str] = Field(description="session create time")
    gmt_modified: Optional[str] = Field(description="session update time")
