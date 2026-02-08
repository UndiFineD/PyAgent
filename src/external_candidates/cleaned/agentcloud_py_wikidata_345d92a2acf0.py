# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\tools.py\builtins.py\wikidata_345d92a2acf0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\tools\builtins\wikidata.py

from typing import Type

from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun

from langchain_core.tools import BaseTool, ToolException

from tools.builtins.base import BaseBuiltinTool


class WikidataTool(BaseBuiltinTool):
    wikidata: WikidataQueryRun

    def __init__(self, **kwargs):
        kwargs["wikidata"] = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())

        super().__init__(**kwargs)

    def run_tool(self, query: str) -> str:
        results = self.wikidata.run(query)

        self.logger.debug(f"{self.__class__.__name__} search results: {results}")

        return results
