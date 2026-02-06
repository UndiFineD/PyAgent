# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\task_lib\finish.py
from typing import Any

from ....env import LOG
from ....infra.db import AsyncSession
from ....schema.llm import ToolSchema
from ....schema.orm import Task
from ....schema.result import Result
from ....schema.utils import asUUID
from ....service.data import task as TD
from ..base import Tool, ToolPool

_finish_tool = Tool().use_schema(
    ToolSchema(
        function={
            "name": "finish",
            "description": "Call it when you have completed the actions for task management.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
    )
)
