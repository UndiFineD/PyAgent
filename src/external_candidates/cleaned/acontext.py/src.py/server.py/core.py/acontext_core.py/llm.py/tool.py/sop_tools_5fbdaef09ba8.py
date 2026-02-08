# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\sop_tools.py
from .base import ToolPool
from .sop_lib.ctx import SOPCtx  # noqa: F401
from .sop_lib.submit import _submit_sop_tool
from .sop_lib.think import _thinking_tool

SOP_TOOLS: ToolPool = {}


SOP_TOOLS[_submit_sop_tool.schema.function.name] = _submit_sop_tool
SOP_TOOLS[_thinking_tool.schema.function.name] = _thinking_tool
