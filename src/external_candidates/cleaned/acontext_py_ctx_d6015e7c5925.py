# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\llm.py\tool.py\task_lib.py\ctx_d6015e7c5925.py
# NOTE: extracted with static-only rules; review before use

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
