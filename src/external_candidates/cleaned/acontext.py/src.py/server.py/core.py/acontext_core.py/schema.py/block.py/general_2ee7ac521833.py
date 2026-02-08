# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\block\general.py
from typing import TypedDict

from pydantic import BaseModel

from ..utils import asUUID


class LLMRenderBlock(BaseModel):
    title: str
    parent_id: asUUID
    order: int
    props: dict | None
    type: str
    block_id: asUUID


class LocatedContentBlock(BaseModel):
    path: str
    render_block: LLMRenderBlock


class GeneralBlockData(TypedDict):
    type: str
    data: dict
