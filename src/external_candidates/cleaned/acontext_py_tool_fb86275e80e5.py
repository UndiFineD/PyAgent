# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\client.py\acontext_py.py\src.py\acontext.py\types.py\tool_fb86275e80e5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\client\acontext-py\src\acontext\types\tool.py

"""Type definitions for tool resources."""

from pydantic import BaseModel, Field


class FlagResponse(BaseModel):
    """Flag response with status and error message."""

    status: int = Field(..., description="Status code")

    errmsg: str = Field(..., description="Error message")


class InsertBlockResponse(BaseModel):
    """Response from inserting a block."""

    id: str = Field(..., description="Block UUID")


class ToolReferenceData(BaseModel):
    """Tool reference data."""

    name: str = Field(..., description="Tool name")

    sop_count: int = Field(..., description="Number of SOPs using this tool")


class ToolRenameItem(BaseModel):
    """Tool rename item."""

    old_name: str = Field(..., description="Old tool name")

    new_name: str = Field(..., description="New tool name")
