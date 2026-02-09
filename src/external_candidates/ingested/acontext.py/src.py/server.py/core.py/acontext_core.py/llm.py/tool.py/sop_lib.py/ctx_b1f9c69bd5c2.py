# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\sop_lib\ctx.py
from dataclasses import dataclass

from ....schema.session.task import TaskSchema
from ....schema.utils import asUUID


@dataclass
class SOPCtx:
    project_id: asUUID
    space_id: asUUID
    task: TaskSchema
