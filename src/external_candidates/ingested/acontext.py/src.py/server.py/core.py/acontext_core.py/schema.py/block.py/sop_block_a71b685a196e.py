# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\block\sop_block.py
from typing import List

from pydantic import BaseModel, Field

from ..utils import asUUID


class SOPStep(BaseModel):
    tool_name: str = Field(
        ...,
        description="exact corresponding tool name from history",
    )
    action: str = Field(
        ...,
        description="what to do with this tool",
    )


class SOPData(BaseModel):
    use_when: str = Field(
        ...,
        description="The scenario when this sop maybe used (3~5words), e.g. 'Broswering xxx.com for items' infos', 'Query Lung disease from Database'",
    )
    preferences: str = Field(
        ...,
        description="User preferences on this SOP if any.",
    )
    tool_sops: List[SOPStep]


class SubmitSOPData(SOPData):
    is_easy_task: bool = Field(
        ...,
        description="If the task is easy or not",
    )


class SOPBlock(SOPData):
    id: asUUID
    space_id: asUUID
