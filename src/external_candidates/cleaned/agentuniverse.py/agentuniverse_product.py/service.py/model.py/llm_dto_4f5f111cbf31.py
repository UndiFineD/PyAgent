# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse_product\service\model\llm_dto.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/7/25 23:27
# @Author  : wangchongshi
# @Email   : wangchongshi.wcs@antgroup.com
# @FileName: llm_dto.py
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LlmDTO(BaseModel):
    id: str = Field(description="ID")
    nickname: Optional[str] = Field(description="llm nickname", default="")
    temperature: Optional[float] = Field(description="llm temperature", default=None)
    model_name: Optional[List[str]] = Field(description="llm model name list", default=[])

    # pydantic protected_namespaces config
    model_config = ConfigDict(protected_namespaces=())
