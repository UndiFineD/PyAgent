# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\tools.py\builtins.py\stackexchange_9ab7840436f3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\tools\builtins\stackexchange.py

from langchain_community.utilities import StackExchangeAPIWrapper

from tools.builtins.base import BaseBuiltinTool


class StackExchangeTool(BaseBuiltinTool):
    stackexchange: StackExchangeAPIWrapper

    def __init__(self, **kwargs):
        kwargs["stackexchange"] = StackExchangeAPIWrapper()

        super().__init__(**kwargs)

    def run_tool(self, query: str) -> str:
        results = self.stackexchange.run(query)

        self.logger.debug(f"{self.__class__.__name__} search results: {results}")

        return results
