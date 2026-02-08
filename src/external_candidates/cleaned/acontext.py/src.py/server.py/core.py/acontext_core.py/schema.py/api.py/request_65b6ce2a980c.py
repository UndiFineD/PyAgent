# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\api\request.py
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from ..utils import asUUID

SearchMode = Literal["fast", "agentic"]


class ToolRename(BaseModel):
    old_name: str = Field(..., description="Old tool name")
    new_name: str = Field(..., description="New tool name")


class ToolRenameRequest(BaseModel):
    rename: list[ToolRename] = Field(..., description="List of tool renames")


class InsertBlockRequest(BaseModel):
    parent_id: Optional[asUUID] = Field(None, description="Parent block ID (optional for page/folder types)")
    props: dict[str, Any] = Field(..., description="Block properties")
    title: str = Field(..., description="Block title")
    type: str = Field(..., description="Block type")
