# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\base.py
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from ...schema.llm import ToolSchema
from ...schema.result import Result


@dataclass
class Tool:
    schema: ToolSchema = None
    handler: Callable[..., Awaitable[Result[str]]] = None

    def use_schema(self, schema: ToolSchema) -> "Tool":
        self.schema = schema
        return self

    def use_handler(self, handler: Callable[..., Awaitable[Result[str]]]) -> "Tool":
        self.handler = handler
        return self


ToolPool = dict[str, Tool]
