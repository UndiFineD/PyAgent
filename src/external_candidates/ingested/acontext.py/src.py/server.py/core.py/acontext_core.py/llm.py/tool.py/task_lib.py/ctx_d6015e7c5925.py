# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\task_lib\ctx.py
from dataclasses import dataclass

from ....infra.db import AsyncSession
from ....schema.session.task import TaskSchema
from ....schema.utils import asUUID


@dataclass
class TaskCtx:
    db_session: AsyncSession
    project_id: asUUID
    session_id: asUUID
    task_ids_index: list[asUUID]
    task_index: list[TaskSchema]
    message_ids_index: list[asUUID]
