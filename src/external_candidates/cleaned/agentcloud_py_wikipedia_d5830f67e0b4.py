# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\tools.py\builtins.py\wikipedia_d5830f67e0b4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\tools\builtins\wikipedia.py

from langchain_community.tools.wikipedia.tool import (
    WikipediaAPIWrapper,
    WikipediaQueryRun,
)

from langchain_core.tools import ToolException

from tools.builtins.base import BaseBuiltinTool


class WikipediaTool(BaseBuiltinTool):
    wikipedia: WikipediaQueryRun

    def __init__(self, **kwargs):
        kwargs["wikipedia"] = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

        super().__init__(**kwargs)

    def run_tool(self, query: str) -> str:
        results = self.wikipedia.run(query)

        self.logger.debug(f"{self.__class__.__name__} search results: {results}")

        return results
