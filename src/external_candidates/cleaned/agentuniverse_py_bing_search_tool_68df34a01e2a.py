# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\tool.py\common_tool.py\bing_search_tool_68df34a01e2a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\tool\common_tool\bing_search_tool.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    :

# @Author  :

# @Email   :

# @FileName: bing_search_tool.py

from typing import Optional

from agentuniverse.agent.action.tool.common_tool.mock_search_tool import MockSearchTool

from agentuniverse.agent.action.tool.tool import Tool, ToolInput

from agentuniverse.base.util.env_util import get_from_env

from langchain_community.utilities import BingSearchAPIWrapper

from pydantic import Field


class BingSearchTool(Tool):
    """The demo bing search tool.

    Implement the execute method of demo bing search tool, using the `BingSearchAPIWrapper` to implement a simple Bing search.

    """

    bing_subscription_key: Optional[str] = Field(default_factory=lambda: get_from_env("BING_SUBSCRIPTION_KEY"))

    bing_search_url: Optional[str] = Field(default="https://api.bing.microsoft.com/v7.0/search")

    def execute(self, input: str):
        if self.bing_subscription_key is None:
            return MockSearchTool().execute(input)

        query = input

        # get top5 results from Bing search.

        search = BingSearchAPIWrapper(
            bing_subscription_key=self.bing_subscription_key,
            k=5,
            bing_search_url=self.bing_search_url,
        )

        return search.run(query=query)
