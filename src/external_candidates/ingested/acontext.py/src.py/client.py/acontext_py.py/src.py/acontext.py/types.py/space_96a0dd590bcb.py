# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\client\acontext-py\src\acontext\types\space.py
"""Type definitions for space resources."""

from typing import Any

from pydantic import BaseModel, Field


class Space(BaseModel):
    """Space model representing a space resource."""

    id: str = Field(..., description="Space UUID")
    project_id: str = Field(..., description="Project UUID")
    configs: dict[str, Any] | None = Field(
        None, description="Space configuration dictionary"
    )
    created_at: str = Field(..., description="ISO 8601 formatted creation timestamp")
    updated_at: str = Field(..., description="ISO 8601 formatted update timestamp")


class ListSpacesOutput(BaseModel):
    """Response model for listing spaces."""

    items: list[Space] = Field(..., description="List of spaces")
    next_cursor: str | None = Field(None, description="Cursor for pagination")
    has_more: bool = Field(..., description="Whether there are more items")


class SearchResultBlockItem(BaseModel):
    """Search result block item model."""

    block_id: str = Field(..., description="Block UUID")
    title: str = Field(..., description="Block title")
    type: str = Field(..., description="Block type")
    props: dict[str, Any] = Field(..., description="Block properties")
    distance: float | None = Field(
        None, description="Cosine distance (0=identical, 2=opposite)"
    )


class SpaceSearchResult(BaseModel):
    """Experience search result model."""

    cited_blocks: list[SearchResultBlockItem] = Field(
        ..., description="List of cited blocks"
    )
    final_answer: str | None = Field(None, description="AI-generated final answer")
