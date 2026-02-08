# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\tool.py\tool_reference_7227c5fcfcb1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\tool\tool_reference.py

from pydantic import BaseModel


class ToolReferenceData(BaseModel):
    name: str

    sop_count: int
