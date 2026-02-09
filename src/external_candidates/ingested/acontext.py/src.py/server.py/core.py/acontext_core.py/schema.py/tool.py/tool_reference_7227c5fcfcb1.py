# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\tool\tool_reference.py
from pydantic import BaseModel


class ToolReferenceData(BaseModel):
    name: str
    sop_count: int
