# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\sop_lib\think.py
from ....env import LOG
from ....infra.db import DB_CLIENT
from ....schema.llm import ToolSchema
from ....schema.result import Result
from ....service.data import task as TD
from ..base import Tool
from .ctx import SOPCtx


async def _thinking_handler(
    ctx: SOPCtx,
    llm_arguments: dict,
) -> Result[str]:
    LOG.info(f"Agent reports its thinking: {llm_arguments.get('thinking', '...')}")
    sop_thinking = llm_arguments.get("thinking", None)
    if sop_thinking is None:
        return Result.resolve("No thinking provided")
    async with DB_CLIENT.get_session_context() as db_session:
        await TD.append_sop_thinking_to_task(db_session, ctx.task.id, sop_thinking)
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
