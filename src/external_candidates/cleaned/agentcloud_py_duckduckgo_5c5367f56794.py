# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\tools.py\builtins.py\duckduckgo_5c5367f56794.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\tools\builtins\duckduckgo.py

from langchain_community.tools import DuckDuckGoSearchResults

from tools.builtins.base import BaseBuiltinTool


class DuckDuckGoSearchTool(BaseBuiltinTool):
    ddg: DuckDuckGoSearchResults

    def __init__(self, **kwargs):
        kwargs["ddg"] = DuckDuckGoSearchResults()

        super().__init__(**kwargs)

    def run_tool(self, query: str) -> str:
        results = self.ddg.run(query)

        self.logger.debug(f"{self.__class__.__name__} search results: {results}")

        return results
