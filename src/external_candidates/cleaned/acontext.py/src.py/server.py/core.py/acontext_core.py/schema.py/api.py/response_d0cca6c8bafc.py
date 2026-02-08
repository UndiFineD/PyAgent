# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\api\response.py
from typing import Any, Optional

from pydantic import BaseModel, Field

from ..utils import asUUID


class SearchResultBlockItem(BaseModel):
    block_id: asUUID = Field(..., description="Block UUID")
    title: str = Field(..., description="Block title")
    type: str = Field(..., description="Block type")
    props: dict[str, Any] = Field(
        ...,
        description="Block properties. For text and sop blocks, it is the rendered props.",
    )
    distance: Optional[float] = Field(
        ...,
        description="Distance between the query and the block. None for 'agentic' mode.",
    )


class SpaceSearchResult(BaseModel):
    cited_blocks: list[SearchResultBlockItem] = Field(..., description="Cited blocks")
    final_answer: Optional[str] = Field(..., description="Final answer, not-null for 'agentic' mode.")


class Flag(BaseModel):
    status: int
    errmsg: str


class InsertBlockResponse(BaseModel):
    id: asUUID = Field(..., description="Block ID")


class LearningStatusResponse(BaseModel):
    space_digested_count: int = Field(..., description="Number of tasks that are space digested")
    not_space_digested_count: int = Field(..., description="Number of tasks that are not space digested")
