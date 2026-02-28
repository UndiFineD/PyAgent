# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\task_lib\update.py
import asyncio

from ....infra.async_mq import MQ_CLIENT
from ....schema.llm import ToolSchema
from ....schema.mq.space import NewTaskComplete
from ....schema.result import Result
from ....schema.session.task import TaskStatus
from ....service.constants import EX, RK
from ....service.data import task as TD
from ..base import Tool
from .ctx import TaskCtx


async def send_complete_new_task(body: NewTaskComplete):
    await MQ_CLIENT.publish(
        exchange_name=EX.space_task,
        routing_key=RK.space_task_new_complete,
        body=body.model_dump_json(),
    )


async def update_task_handler(
    ctx: TaskCtx,
    llm_arguments: dict,
) -> Result[str]:
    task_order = llm_arguments.get("task_order", None)
    if not task_order:
        return Result.resolve(
            "You must provide a task order argument, so that we can update the task. Updating failed."
        )
    if task_order > len(ctx.task_ids_index) or task_order < 1:
        return Result.resolve(
            f"Task order {task_order} is out of range, updating failed."
        )
    actually_task_id = ctx.task_ids_index[task_order - 1]
    task_status = llm_arguments.get("task_status", None)
    task_description = llm_arguments.get("task_description", None)
    r = await TD.update_task(
        ctx.db_session,
        actually_task_id,
        status=task_status,
        patch_data=(
            {
                "task_description": task_description,
            }
            if task_description
            else None
        ),
    )
    t, eil = r.unpack()
    if eil:
        return r
    if task_status is not None and task_status == TaskStatus.SUCCESS.value:
        asyncio.create_task(
            send_complete_new_task(
                NewTaskComplete(
                    project_id=ctx.project_id,
                    session_id=ctx.session_id,
                    task_id=actually_task_id,
                )
            )
        )
    return Result.resolve(f"Task {t.order} updated")


_update_task_tool = (
    Tool()
    .use_schema(
        ToolSchema(
            function={
                "name": "update_task",
                "description": """Update an existing task's description and/or status. 
Use this when task progress changes or task details need modification.
Mostly use it to update the task status, if you're confident about a task is running, completed or failed.
Only when the conversation explicitly mention certain task's purpose should be modified, then use this tool to update the task description.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_order": {
                            "type": "integer",
                            "description": "The order number of the task to update.",
                        },
                        "task_status": {
                            "type": "string",
                            "enum": ["pending", "running", "success", "failed"],
                            "description": "New status for the task. (optional).",
                        },
                        "task_description": {
                            "type": "string",
                            "description": "Update description for the task, of what's should be done and what's the expected result if any. (optional).",
                        },
                    },
                    "required": ["task_order"],
                },
            }
        )
    )
    .use_handler(update_task_handler)
)
