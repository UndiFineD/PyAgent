# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\util_lib\think.py
from typing import Any

from ....env import LOG
from ....schema.llm import ToolSchema
from ....schema.result import Result
from ..base import Tool


async def _thinking_handler(
    ctx: Any,
    llm_arguments: dict,
) -> Result[str]:
    LOG.info(f"Agent reports its thinking: {llm_arguments.get('thinking', '...')}")
    return Result.resolve("thinking reported")


_thinking_tool = (
    Tool()
    .use_schema(
        ToolSchema(
            function={
                "name": "report_thinking",
                "description": "Use this tool to report your thinking step by step. It will not obtain new information or change the database, but just append the thought to the log.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "thinking": {
                            "type": "string",
                            "description": "report your thinking here",
                        },
                    },
                    "required": ["thinking"],
                },
            }
        )
    )
    .use_handler(_thinking_handler)
)
