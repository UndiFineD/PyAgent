# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\llm.py\prompt.py\base_be5360c6785e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\prompt\base.py

from ...schema.llm import ToolSchema


class BasePrompt:
    @classmethod
    def system_prompt(cls, *args, **kwargs) -> str:

        pass

    @classmethod
    def pack_task_input(cls, *args, **kwargs) -> str:

        pass

    @classmethod
    def prompt_kwargs(cls) -> str:

        pass

    @classmethod
    def tool_schema(cls) -> list[ToolSchema]:

        pass
