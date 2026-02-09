# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\task_lib\insert.py
from ....env import LOG
from ....schema.llm import ToolSchema
from ....schema.orm import Task
from ....schema.result import Result
from ....service.data import task as TD
from ..base import Tool, ToolPool
from .ctx import TaskCtx


async def insert_task_handler(ctx: TaskCtx, llm_arguments: dict) -> Result[str]:
    r = await TD.insert_task(
        ctx.db_session,
        ctx.project_id,
        ctx.session_id,
        after_order=llm_arguments["after_task_order"],
        data={
            "task_description": llm_arguments["task_description"],
            "user_preferences": [],
            "progresses": [],
        },
    )
    t, eil = r.unpack()
    if eil:
        return r
    return Result.resolve(f"Task {t.order} created")


_insert_task_tool = (
    Tool()
    .use_schema(
        ToolSchema(
            function={
                "name": "insert_task",
                "description": "Create a new task by inserting it after the specified task order. This is used when identifying new tasks from conversation messages.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "after_task_order": {
                            "type": "integer",
                            "description": "The task order after which to insert the new task. Use 0 to insert at the beginning.",
                        },
                        "task_description": {
                            "type": "string",
                            "description": "A clear, concise description of the task, of what's should be done and what's the expected result if any.",
                        },
                    },
                    "required": ["after_task_order", "task_description"],
                },
            }
        )
    )
    .use_handler(insert_task_handler)
)
