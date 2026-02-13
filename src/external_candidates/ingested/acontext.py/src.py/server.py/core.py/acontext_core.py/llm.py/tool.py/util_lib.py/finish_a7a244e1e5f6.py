# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\util_lib\finish.py
from ....schema.llm import ToolSchema
from ..base import Tool

_finish_tool = Tool().use_schema(
    ToolSchema(
        function={
            "name": "finish",
            "description": "Call it when you have completed everything you need to do in this workspace.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
    )
)
