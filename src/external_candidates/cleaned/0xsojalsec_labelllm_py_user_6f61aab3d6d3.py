# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\models.py\user_6f61aab3d6d3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\models\user.py

import time

from typing import Annotated

from app import schemas

from beanie import Document, Indexed

from pydantic import BaseModel, Field


class User(Document):
    # 用户id, 目前使用sso的id

    user_id: Annotated[str, Indexed(unique=True)]

    # 用户密码

    password: str

    # 用户角色

    role: schemas.user.UserType

    # 用户名称

    name: str

    # 创建时间

    create_time: int = 0

    # 更新时间

    update_time: int = 0


class UserCreate(BaseModel):
    user_id: str

    name: str

    password: str

    role: schemas.user.UserType = schemas.user.UserType.USER

    create_time: int = Field(default_factory=lambda: int(time.time()))

    update_time: int = Field(default_factory=lambda: int(time.time()))


class UserUpdate(BaseModel):
    name: str | None = Field(default=None)

    role: schemas.user.UserType | None = Field(default=None)

    update_time: int = Field(default_factory=lambda: int(time.time()))
